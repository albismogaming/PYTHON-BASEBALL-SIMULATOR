import pickle
import math as m
from typing import Dict, Tuple
from pathlib import Path
from DATA_LOADERS.TEAM_LOADER import TeamLoader
from DATA_LOADERS.LEAGUE_STATS_LOADER import LeagueLoader
from CONTEXT.PLAYER_CONTEXT import Player
from UTILITIES.FILE_PATHS import MATCHUP_TABLE, TEAM_META, TEAM_PATH, LEAGUE_DATA


def calculate_base_probability(batter_prob, pitcher_prob, batter_weight=0.50, pitcher_weight=0.50):
    """ Calculate combined probability using logit transformation (log-odds). """
    # Avoid division by zero and extreme values
    epsilon = 1e-6
    batter_prob = max(epsilon, min(batter_prob, 1 - epsilon))
    pitcher_prob = max(epsilon, min(pitcher_prob, 1 - epsilon))
    
    # Convert to log-odds (logit transformation)
    batter_logit = m.log(batter_prob / (1 - batter_prob))
    pitcher_logit = m.log(pitcher_prob / (1 - pitcher_prob))
    
    # Weighted average in log-odds space
    combined_logit = (batter_logit * batter_weight) + (pitcher_logit * pitcher_weight)
    
    # Convert back to probability (inverse logit)
    return 1 / (1 + m.exp(-combined_logit))


def calculate_split_advantage(batter, pitcher) -> float:
    """Calculate platoon advantage multiplier."""
    if batter.bats == 'B':
        return 1.05  # Switch hitters always get 5% boost
    
    favorable = (
        (batter.bats == 'L' and pitcher.throws == 'R') or
        (batter.bats == 'R' and pitcher.throws == 'L')
    )
    
    return 1.05 if favorable else 0.95


class MatchupPrecomputer:
    """Precompute and store all batter-pitcher matchup probabilities."""


    def __init__(self, output_path: str = MATCHUP_TABLE):
        self.output_path = output_path
        self.matchup_table: Dict[Tuple[str, int, str, int], Dict[str, float]] = {}


    def load_all_teams(self) -> Tuple[list, list]:
        """
        Load all teams from TEAM_META and extract all batters and pitchers.
        
        Returns:
            Tuple of (all_batters, all_pitchers) lists
        """
        print("Loading teams...")
        metadata = TeamLoader.load_team_metadata(TEAM_META)
        
        all_batters = []
        all_pitchers = []
        
        for team_abbrev in metadata.keys():
            print(f"  Loading {team_abbrev}...")
            
            try:
                team = TeamLoader.load_full_team(team_abbrev=team_abbrev, roster_csv=f"{TEAM_PATH}\\{team_abbrev}.csv", teams_csv=f"{TEAM_META}")
                all_batters.extend(team.batters)
                all_pitchers.extend(team.pitchers)
            except FileNotFoundError:
                print(f"  Warning: Could not find roster file for {team_abbrev}, skipping...")
                continue
                
        print(f"Loaded {len(all_batters)} batters and {len(all_pitchers)} pitchers")
        return all_batters, all_pitchers
    

    def compute_matchup_probabilities(self, batter: Player, pitcher: Player) -> Dict[str, float]:
        """
        Compute all outcome probabilities for a batter-pitcher matchup.
        
        Args:
            batter: Batter Player object
            pitcher: Pitcher Player object
            league_stats: League average stats dictionary
            
        Returns:
            Dictionary with all outcome probabilities
        """
        probabilities = {}
        
        # Calculate platoon split multiplier
        split_multiplier = calculate_split_advantage(batter, pitcher)
        
        # Compute all outcome probabilities (SO, BB, HP, HR, IH, SL, DL, TL)
        for outcome in ['SO', 'BB', 'HP', 'HR', 'IH', 'SL', 'DL', 'TL']:
            batter_prob = batter.bat_stats_raw[outcome]
            pitcher_prob = pitcher.pit_stats_raw[outcome]
            
            base_prob = calculate_base_probability(batter_prob, pitcher_prob)
            
            # Apply platoon split
            probabilities[outcome] = base_prob * split_multiplier
        
        # Compute outs distribution based on GB/FB ratios
        pitcher_fb_rate = 1.0 / (1.0 + pitcher.pit_stats_raw['GBFB'])
        batter_fb_rate = 1.0 / (1.0 + batter.bat_stats_raw['GBFB'])
        
        combined_fb_rate = calculate_base_probability(batter_fb_rate, pitcher_fb_rate)
        
        # Distribute fly ball outs: 56% flyouts, 26% lineouts, 18% popouts
        probabilities['FO'] = combined_fb_rate * 0.56
        probabilities['LO'] = combined_fb_rate * 0.26
        probabilities['PO'] = combined_fb_rate * 0.18
        probabilities['GO'] = 1.0 - combined_fb_rate
        
        # Store additional context that might be useful
        probabilities['BABIP_batter'] = batter.bat_stats_raw['BABIP']
        probabilities['BABIP_pitcher'] = pitcher.pit_stats_raw['BABIP']
        probabilities['GBFB_batter'] = batter.bat_stats_raw['GBFB']
        probabilities['GBFB_pitcher'] = pitcher.pit_stats_raw['GBFB']
        probabilities['platoon_multiplier'] = split_multiplier
        
        return probabilities
    

    def precompute_all_matchups(self):
        """
        Precompute probabilities for all batter-pitcher matchups.
        """
        print("\n" + "="*60)
        print("MATCHUP PRECOMPUTATION")
        print("="*60 + "\n")
        
        # Load league stats
        print("Loading league statistics...")
        
        # Load all teams
        all_batters, all_pitchers = self.load_all_teams()
        
        # Compute all matchups
        total_matchups = len(all_batters) * len(all_pitchers)
        print(f"\nComputing {total_matchups:,} matchups...")
        
        computed = 0
        for batter in all_batters:
            for pitcher in all_pitchers:
                # Use team + player_id to create unique key (player_id is not unique across teams)
                key = (batter.team_abbrev, batter.player_id, pitcher.team_abbrev, pitcher.player_id)
                
                # Compute probabilities
                self.matchup_table[key] = self.compute_matchup_probabilities(batter, pitcher)
                
                computed += 1
                
                # Progress indicator
                if computed % 1000 == 0 or computed == total_matchups:
                    progress = (computed / total_matchups) * 100
                    print(f"  Progress: {computed:,}/{total_matchups:,} ({progress:.1f}%)")
        
        print("\nPrecomputation complete!")
        return self.matchup_table
    

    def save_table(self):
        """Save the matchup table to a pickle file."""
        print(f"\nSaving matchup table to {self.output_path}...")
        
        # Ensure directory exists
        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_path, 'wb') as f:
            pickle.dump(self.matchup_table, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Calculate file size
        file_size = Path(self.output_path).stat().st_size / (1024 * 1024)  # MB
        print(f"Saved {len(self.matchup_table):,} matchups ({file_size:.2f} MB)")
    
    def load_table(self) -> Dict[Tuple[str, int, str, int], Dict[str, float]]:
        """Load a precomputed matchup table from pickle file."""
        print(f"Loading matchup table from {self.output_path}...")
        
        with open(self.output_path, 'rb') as f:
            self.matchup_table = pickle.load(f)
        
        print(f"Loaded {len(self.matchup_table):,} matchups")
        return self.matchup_table
    
    def get_matchup_probs(self, batter_team: str, batter_id: int, pitcher_team: str, pitcher_id: int):
        """
        Retrieve precomputed probabilities for a specific matchup.
        
        Args:
            batter_team: Batter's team abbreviation
            batter_id: Batter's player ID
            pitcher_team: Pitcher's team abbreviation
            pitcher_id: Pitcher's player ID
            
        Returns:
            Dictionary of outcome probabilities, or None if not found
        """
        return self.matchup_table.get((batter_team, batter_id, pitcher_team, pitcher_id), None)
    
    def display_summary(self):
        """Display summary statistics of the matchup table."""
        print("\n" + "="*60)
        print("MATCHUP TABLE SUMMARY")
        print("="*60)
        
        print(f"\nTotal matchups: {len(self.matchup_table):,}")
        
        # Sample a matchup to show structure
        if self.matchup_table:
            sample_key = list(self.matchup_table.keys())[0]
            sample_probs = self.matchup_table[sample_key]
            
            print(f"\nSample matchup ({sample_key[0]} Batter #{sample_key[1]} vs {sample_key[2]} Pitcher #{sample_key[3]}):")
            print("\nBase Outcomes:")
            for outcome in ['SO', 'BB', 'HP', 'HR']:
                prob = sample_probs[outcome]
                print(f"  {outcome}: {prob:.4f} ({prob*100:.2f}%)")
            
            print("\nHit Outcomes:")
            for outcome in ['IH', 'SL', 'DL', 'TL']:
                prob = sample_probs[outcome]
                print(f"  {outcome}: {prob:.4f} ({prob*100:.2f}%)")
            
            print("\nAdditional Data:")
            print(f"  Platoon Multiplier: {sample_probs['platoon_multiplier']:.3f}")
            print(f"  BABIP (Batter): {sample_probs['BABIP_batter']:.3f}")
            print(f"  BABIP (Pitcher): {sample_probs['BABIP_pitcher']:.3f}")
            print(f"  GB/FB (Batter): {sample_probs['GBFB_batter']:.3f}")
            print(f"  GB/FB (Pitcher): {sample_probs['GBFB_pitcher']:.3f}")


def main():
    """Main execution function."""
    precomputer = MatchupPrecomputer()
    
    precomputer.precompute_all_matchups()
    precomputer.save_table()
    precomputer.display_summary()
    
    print("\n" + "="*60)
    print("DONE!")
    print("="*60)
    print(f"\nMatchup table saved to: {precomputer.output_path}")
    print("Use MatchupPrecomputer.load_table() to load in your simulation.")


if __name__ == "__main__":
    main()

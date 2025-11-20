from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from UTILITIES.ENUMS import Outcome


class StatsManager:
    """ Static manager for in-game statistics for batters and pitchers. """
    
    # Class-level dictionaries to store all stats
    batter_stats: Dict = {}  # Key: (team_abbrev, player_id), Value: stat dict
    pitcher_stats: Dict = {}  # Key: (team_abbrev, player_id), Value: stat dict
    
    # ==================== INITIALIZATION ====================
    
    @staticmethod
    def _get_player_key(player):
        """Get hashable key for a player."""
        return (player.team_abbrev, player.player_id)
    
    @staticmethod
    def initialize_batter(batter):
        """
        Initialize stats for a batter if not already tracked.
        
        Args:
            batter: Player object (batter)
        """
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            StatsManager.batter_stats[key] = {
                'player': batter,
                'PA': 0,      # Plate appearances
                'AB': 0,      # At-bats
                'H': 0,       # Hits
                '1B': 0,      # Singles
                '2B': 0,      # Doubles
                '3B': 0,      # Triples
                'HR': 0,      # Home runs
                'R': 0,       # Runs scored
                'RBI': 0,     # Runs batted in
                'BB': 0,      # Walks
                'SO': 0,      # Strikeouts
                'HBP': 0,     # Hit by pitch
                'TB': 0,      # Total bases
            }
    
    @staticmethod
    def initialize_pitcher(pitcher):
        """
        Initialize stats for a pitcher if not already tracked.
        
        Args:
            pitcher: Player object (pitcher)
        """
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            StatsManager.pitcher_stats[key] = {
                'player': pitcher,
                'IP': 0.0,       # Innings pitched (as outs/3)
                'PT': 0,    # Total pitches thrown
                'H': 0,          # Hits allowed
                'R': 0,          # Runs allowed
                'ER': 0,         # Earned runs
                'BB': 0,         # Walks issued
                'SO': 0,         # Strikeouts
                'HR': 0,         # Home runs allowed
                'BF': 0,         # Batters faced
                'Outs': 0,       # Outs recorded
            }
    
    # ==================== RECORD STATS ====================
    
    @staticmethod
    def record_at_bat(batter, pitcher, outcome: Outcome, pitch_count: int, runs_scored: int = 0, rbi: int = 0):
        """
        Record a complete at-bat with all relevant stats.
        
        Args:
            batter: Batter Player object
            pitcher: Pitcher Player object
            outcome: Outcome enum value
            pitch_count: Number of pitches in the at-bat
            runs_scored: Runs scored by the batter on this play
            rbi: RBIs credited to the batter
        """
        StatsManager.initialize_batter(batter)
        StatsManager.initialize_pitcher(pitcher)
        
        # Update batter stats
        StatsManager._update_batter_stats(batter, outcome, runs_scored, rbi)
        
        # Update pitcher stats
        StatsManager._update_pitcher_stats(pitcher, outcome, pitch_count)
    
    @staticmethod
    def _update_batter_stats(batter, outcome: Outcome, runs_scored: int, rbi: int):
        """Update batter statistics based on outcome."""
        key = StatsManager._get_player_key(batter)
        stats = StatsManager.batter_stats[key]
        
        # Every outcome is a plate appearance
        stats['PA'] += 1
        
        # Determine if it's an at-bat (excludes BB, HP, sacrifices)
        is_at_bat = outcome not in [Outcome.BB, Outcome.HP]
        
        if is_at_bat:
            stats['AB'] += 1
        
        if outcome in [Outcome.SL, Outcome.DL, Outcome.TL, Outcome.HR, Outcome.IH]:
            stats['H'] += 1

        # Hits
        if outcome == Outcome.SL or outcome == Outcome.IH:
            stats['1B'] += 1
            stats['TB'] += 1
        elif outcome == Outcome.DL:
            stats['2B'] += 1
            stats['TB'] += 2
        elif outcome == Outcome.TL:
            stats['3B'] += 1
            stats['TB'] += 3
        elif outcome == Outcome.HR:
            stats['HR'] += 1
            stats['TB'] += 4
        
        # Other outcomes
        if outcome == Outcome.SO:
            stats['SO'] += 1
        elif outcome == Outcome.BB:
            stats['BB'] += 1
        elif outcome == Outcome.HP:
            stats['HBP'] += 1
        
        # Runs and RBI
        stats['R'] += runs_scored
        stats['RBI'] += rbi
    
    @staticmethod
    def _update_pitcher_stats(pitcher, outcome: Outcome, pitch_count: int):
        """Update pitcher statistics based on outcome."""
        key = StatsManager._get_player_key(pitcher)
        stats = StatsManager.pitcher_stats[key]
        
        # Every at-bat is a batter faced
        stats['BF'] += 1
        stats['PT'] += pitch_count
        
        # Hits allowed
        if outcome in [Outcome.SL, Outcome.DL, Outcome.TL, Outcome.HR, Outcome.IH]:
            stats['H'] += 1
        
        # Home runs allowed
        if outcome == Outcome.HR:
            stats['HR'] += 1
        
        # Walks
        if outcome == Outcome.BB:
            stats['BB'] += 1
        
        # Strikeouts
        if outcome == Outcome.SO:
            stats['SO'] += 1
        
        # Outs recorded
        if outcome in [Outcome.SO, Outcome.GO, Outcome.FO, Outcome.LO, Outcome.PO]:
            stats['Outs'] += 1
            stats['IP'] = stats['Outs'] / 3.0
    
    @staticmethod
    def record_run_for_pitcher(pitcher, earned: bool = True):
        """
        Record a run allowed by pitcher.
        
        Args:
            pitcher: Pitcher Player object
            earned: Whether the run is earned (default True)
        """
        StatsManager.initialize_pitcher(pitcher)
        key = StatsManager._get_player_key(pitcher)
        stats = StatsManager.pitcher_stats[key]
        
        stats['R'] += 1
        if earned:
            stats['ER'] += 1
    
    # ==================== CALCULATED STATS ====================
    
    @staticmethod
    def get_batting_average(batter) -> float:
        """Calculate batting average (H / AB)."""
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            return 0.0
        stats = StatsManager.batter_stats[key]
        return stats['H'] / stats['AB'] if stats['AB'] > 0 else 0.0
    
    @staticmethod
    def get_on_base_percentage(batter) -> float:
        """Calculate on-base percentage (H + BB + HBP) / (AB + BB + HBP)."""
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            return 0.0
        stats = StatsManager.batter_stats[key]
        denominator = stats['AB'] + stats['BB'] + stats['HBP']
        if denominator == 0:
            return 0.0
        return (stats['H'] + stats['BB'] + stats['HBP']) / denominator
    
    @staticmethod
    def get_slugging_percentage(batter) -> float:
        """Calculate slugging percentage (TB / AB)."""
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            return 0.0
        stats = StatsManager.batter_stats[key]
        return stats['TB'] / stats['AB'] if stats['AB'] > 0 else 0.0
    
    @staticmethod
    def get_ops(batter) -> float:
        """Calculate OPS (OBP + SLG)."""
        return StatsManager.get_on_base_percentage(batter) + StatsManager.get_slugging_percentage(batter)
    
    @staticmethod
    def get_era(pitcher) -> float:
        """Calculate ERA (ER * 9 / IP)."""
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            return 0.0
        stats = StatsManager.pitcher_stats[key]
        if stats['IP'] == 0:
            return 0.0
        return (stats['ER'] * 9) / stats['IP']
    
    @staticmethod
    def get_whip(pitcher) -> float:
        """Calculate WHIP ((BB + H) / IP)."""
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            return 0.0
        stats = StatsManager.pitcher_stats[key]
        if stats['IP'] == 0:
            return 0.0
        return (stats['BB'] + stats['H']) / stats['IP']
    
    @staticmethod
    def format_innings_pitched(pitcher) -> str:
        """Format innings pitched (e.g., 5.2 for 5 2/3 innings)."""
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            return "0.0"
        stats = StatsManager.pitcher_stats[key]
        outs = stats['Outs']
        full_innings = outs // 3
        remaining_outs = outs % 3
        return f"{full_innings}.{remaining_outs}"
    
    # ==================== RETRIEVAL ====================
    
    @staticmethod
    def get_batter_stats(batter) -> Dict:
        """Get all stats for a specific batter."""
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            return {}
        return StatsManager.batter_stats[key].copy()
    
    @staticmethod
    def get_pitcher_stats(pitcher) -> Dict:
        """Get all stats for a specific pitcher."""
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            return {}
        return StatsManager.pitcher_stats[key].copy()
    
    @staticmethod
    def get_all_batter_stats() -> List[Dict]:
        """Get stats for all batters as a list."""
        return list(StatsManager.batter_stats.values())
    
    @staticmethod
    def get_all_pitcher_stats() -> List[Dict]:
        """Get stats for all pitchers as a list."""
        return list(StatsManager.pitcher_stats.values())
    
    @staticmethod
    def get_team_batting_stats(team_abbrev: str) -> List[Dict]:
        """Get batting stats for all players on a team."""
        return [stats for stats in StatsManager.batter_stats.values() 
                if stats['player'].team_abbrev == team_abbrev]
    
    @staticmethod
    def get_team_pitching_stats(team_abbrev: str) -> List[Dict]:
        """Get pitching stats for all pitchers on a team."""
        return [stats for stats in StatsManager.pitcher_stats.values() 
                if stats['player'].team_abbrev == team_abbrev]
    
    # ==================== FORMATTING ====================
    
    @staticmethod
    def format_batting_stats(team_abbrev: Optional[str] = None) -> str:
        """
        Format batting stats as a table.
        
        Args:
            team_abbrev: Filter by team (optional)
        
        Returns:
            Formatted string table
        """
        if team_abbrev:
            stats_list = StatsManager.get_team_batting_stats(team_abbrev)
        else:
            stats_list = StatsManager.get_all_batter_stats()
        
        if not stats_list:
            return "No batting stats recorded."
        
        lines = []
        lines.append(f"{'PLAYER':<20} {'POS':<4} {'AB':>3} {'R':>3} {'H':>3} {'2B':>3} {'3B':>3} {'HR':>3} {'RBI':>3} {'BB':>3} {'SO':>3} {'AVG':>5}")
        lines.append("-" * 80)
        
        for stats in sorted(stats_list, key=lambda x: x.get('AB', 0), reverse=True):
            player = stats['player']
            avg = StatsManager.get_batting_average(player)
            
            lines.append(
                f"{player.full_name:<20} {player.position:<4} "
                f"{stats['AB']:>3} {stats['R']:>3} {stats['H']:>3} "
                f"{stats['2B']:>3} {stats['3B']:>3} {stats['HR']:>3} "
                f"{stats['RBI']:>3} {stats['BB']:>3} {stats['SO']:>3} "
                f"{avg:>5.3f}"
            )
        
        return "\n".join(lines)
    
    @staticmethod
    def format_pitching_stats(team_abbrev: Optional[str] = None) -> str:
        """
        Format pitching stats as a table.
        
        Args:
            team_abbrev: Filter by team (optional)
        
        Returns:
            Formatted string table
        """
        if team_abbrev:
            stats_list = StatsManager.get_team_pitching_stats(team_abbrev)
        else:
            stats_list = StatsManager.get_all_pitcher_stats()
        
        if not stats_list:
            return "No pitching stats recorded."
        
        lines = []
        lines.append(f"{'PLAYER':<20} {'POS':<4} {'IP':>5} {'H':>3} {'R':>3} {'ER':>3} {'BB':>3} {'SO':>3} {'HR':>3} {'Pit':>4} {'ERA':>5}")
        lines.append("-" * 90)
        
        for stats in sorted(stats_list, key=lambda x: x.get('BF', 0), reverse=True):
            player = stats['player']
            ip_str = StatsManager.format_innings_pitched(player)
            era = StatsManager.get_era(player)
            
            lines.append(
                f"{player.full_name:<20} {player.position:<4} "
                f"{ip_str:>5} {stats['H']:>3} {stats['R']:>3} {stats['ER']:>3} "
                f"{stats['BB']:>3} {stats['SO']:>3} {stats['HR']:>3} "
                f"{stats['PT']:>4} {era:>5.2f}"
            )
        
        return "\n".join(lines)
    
    # ==================== RESET ====================
    
    @staticmethod
    def reset():
        """Clear all stats for a new game."""
        StatsManager.batter_stats.clear()
        StatsManager.pitcher_stats.clear()
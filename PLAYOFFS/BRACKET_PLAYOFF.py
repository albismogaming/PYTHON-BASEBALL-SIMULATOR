from typing import List, Dict
from GAMEDAY import play_game, load_team
from UTILITIES.COLOR_CODES import *


class BracketPlayoff:
    """Standard single-elimination bracket with optional byes."""
    
    def __init__(self, teams: List[str], config: Dict):
        """
        Initialize bracket playoff.
        
        Args:
            teams: List of teams in seeding order
            config: Playoff configuration dictionary
        """
        self.teams = teams
        self.config = config
        self.num_teams = config['num_teams']
        self.num_byes = config.get('num_byes', 0)
        self.rounds = config['rounds']
        self.teams_cache = {}
        self.series_results = {f'round_{i+1}': [] for i in range(len(self.rounds))}
    
    def _get_team(self, team_abbrev: str):
        """Get team from cache or load if not cached."""
        if team_abbrev not in self.teams_cache:
            self.teams_cache[team_abbrev] = load_team(team_abbrev)
        return self.teams_cache[team_abbrev]
    
    def simulate_series(self, higher_seed: str, lower_seed: str, 
                       round_config: Dict, series_name: str, verbose: bool = True) -> str:
        """ Simulate a playoff series between two teams. """       
        games_to_win = round_config['wins_needed']
        home_field_games = round_config['home_field_games']
        
        if verbose:
            print(f"\n{BOLD}{'='*60}{RESET}")
            print(f"{BOLD}  {series_name}{RESET}")
            print(f"{BOLD}{'='*60}{RESET}\n")
        
        higher_team = self._get_team(higher_seed)
        lower_team = self._get_team(lower_seed)
        
        higher_wins = 0
        lower_wins = 0
        game_num = 1
        
        while higher_wins < games_to_win and lower_wins < games_to_win:
            # Higher seed has home field advantage for specified games
            is_higher_seed_home = game_num in home_field_games
            home_team = higher_team if is_higher_seed_home else lower_team
            away_team = lower_team if is_higher_seed_home else higher_team
            home_abbrev = higher_seed if is_higher_seed_home else lower_seed
            away_abbrev = lower_seed if is_higher_seed_home else higher_seed
            
            # Simulate game
            away_score, home_score = play_game(away_team, home_team)
            
            # Update wins
            if away_score > home_score:
                if away_abbrev == higher_seed:
                    higher_wins += 1
                else:
                    lower_wins += 1
            else:
                if home_abbrev == higher_seed:
                    higher_wins += 1
                else:
                    lower_wins += 1
            
            if verbose:
                winner = away_abbrev if away_score > home_score else home_abbrev
                winner_color = GREEN if winner == higher_seed else CYAN
                print(f"Game {game_num}: {away_abbrev} {away_score:2} @ {home_abbrev} {home_score:2}  "
                      f"({winner_color}{winner} wins{RESET}) — Series: {higher_seed} {higher_wins}-{lower_wins} {lower_seed}")
            
            game_num += 1
        
        winner = higher_seed if higher_wins == games_to_win else lower_seed
        
        if verbose:
            print(f"\n{BOLD}{GREEN}>>> {winner} wins series {max(higher_wins, lower_wins)}-{min(higher_wins, lower_wins)} <<<{RESET}\n")
        
        return winner
    
    def simulate(self, verbose: bool = True) -> str:
        """
        Simulate complete bracket playoff.
        
        Returns:
            Champion team abbreviation
        """
        # Store original seeds for home field determination
        original_seeds = {team: i+1 for i, team in enumerate(self.teams)}
        active_teams = list(self.teams)
        
        # Simulate each round
        for round_num, round_config in enumerate(self.rounds):
            round_name = round_config['name']
            
            # First round might have byes
            if round_num == 0 and self.num_byes > 0:
                print(f"\n{CYAN}Top {self.num_byes} seeds receive BYE to {self.rounds[1]['name']}{RESET}")
                for i in range(self.num_byes):
                    print(f"  #{original_seeds[active_teams[i]]} {active_teams[i]} — BYE")
                print()
                competing_teams = active_teams[self.num_byes:]
            else:
                competing_teams = active_teams
            
            # Create matchups (higher seed vs lower seed)
            matchups = []
            num_matchups = len(competing_teams) // 2
            for i in range(num_matchups):
                higher_seed_team = competing_teams[i]
                lower_seed_team = competing_teams[-(i+1)]
                matchups.append((higher_seed_team, lower_seed_team))
                if verbose:
                    print(f"{round_name}: #{original_seeds[higher_seed_team]} {higher_seed_team} vs "
                          f"#{original_seeds[lower_seed_team]} {lower_seed_team}")
            
            # Simulate all series in this round
            round_winners = []
            for higher_seed_team, lower_seed_team in matchups:
                winner = self.simulate_series(
                    higher_seed_team, lower_seed_team,
                    round_config=round_config,
                    series_name=f"{round_name}: #{original_seeds[higher_seed_team]} {higher_seed_team} vs "
                                f"#{original_seeds[lower_seed_team]} {lower_seed_team}",
                    verbose=verbose
                )
                self.series_results[f'round_{round_num+1}'].append((higher_seed_team, lower_seed_team, winner))
                round_winners.append(winner)
            
            # Add bye teams back for next round
            if round_num == 0 and self.num_byes > 0:
                active_teams = active_teams[:self.num_byes] + round_winners
            else:
                active_teams = round_winners
            
            # Sort by original seed for next round matchups
            active_teams.sort(key=lambda t: original_seeds[t])
        
        champion = active_teams[0]
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}{GREEN}  🏆 CHAMPION: {champion} 🏆{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        return champion

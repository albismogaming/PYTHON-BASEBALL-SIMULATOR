from typing import List, Dict, Tuple
from GAMEDAY import play_game, load_team
from UTILITIES.COLOR_CODES import *


class PoolPlayPlayoff:
    """Pool play stage followed by bracket playoff."""
    
    def __init__(self, teams: List[str], config: Dict):
        """
        Initialize pool play playoff.
        
        Args:
            teams: List of teams in seeding order
            config: Playoff configuration dictionary
        """
        self.teams = teams
        self.config = config
        self.num_teams = config['num_teams']
        self.num_pools = config['num_pools']
        self.games_per_matchup = config['pool_play']['games_per_matchup']
        self.advance_per_pool = config['pool_play']['advance_per_pool']
        self.wild_cards = config['pool_play'].get('wild_cards', 0)
        self.bracket_rounds = config['bracket_rounds']
        self.teams_cache = {}
        
        # Divide teams into pools (snake draft style to balance pools)
        self.pools = self._create_pools()
        
        # Track standings per pool
        self.pool_standings = {}
        for pool_name in self.pools:
            self.pool_standings[pool_name] = {
                team: {'wins': 0, 'losses': 0, 'runs_for': 0, 'runs_against': 0}
                for team in self.pools[pool_name]
            }
    
    def _create_pools(self) -> Dict[str, List[str]]:
        """
        Divide teams into pools using snake draft to balance strength.
        Example for 8 teams, 2 pools: Pool A gets 1,4,5,8 and Pool B gets 2,3,6,7
        """
        pools = {f'Pool {chr(65+i)}': [] for i in range(self.num_pools)}
        pool_names = list(pools.keys())
        
        direction = 1  # 1 for forward, -1 for backward (snake)
        current_pool_idx = 0
        
        for team in self.teams:
            pools[pool_names[current_pool_idx]].append(team)
            
            # Move to next pool
            current_pool_idx += direction
            
            # Reverse direction at ends (snake draft)
            if current_pool_idx >= self.num_pools:
                current_pool_idx = self.num_pools - 1
                direction = -1
            elif current_pool_idx < 0:
                current_pool_idx = 0
                direction = 1
        
        return pools
    
    def _get_team(self, team_abbrev: str):
        """Get team from cache or load if not cached."""
        if team_abbrev not in self.teams_cache:
            self.teams_cache[team_abbrev] = load_team(team_abbrev)
        return self.teams_cache[team_abbrev]
    
    def simulate_pool_play(self, verbose: bool = True) -> List[str]:
        """
        Simulate pool play stage.
        
        Returns:
            List of advancing teams in order
        """
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  POOL PLAY STAGE{RESET}")
        print(f"{BOLD}  {self.num_pools} pools, each team plays pool opponents {self.games_per_matchup} times{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        # Display pool assignments
        for pool_name, pool_teams in self.pools.items():
            print(f"{CYAN}{pool_name}:{RESET} {', '.join(pool_teams)}")
        print()
        
        # Simulate games within each pool
        for pool_name, pool_teams in self.pools.items():
            print(f"\n{BOLD}--- {pool_name} Games ---{RESET}\n")
            
            # Generate all matchups within pool
            for i, team1 in enumerate(pool_teams):
                for team2 in pool_teams[i+1:]:
                    for game_num in range(1, self.games_per_matchup + 1):
                        # Alternate home field
                        if game_num % 2 == 1:
                            home_abbrev, away_abbrev = team1, team2
                        else:
                            home_abbrev, away_abbrev = team2, team1
                        
                        home_team = self._get_team(home_abbrev)
                        away_team = self._get_team(away_abbrev)
                        
                        # Simulate game
                        away_score, home_score = play_game(away_team, home_team)
                        
                        # Update standings
                        if away_score > home_score:
                            self.pool_standings[pool_name][away_abbrev]['wins'] += 1
                            self.pool_standings[pool_name][home_abbrev]['losses'] += 1
                        else:
                            self.pool_standings[pool_name][home_abbrev]['wins'] += 1
                            self.pool_standings[pool_name][away_abbrev]['losses'] += 1
                        
                        self.pool_standings[pool_name][away_abbrev]['runs_for'] += away_score
                        self.pool_standings[pool_name][away_abbrev]['runs_against'] += home_score
                        self.pool_standings[pool_name][home_abbrev]['runs_for'] += home_score
                        self.pool_standings[pool_name][home_abbrev]['runs_against'] += away_score
                        
                        if verbose:
                            winner = away_abbrev if away_score > home_score else home_abbrev
                            print(f"  {away_abbrev} {away_score:2} @ {home_abbrev} {home_score:2}  ({GREEN}{winner}{RESET})")
        
        # Display pool standings
        self._display_pool_standings()
        
        # Determine advancing teams
        advancing_teams = []
        pool_winners = []
        wild_card_candidates = []
        
        # Get top teams from each pool
        for pool_name, pool_teams in self.pools.items():
            sorted_teams = self._sort_pool_teams(pool_name)
            
            # Pool winners/qualifiers
            for i in range(self.advance_per_pool):
                team = sorted_teams[i]
                advancing_teams.append(team)
                if i == 0:
                    pool_winners.append(team)
            
            # Remaining teams are wild card candidates
            for i in range(self.advance_per_pool, len(sorted_teams)):
                team = sorted_teams[i]
                wild_card_candidates.append((team, pool_name))
        
        # Select wild cards if configured
        if self.wild_cards > 0:
            # Sort wild card candidates by record across all pools
            wild_card_candidates.sort(
                key=lambda x: (
                    self.pool_standings[x[1]][x[0]]['wins'],
                    self.pool_standings[x[1]][x[0]]['runs_for'] - self.pool_standings[x[1]][x[0]]['runs_against']
                ),
                reverse=True
            )
            
            print(f"\n{BOLD}{YELLOW}Wild Card Selection:{RESET}")
            for i in range(min(self.wild_cards, len(wild_card_candidates))):
                wc_team, wc_pool = wild_card_candidates[i]
                advancing_teams.append(wc_team)
                stats = self.pool_standings[wc_pool][wc_team]
                print(f"  Wild Card #{i+1}: {wc_team} ({wc_pool}) - {stats['wins']}-{stats['losses']}")
        
        print(f"\n{BOLD}{GREEN}Teams Advancing to Bracket:{RESET}")
        for i, team in enumerate(advancing_teams, 1):
            print(f"  #{i} {team}")
        print()
        
        return advancing_teams
    
    def _sort_pool_teams(self, pool_name: str) -> List[str]:
        """Sort teams in a pool by wins, then run differential."""
        pool_teams = self.pools[pool_name]
        return sorted(
            pool_teams,
            key=lambda t: (
                self.pool_standings[pool_name][t]['wins'],
                self.pool_standings[pool_name][t]['runs_for'] - self.pool_standings[pool_name][t]['runs_against']
            ),
            reverse=True
        )
    
    def _display_pool_standings(self):
        """Display standings for each pool."""
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  POOL PLAY STANDINGS{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        for pool_name, pool_teams in self.pools.items():
            print(f"{BOLD}{CYAN}{pool_name}{RESET}")
            print(f"  {'Team':<8} {'W':>3} {'L':>3} {'RF':>4} {'RA':>4} {'Diff':>5}")
            print(f"  {'-'*36}")
            
            sorted_teams = self._sort_pool_teams(pool_name)
            
            for i, team in enumerate(sorted_teams, 1):
                stats = self.pool_standings[pool_name][team]
                diff = stats['runs_for'] - stats['runs_against']
                color = GREEN if i <= self.advance_per_pool else WHITE
                print(f"  {color}{i}. {team:<6} {stats['wins']:>3} {stats['losses']:>3} "
                      f"{stats['runs_for']:>4} {stats['runs_against']:>4} {diff:>+5}{RESET}")
            print()
    
    def simulate_bracket(self, teams: List[str], verbose: bool = True) -> str:
        """
        Simulate bracket stage.
        
        Args:
            teams: List of teams in seeding order
            
        Returns:
            Champion team abbreviation
        """
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  BRACKET STAGE{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        active_teams = list(teams)
        original_seeds = {team: i+1 for i, team in enumerate(teams)}
        
        for round_num, round_config in enumerate(self.bracket_rounds):
            round_name = round_config['name']
            
            # Create matchups
            matchups = []
            num_matchups = len(active_teams) // 2
            for i in range(num_matchups):
                higher_seed_team = active_teams[i]
                lower_seed_team = active_teams[-(i+1)]
                matchups.append((higher_seed_team, lower_seed_team))
            
            # Simulate series
            round_winners = []
            for higher_seed_team, lower_seed_team in matchups:
                winner = self._simulate_series(
                    higher_seed_team, lower_seed_team, round_config, round_name, verbose
                )
                round_winners.append(winner)
            
            active_teams = round_winners
            active_teams.sort(key=lambda t: original_seeds[t])
        
        champion = active_teams[0]
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}{GREEN}  🏆 CHAMPION: {champion} 🏆{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        return champion
    
    def _simulate_series(self, higher_seed: str, lower_seed: str, 
                        round_config: Dict, round_name: str, verbose: bool = True) -> str:
        """Simulate a playoff series."""
        games_to_win = round_config['wins_needed']
        home_field_games = round_config['home_field_games']
        
        if verbose:
            print(f"\n{BOLD}{round_name}: {higher_seed} vs {lower_seed}{RESET}")
        
        higher_team = self._get_team(higher_seed)
        lower_team = self._get_team(lower_seed)
        
        higher_wins = 0
        lower_wins = 0
        game_num = 1
        
        while higher_wins < games_to_win and lower_wins < games_to_win:
            is_higher_seed_home = game_num in home_field_games
            home_team = higher_team if is_higher_seed_home else lower_team
            away_team = lower_team if is_higher_seed_home else higher_team
            home_abbrev = higher_seed if is_higher_seed_home else lower_seed
            away_abbrev = lower_seed if is_higher_seed_home else higher_seed
            
            away_score, home_score = play_game(away_team, home_team)
            
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
                print(f"  Game {game_num}: {away_abbrev} {away_score:2} @ {home_abbrev} {home_score:2}  ({GREEN}{winner}{RESET})")
            
            game_num += 1
        
        winner = higher_seed if higher_wins == games_to_win else lower_seed
        if verbose:
            print(f"  {BOLD}{GREEN}{winner} wins series {max(higher_wins, lower_wins)}-{min(higher_wins, lower_wins)}{RESET}\n")
        
        return winner
    
    def simulate(self, verbose: bool = True) -> str:
        """
        Simulate complete pool play playoff.
        
        Returns:
            Champion team abbreviation
        """
        # Pool play stage
        advancing_teams = self.simulate_pool_play(verbose)
        
        # Bracket stage
        champion = self.simulate_bracket(advancing_teams, verbose)
        
        return champion

import csv
import time
from collections import defaultdict
from GAMEDAY import play_game, load_game_data, load_team
from UTILITIES.FILE_PATHS import TEAM_META
from UTILITIES.COLOR_CODES import *

class SeasonSimulator:
    def __init__(self, schedule_csv: str):
        """
        Initialize season simulator with schedule CSV file.
        
        Args:
            schedule_csv: Path to CSV file containing game schedule
                         Expected columns: date, away_team, home_team
        """
        self.schedule_csv = schedule_csv
        self.schedule = []
        self.standings = defaultdict(lambda: {'wins': 0, 'losses': 0, 'runs_scored': 0, 'runs_allowed': 0})
        self.game_results = []
        self.teams_cache = {}  # Cache loaded teams for reuse
        self._initialized = False
        
        self._load_schedule()
        self._load_team_info()
    
    def _load_team_info(self):
        """Load team information from TEAM_META.csv"""
        self.team_info = {}
        with open(TEAM_META, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                abbrev = row['team_abbrev']
                self.team_info[abbrev] = {
                    'market': row['market'],
                    'name': row['team_name'],
                    'league': row['league']
                }
    
    def _load_schedule(self):
        """Load schedule from CSV file"""
        try:
            with open(self.schedule_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.schedule.append({
                        'date': row.get('date', ''),
                        'away_team': row['away_team'].strip().upper(),
                        'home_team': row['home_team'].strip().upper()
                    })
            print(f"{GREEN}✓{RESET} Loaded {len(self.schedule)} games from schedule")
        except FileNotFoundError:
            print(f"{RED}✗{RESET} Schedule file not found: {self.schedule_csv}")
            raise
        except KeyError as e:
            print(f"{RED}✗{RESET} Missing required column in schedule CSV: {e}")
            raise
    
    def _get_team(self, team_abbrev: str):
        """Get team from cache or load if not cached."""
        if team_abbrev not in self.teams_cache:
            self.teams_cache[team_abbrev] = load_team(team_abbrev)
        return self.teams_cache[team_abbrev]
    
    def simulate_game(self, game_num: int, away_abbrev: str, home_abbrev: str, show_score: bool = True):
        """ Simulate a single game and update standings. """
        try:
            # Get teams (from cache if already loaded)
            away_team = self._get_team(away_abbrev)
            home_team = self._get_team(home_abbrev)
            
            away_score, home_score = play_game(away_team, home_team)
            
            # Update standings
            if away_score > home_score:
                self.standings[away_abbrev]['wins'] += 1
                self.standings[home_abbrev]['losses'] += 1
            else:
                self.standings[home_abbrev]['wins'] += 1
                self.standings[away_abbrev]['losses'] += 1
            
            # Update run differentials
            self.standings[away_abbrev]['runs_scored'] += away_score
            self.standings[away_abbrev]['runs_allowed'] += home_score
            self.standings[home_abbrev]['runs_scored'] += home_score
            self.standings[home_abbrev]['runs_allowed'] += away_score
            
            # Store result
            result = {
                'game_num': game_num,
                'away_team': away_abbrev,
                'home_team': home_abbrev,
                'away_score': away_score,
                'home_score': home_score
            }
            self.game_results.append(result)
            
            if show_score:
                winner_color = GREEN if away_score > home_score else CYAN
                loser_color = CYAN if away_score > home_score else GREEN
                print(f"Game {game_num:3}: {loser_color if away_score > home_score else winner_color}{away_abbrev} {away_score:2}{RESET} @ "
                      f"{loser_color if home_score > away_score else winner_color}{home_abbrev} {home_score:2}{RESET}")
            
            return away_score, home_score
            
        except Exception as e:
            print(f"{RED}✗{RESET} Error simulating {away_abbrev} @ {home_abbrev}: {e}")
            raise
    
    def simulate_season(self, verbose: bool = True, show_progress: bool = True):
        """
        Simulate entire season from schedule.
        
        Args:
            verbose: Print each game result
            show_progress: Show progress updates every N games
        """
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  SEASON SIMULATION - {len(self.schedule)} Games{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        # Initialize game data once for the entire season
        if not self._initialized:
            print(f"{YELLOW}Initializing game data (caches, league context)...{RESET}")
            init_time = time.time()
            load_game_data()
            self._initialized = True
            print(f"{GREEN}✓{RESET} Initialized in {time.time() - init_time:.3f}s\n")
        
        start_time = time.time()
        
        for i, game in enumerate(self.schedule, 1):
            away_team = game['away_team']
            home_team = game['home_team']
            
            # Show progress periodically
            if show_progress and i % 100 == 0:
                elapsed = time.time() - start_time
                games_per_sec = i / elapsed if elapsed > 0 else 0
                print(f"\n{YELLOW}--- Progress: {i}/{len(self.schedule)} games ({games_per_sec:.1f} games/sec) ---{RESET}\n")
            
            self.simulate_game(i, away_team, home_team, show_score=verbose)
        
        elapsed = time.time() - start_time
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{GREEN}✓{RESET} Season simulation complete!")
        print(f"  Total time: {elapsed:.2f} seconds ({len(self.schedule)/elapsed:.2f} games/sec)")
        print(f"{BOLD}{'='*60}{RESET}\n")  # Extra newlines for spacing
    
    def export_results(self, output_csv: str):
        """
        Export game results to CSV file.
        
        Args:
            output_csv: Path to output CSV file
        """
        try:
            with open(output_csv, 'w', newline='') as f:
                fieldnames = ['game_num', 'away_team', 'home_team', 'away_score', 'home_score']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.game_results)
            print(f"{GREEN}✓{RESET} Results exported to {output_csv}")
        except Exception as e:
            print(f"{RED}✗{RESET} Error exporting results: {e}")


def main():
    """Main entry point for season simulation"""
    # Example usage - modify schedule path as needed
    schedule_file = "GAME_DATA\\SCHEDULE.csv"
    
    # Create simulator
    sim = SeasonSimulator(schedule_csv=schedule_file)
    
    # Simulate season
    sim.simulate_season(verbose=True, show_progress=True)
    
    # Export results
    sim.export_results("GAME_DATA\\RESULTS.csv")

if __name__ == "__main__":
    main()

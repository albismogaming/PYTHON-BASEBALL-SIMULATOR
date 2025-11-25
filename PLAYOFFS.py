import time
from typing import List, Optional
from GAMEDAY import load_game_data
from UTILITIES.COLOR_CODES import *
from PLAYOFFS.PLAYOFF_FACTORY import PlayoffFactory
from PLAYOFFS.PLAYOFF_CONFIG import PLAYOFF_FORMATS, ACTIVE_FORMAT


class PlayoffSimulator:
    def __init__(self, teams: List[str], format_name: Optional[str] = None):
        """
        Initialize playoff simulator with seeded teams.
        
        Args:
            teams: List of teams in seeding order
            format_name: Playoff format to use (uses ACTIVE_FORMAT if None)
        """
        self.format_name = format_name or ACTIVE_FORMAT
        self.config = PLAYOFF_FORMATS[self.format_name]
        
        if len(teams) != self.config['num_teams']:
            raise ValueError(f"Format '{self.format_name}' requires {self.config['num_teams']} teams, got {len(teams)}")
        
        self.teams = teams
        self._initialized = False
        
        # Create the appropriate playoff simulator based on format
        self.playoff_simulator = PlayoffFactory.create_playoff(teams, self.format_name)
    
    def simulate_playoffs(self, verbose: bool = True) -> str:
        """
        Simulate complete playoffs using the configured format.
        
        Returns:
            Champion team abbreviation
        """
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  {self.format_name.replace('_', ' ').upper()} PLAYOFFS{RESET}")
        print(f"{BOLD}  Format: {self.config.get('type', 'standard')}{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        # Delegate to the specific playoff simulator
        champion = self.playoff_simulator.simulate(verbose=verbose)
        
        return champion
    
    def run_playoffs(self, verbose: bool = True):
        """
        Initialize game data and run complete playoffs.
        
        Returns:
            Champion team abbreviation
        """
        # Initialize game data once
        if not self._initialized:
            print(f"{YELLOW}Initializing game data...{RESET}")
            init_time = time.time()
            load_game_data()
            self._initialized = True
            print(f"{GREEN}✓{RESET} Initialized in {time.time() - init_time:.3f}s\n")
        
        start_time = time.time()
        champion = self.simulate_playoffs(verbose=verbose)
        elapsed = time.time() - start_time
        
        print(f"\n{GREEN}✓{RESET} Playoffs completed in {elapsed:.2f} seconds\n")
        
        return champion


def main():
    """Example playoff simulation"""
    # Define playoff teams in seeding order (1-6)
    playoff_teams = [
        "LAP",  # #1 seed
        "NYC",  # #2 seed
        "SDT",  # #3 seed
        "SFN",  # #4 seed
        "BKN",  # #5 seed
        "PIT",  # #6 seed
    ]
    
    # Run playoffs
    sim = PlayoffSimulator(playoff_teams, format_name='GAUNTLET_6')
    champion = sim.run_playoffs(verbose=True)
    
    print(f"WORLD SERIES CHAMPION: {champion}")

if __name__ == "__main__":
    main()

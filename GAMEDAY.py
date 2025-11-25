import time
from DATA_LOADERS.TEAM_LOADER import TeamLoader
from DATA_LOADERS.LEAGUE_STATS_LOADER import LeagueLoader
from GAME_LOGIC.GAMESTATE import GameState
from TEAM_UTILS.LINEUP_MANAGER import LineupManager
from TEAM_UTILS.PITCHING_MANAGER import PitchingManager
from ATBAT.ATBAT_SIM import AtBatSimulator
from TEAM_UTILS.STATS_MANAGER import StatsManager
from UTILITIES.FUNCTIONS import *
from UTILITIES.FILE_PATHS import TEAM_META, LEAGUE_DATA, ALL_TEAM_PATH
from UTILITIES.RANDOM import init_random_pool


def setup_managers(team):
    lineup_mgr = LineupManager(team.batters)
    pitching_mgr = PitchingManager(team.pitchers)
    
    # Select starting pitcher
    pitching_mgr.select_starting_pitcher(randomize=True)
    
    # Set lineup (can be manual or automatic)
    lineup_mgr.select_lineup()
    
    return lineup_mgr, pitching_mgr


def simulate_half_inning(gamestate, batting_lineup, pitching_mgr):
    """ Simulate one half-inning (3 outs). """
    # Reset half-inning state
    gamestate.reset_half_inning()
    
    while gamestate.outs < 3:
        # Get current batter and pitcher, calculate base probabilities
        batter, pitcher, base_probs = AtBatSimulator.step_initialize_matchup(batting_lineup, pitching_mgr)
        # Simulate the at-bat (apply modifiers, determine outcome, execute)
        AtBatSimulator.simulate_at_bat(gamestate, batter, pitcher, base_probs)
        # Advance to next batter
        AtBatSimulator.step_advance_batter(batting_lineup)
        # Check if pitcher should be changed (after at-bat, before next batter faces them)
        if pitching_mgr.should_change_pitcher():
            pitching_mgr.change_pitcher()


def simulate_inning(gamestate, away_team, home_team, away_lineup, away_pitching, home_lineup, home_pitching):
    """ Simulate one full inning (top and bottom). """
    # Top of inning (away team bats)
    simulate_half_inning(gamestate, away_lineup, home_pitching)
    
    # Check if game can end (home team ahead in 9th+, skip bottom half)
    if gamestate.can_game_end():
        return
    
    # Bottom of inning (home team bats)
    gamestate.toggle_inning_half()
    simulate_half_inning(gamestate, home_lineup, away_pitching)
    
    # Check if game ended (walk-off or away team ahead after bottom of 9th+)
    if gamestate.can_game_end():
        return
    
    # Advance to next inning if game continues
    gamestate.reset_inning()

def play_game(away_team, home_team):
    """ Simulate a single game between two teams. """

    # Initialize game state
    gamestate = GameState(away_team, home_team)
    
    # Setup managers for both teams
    away_lineup, away_pitching = setup_managers(away_team)
    home_lineup, home_pitching = setup_managers(home_team)

    # Main game loop - simulate 9 innings (or more for extras)
    while not gamestate.is_game_over:
        simulate_inning(
            gamestate, away_team, home_team,
            away_lineup, away_pitching,
            home_lineup, home_pitching
        )
    
    return gamestate.stats["away_team"]["score"], gamestate.stats["home_team"]["score"]


def load_game_data():
    """ Initialize all game data (player cache, league context, random pool). Call this once before running games. """   
    init_random_pool(size=500)
    
    # Load all players from ALL_TEAMS.csv
    TeamLoader.initialize_player_cache(ALL_TEAM_PATH)
    LeagueLoader.load_league_data(LEAGUE_DATA, 2025)


def load_team(team_abbrev: str):
    """ Load a single team from the player cache. """   
    if not TeamLoader._cache_initialized:
        raise RuntimeError("Player cache not initialized. Call load_game_data() first.")
    
    return TeamLoader.load_team_from_cache(team_abbrev=team_abbrev, teams_csv=TEAM_META)


if __name__ == "__main__":
    # Load game data once (caches, league context, etc.)
    print("Loading game data...")
    load_game_data()
    
    # Load teams
    away_abbrev = "PIT"
    home_abbrev = "WAS"
    
    print(f"Loading teams: {away_abbrev} @ {home_abbrev}")
    away_team = load_team(away_abbrev)
    home_team = load_team(home_abbrev)
    
    # Simulate game
    start_time = time.time()

    away_score, home_score = play_game(away_team, home_team)
    print(f"{away_abbrev} {away_score:2} - {home_abbrev} {home_score:2}")
    
    elapsed = time.time() - start_time
    print(f"\nGame simulated in {elapsed:.7f} seconds")
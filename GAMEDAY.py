import time
from DATA_LOADERS.TEAM_LOADER import TeamLoader
from DATA_LOADERS.LEAGUE_STATS_LOADER import LeagueLoader
from GAME_LOGIC.GAMESTATE import GameState
from TEAM_UTILS.LINEUP_MANAGER import LineupManager
from TEAM_UTILS.PITCHING_MANAGER import PitchingManager
from ATBAT.ATBAT_SIM import AtBatSimulator
from UTILITIES.ENUMS import InningHalf
from UTILITIES.SCOREBOARD import Scoreboard
from UTILITIES.COLOR_CODES import *
from UTILITIES.FUNCTIONS import *
from UTILITIES.FILE_PATHS import TEAM_PATH, LEAGUE_DATA


def load_teams(away_abbrev: str, home_abbrev: str):
    print(f"\nLoading {away_abbrev} roster...")
    away_team = TeamLoader.load_full_team(
        team_abbrev=away_abbrev,
        roster_csv=f"{TEAM_PATH}\\{away_abbrev}.csv",
        teams_csv=f"{TEAM_PATH}\\TEAM_META.csv"
    )
    
    print(f"Loading {home_abbrev} roster...")
    home_team = TeamLoader.load_full_team(
        team_abbrev=home_abbrev,
        roster_csv=f"{TEAM_PATH}\\{home_abbrev}.csv",
        teams_csv=f"{TEAM_PATH}\\TEAM_META.csv"
    )
    
    return away_team, home_team


def setup_managers(team):
    lineup_mgr = LineupManager(team.batters)
    pitching_mgr = PitchingManager(team.pitchers)
    
    # Select starting pitcher
    starter = pitching_mgr.select_starting_pitcher(randomize=True)
    print(f"{team.abbreviation} Starting Pitcher: {starter.full_name}")
    
    # Set lineup (can be manual or automatic)
    lineup_mgr.select_lineup()
    print(f"{team.abbreviation} Lineup set")
    
    return lineup_mgr, pitching_mgr


def simulate_half_inning(gamestate, batting_lineup, pitching_mgr, league_context):
    """
    Simulate one half-inning (3 outs).
    
    Args:
        gamestate: GameState object
        batting_lineup: LineupManager for batting team
        pitching_mgr: PitchingManager for pitching team
        league_context: League context with factors
    """
    # Reset half-inning state
    gamestate.reset_half_inning()
    
    while gamestate.outs < 3:
        # Get current batter and pitcher
        batter, pitcher = AtBatSimulator.step_initialize_matchup(batting_lineup, pitching_mgr)
        
        Scoreboard.scoreboard(gamestate)

        print(f"\n{batter.full_name} vs {pitcher.full_name}")
        
        # Generate matchup token
        matchup_token = AtBatSimulator.step_generate_token(
            batter=batter,
            pitcher=pitcher,
            league=league_context,
            gamestate=gamestate
        )
        
        # Generate outcome, pitches, and hit info
        outcome, pitches, hit_info = AtBatSimulator.step_generate_outcome(matchup_token)
        
        print(f"  → {outcome.value} ({' '.join(pitches)})")
        
        # Check for fielding error on balls in play (only FO, GO, LO, PO)
        is_error = AtBatSimulator.step_check_for_error(outcome, hit_info, gamestate)
        
        # Execute outcome
        play_context = AtBatSimulator.step_execute_outcome(
            outcome=outcome,
            gamestate=gamestate,
            batter=batter,
            pitcher=pitcher,
            matchup_token=matchup_token,
            hit_info=hit_info,
            is_error=is_error
        )
        
        # Advance to next batter
        AtBatSimulator.step_advance_batter(play_context, batting_lineup)
    
    # print(f"\nEnd of half-inning: {gamestate.outs} outs")


def simulate_inning(gamestate, away_team, home_team,
                   away_lineup, away_pitching,
                   home_lineup, home_pitching,
                   league_context):
    """
    Simulate one full inning (top and bottom).
    
    Args:
        gamestate: GameState object
        away_team, home_team: Team objects
        away_lineup, home_lineup: LineupManagers
        away_pitching, home_pitching: PitchingManagers
        league_context: League context
    """
    Scoreboard.inning_start(gamestate, InningHalf.TOP)
    
    simulate_half_inning(gamestate, away_lineup, home_pitching, league_context)
    
    # Show scoreboard after top half
    Scoreboard.scoreboard(gamestate)
    
    # Check if home team can skip bottom half (already winning in 9th+)
    if gamestate.current_inning >= 9:
        if gamestate.stats['home_team']['score'] > gamestate.stats['away_team']['score']:
            print(f"\n🏆 GAME OVER! {home_team.full_name} wins!")
            gamestate.is_game_over = True
            return
    

    gamestate.toggle_inning_half()
    Scoreboard.inning_start(gamestate, InningHalf.BOT)
    simulate_half_inning(gamestate, home_lineup, away_pitching, league_context)
    
    # Show scoreboard after bottom half
    Scoreboard.scoreboard(gamestate)
    
    # Check for walk-off or regulation end after bottom of 9th+
    if gamestate.current_inning >= 9:
        home_score = gamestate.stats['home_team']['score']
        away_score = gamestate.stats['away_team']['score']
        
        if home_score > away_score:
            print(f"\n🏆 WALK-OFF! {home_team.full_name} wins!")
            gamestate.is_game_over = True
            return
        elif away_score > home_score:
            print(f"\n🏆 GAME OVER! {away_team.full_name} wins!")
            gamestate.is_game_over = True
            return
        # Tied - continue to extra innings
    
    # Advance to next inning
    gamestate.reset_inning()


def play_game(away_abbrev: str = "NYY", home_abbrev: str = "LAD"):
    """
    Main game simulation function - simulates a full 9-inning game.
    
    Args:
        away_abbrev: Away team abbreviation
        home_abbrev: Home team abbreviation
    """
    print(rgb_colored("⚾ BASEBALL SIMULATOR 2025 ⚾", GOLD))
    print()
    
    # Load teams
    away_team, home_team = load_teams(away_abbrev, home_abbrev)
    
    # Load league context (park factors, etc.)
    league_context = LeagueLoader.load_league_data(LEAGUE_DATA, 2025)
    
    # Initialize game state
    gamestate = GameState(away_team, home_team)
    
    # Setup managers for both teams
    print(f"\n{away_team.full_name} Setup:")
    away_lineup, away_pitching = setup_managers(away_team)
    
    print(f"\n{home_team.full_name} Setup:")
    home_lineup, home_pitching = setup_managers(home_team)
    
    print("\nPLAY BALL!")
    
    # Main game loop - simulate 9 innings (or more for extras)
    while not gamestate.is_game_over:
        simulate_inning(
            gamestate, away_team, home_team,
            away_lineup, away_pitching,
            home_lineup, home_pitching,
            league_context
        )
        
    Scoreboard.boxscore(gamestate)

if __name__ == "__main__":
    start_time = time.time()
    
    # Run full game simulation
    play_game(away_abbrev="NYY", home_abbrev="LAD")
    
    elapsed = time.time() - start_time
    print(f"\nGame simulated in {elapsed:.4f} seconds")
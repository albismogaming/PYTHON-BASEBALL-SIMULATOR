from ATBAT.ATBAT_SIM import AtBatSimulator
from ATBAT.ATBAT_FACTORY import AtBatFactory
from TEAM_UTILS.STATS_MANAGER import StatsManager
from UTILITIES.ENUMS import EventType, Pitch
from UTILITIES.SCOREBOARD import Scoreboard

def simulate_half_inning(gamestate, batting_lineup, pitching_mgr):
    gamestate.reset_half_inning()
    # Scoreboard.inning_start(gamestate, gamestate.inninghalf)

    while gamestate.outs < 3:
        token = AtBatSimulator.initialize_matchup(batting_lineup, pitching_mgr)
        atbat = AtBatSimulator.simulate_at_bat(gamestate, token)

        for event in atbat.events:
            # print(event)
            
            # Handle event based on type
            match event.event_type:
                case EventType.PITCH:
                    StatsManager.record_pitch(token.pitcher)
                    if event.event_code != Pitch.IP:
                        result = AtBatFactory.execute_event(event.event_code, gamestate, token)
                        gamestate.apply_result(result)
                
                case EventType.MICRO | EventType.OTHER:
                    result = AtBatFactory.execute_event(event.event_code, gamestate, token)
                    # print(result.bases_before, result.bases_after)
                    gamestate.apply_result(result)
                
                    # Record the at-bat stats
                    StatsManager.record_at_bat(result=result)
        
                case EventType.MACRO:
                    result = AtBatFactory.execute_event(event.event_code, gamestate, token)
                    # print(result.bases_before, result.bases_after)
                    gamestate.apply_result(result)
                    
                    # Record the at-bat stats
                    StatsManager.record_at_bat(result=result)


            # Check if action or half-inning should end
            end_half_inning, break_atbat = gamestate.should_end(event.event_type == EventType.MACRO)
            if end_half_inning:
                return
            if break_atbat:
                break

        # Display updated scoreboard after at-bat
        # Scoreboard.scoreboard(gamestate)
        
        # Check if game ended during the at-bat
        if gamestate.can_game_end():
            return

        # Reset count and advance to next batter only if at-bat completed
        gamestate.reset_count()
        AtBatSimulator.advance_next_batter(batting_lineup)

        if pitching_mgr.should_change_pitcher():
            pitching_mgr.change_pitcher()


def simulate_inning(gamestate, away_team, home_team, away_lineup, away_pitching, home_lineup, home_pitching):
    """ Simulate one full inning (top and bottom). """
    # Top of inning (away team bats)
    simulate_half_inning(gamestate, away_lineup, home_pitching)
    
    if gamestate.can_game_end():
        return

    # Bottom of inning (home team bats)
    gamestate.toggle_inning_half()
    
    simulate_half_inning(gamestate, home_lineup, away_pitching)
    
    if gamestate.can_game_end():
        return

    # Advance to next inning if game continues
    gamestate.reset_inning()

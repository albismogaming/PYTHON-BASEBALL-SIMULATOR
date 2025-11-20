from OUTCOME_ENGINE.OUTCOME_TOKEN import MatchupTokenGenerator
from OUTCOME_ENGINE.OUTCOME_GENERATOR import OutcomeGenerator
from OUTCOME_ENGINE.OUTCOME_FACTORY import OutcomeFactory
from ATBAT.ATBAT_PITCHES import PitchCountGenerator
from TEAM_UTILS.STATS_MANAGER import StatsManager
from UTILITIES.ENUMS import Outcome

class AtBatSimulator:
    """
    Step-by-step at-bat simulation with stateless methods.
    Each step receives input and returns output - no internal state.
    """
    @staticmethod
    def step_initialize_matchup(batting_lineup_mgr, pitching_team_mgr):
        """
        Get the current batter and pitcher for the matchup.
        """
        batter = batting_lineup_mgr.get_current_batter()
        pitcher = pitching_team_mgr.get_current_pitcher()

        return batter, pitcher

    @staticmethod
    def simulate_at_bat(gamestate, batter, pitcher):
        """ Simulate a complete at-bat: generate probabilities, determine outcome, and execute it. """

        # Generate matchup probabilities
        outcome_probs, babip_prob = MatchupTokenGenerator.generate_token(gamestate, batter, pitcher)
        
        # Determine outcome from probabilities
        outcome = OutcomeGenerator.generate_final_outcome(outcome_probs, babip_prob)
        
        # Generate pitch count for the outcome
        pitches_thrown = PitchCountGenerator.generate_pitches_thrown(outcome)
        
        # Execute outcome and get result data
        result = OutcomeFactory.execute_outcome(outcome=outcome, gamestate=gamestate, batter=batter, pitcher=pitcher)
        
        # Update game state with the result
        gamestate.add_stats(hits=result.get('hits', 0), runs=result.get('runs', 0), outs=result.get('outs', 0))
        
        # Record stats using the outcome data
        runs_scored = 1 if outcome == Outcome.HR else 0  # Only batter scores on HR
        StatsManager.record_at_bat(batter, pitcher, outcome, pitches_thrown, runs_scored, result['rbis'])
    
    @staticmethod
    def step_advance_batter(batting_lineup_mgr):
        """ Step 5: Advance to the next batter in the lineup. """       
        batting_lineup_mgr.get_next_batter()
        
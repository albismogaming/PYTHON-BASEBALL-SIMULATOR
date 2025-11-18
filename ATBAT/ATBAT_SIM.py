from ATBAT.GEN_PIT_SEQ import PitchSequenceGenerator
from OUTCOME_ENGINE.OUTCOME_TOKEN import MatchupTokenGenerator
from OUTCOME_ENGINE.OUTCOME_GENERATOR import OutcomeGenerator
from ATBAT.HIT_ENGINE import HitEngine
from OUTCOME_ENGINE.OUTCOME_FACTORY import OutcomeFactory
from UTILITIES.ENUMS import HitTypes, Outcome
import random

class AtBatSimulator:
    """
    Step-by-step at-bat simulation with stateless methods.
    Each step receives input and returns output - no internal state.
    """
    @staticmethod
    def step_initialize_matchup(batting_lineup_mgr, pitching_team_mgr):
        """
        Get the current batter and pitcher for the matchup.
        
        Args:
            batting_lineup_mgr: LineupManager for the batting team
            pitching_team_mgr: TeamManager or PitchingManager for the pitching team
            
        Returns:
            Tuple of (batter, pitcher) Player objects
        """
        batter = batting_lineup_mgr.get_current_batter()
        pitcher = pitching_team_mgr.get_current_pitcher()

        return batter, pitcher

    @staticmethod
    def step_generate_token(batter, pitcher, league, gamestate):
        """
        Step 1: Generate matchup token with probabilities.
        
        Args:
            batter: Batter PlayerContext
            pitcher: Pitcher PlayerContext
            gamestate: Current GameState
            
        Returns:
            MatchupToken with all probabilities
        """
        matchup_token = MatchupTokenGenerator.generate_token(
            batter, pitcher, league, gamestate
        )
        return matchup_token
        
    @staticmethod
    def step_generate_outcome(matchup_token):
        """
        Step 2: Determine outcome from token probabilities.
        
        Args:
            matchup_token: MatchupToken from step 1
            
        Returns:
            Tuple of (outcome, pitches, hit_info)
            - outcome: Outcome enum (SO, BB, HR, SL, GO, etc.)
            - pitches: List of pitch codes
            - hit_info: HitInfo object or None if not a ball in play
        """
        outcome = OutcomeGenerator.generate_final_outcome(matchup_token)
        pitches = PitchSequenceGenerator.generate_sequence(outcome)
        
        # Only generate hit info for balls put in play
        # SO, BB, HP don't have hit characteristics
        balls_in_play = ['SL', 'DL', 'TL', 'HR', 'GO', 'FO', 'LO', 'PO', 'IH']
        if outcome.name in balls_in_play:
            hit_info = HitEngine.generate_hit_info(outcome, matchup_token.batter)
        else:
            hit_info = None

        return outcome, pitches, hit_info

    @staticmethod
    def step_check_for_error(outcome, hit_info, gamestate):
        """
        Step 3.5: Check if a fielding error occurs on a ball in play.
        
        Args:
            hit_info: HitInfo object with fielder and hit characteristics
            gamestate: GameState to get fielder from team
            
        Returns:
            bool: True if error occurs, False otherwise
        """

        error_possible_outcomes = [Outcome.FO, Outcome.GO, Outcome.LO, Outcome.PO]
        if outcome not in error_possible_outcomes:
            return False
        
        if hit_info is None:
            return False
            
        # Get the fielder who will make the play
        fielder = gamestate.get_fielder(hit_info)
        if not fielder or not hasattr(fielder, 'field'):
            return False
        
        return random.random() > fielder.field

    @staticmethod
    def step_execute_outcome(outcome, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        """
        Step 4: Execute outcome and update game state.
        
        Args:
            outcome: Outcome enum
            gamestate: GameState to update
            batter: Batter PlayerContext
            pitcher: Pitcher PlayerContext
            matchup_token: MatchupToken
            base_runner_mgr: BaseRunnerManager
            hit_info: HitInfo from step 3
            is_error: Whether a fielding error occurred
            
        Returns:
            PlayContext with complete results
        """
        
        play_context = OutcomeFactory.execute_outcome(
            outcome=outcome,
            gamestate=gamestate,
            batter=batter,
            pitcher=pitcher,
            matchup_token=matchup_token,
            hit_info=hit_info,
            is_error=is_error
        )
        return play_context
    
    @staticmethod
    def step_advance_batter(play_context, batting_lineup_mgr):
        """
        Step 5: Advance to the next batter in the lineup.
        
        Args:
            play_context: PlayContext with results of the play
            batting_lineup_mgr: LineupManager for the batting team
        """
        if play_context.at_bat_complete:
            batting_lineup_mgr.get_next_batter()
        
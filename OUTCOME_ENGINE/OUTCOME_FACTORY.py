from UTILITIES.ENUMS import Outcome
from OUTCOME_FILES.STRIKEOUTS import Strikeout
from OUTCOME_FILES.BASEONBALLS import BaseOnBalls
from OUTCOME_FILES.HITBYPITCH import HitByPitch
from OUTCOME_FILES.INFIELDHIT import InfieldHit
from OUTCOME_FILES.SINGLE import Single
from OUTCOME_FILES.DOUBLE import Double
from OUTCOME_FILES.TRIPLE import Triple
from OUTCOME_FILES.HOMERUN import Homerun
from OUTCOME_FILES.GROUNDOUTS import Groundout
from OUTCOME_FILES.FLYOUT import Flyout
from OUTCOME_FILES.LINEOUT import Lineout
from OUTCOME_FILES.POPOUT import Popout


class OutcomeFactory:
    """
    Stateless registry for all outcome executors.
    Maps each outcome enum to its executor class.
    """
    
    # Class-level registry mapping outcomes to their executor classes (not instances)
    _EXECUTORS = {
        # Three True Outcomes
        Outcome.SO: Strikeout,
        Outcome.BB: BaseOnBalls,
        Outcome.HP: HitByPitch,
        
        # Hits
        Outcome.IH: InfieldHit,
        Outcome.SL: Single,
        Outcome.DL: Double,
        Outcome.TL: Triple,
        Outcome.HR: Homerun,
        
        # Outs
        Outcome.GO: Groundout,
        Outcome.FO: Flyout,
        Outcome.LO: Lineout,
        Outcome.PO: Popout,
    }
    
    @staticmethod
    def get_executor(outcome):
        """
        Get the executor class for a specific outcome.
        
        Args:
            outcome: Outcome enum value
            
        Returns:
            Executor class for this outcome
            
        Raises:
            KeyError: If no executor exists for the outcome
        """
        if outcome not in OutcomeFactory._EXECUTORS:
            raise KeyError(f"No executor registered for outcome: {outcome}")
        
        executor_class = OutcomeFactory._EXECUTORS[outcome]
        if executor_class is None:
            raise NotImplementedError(f"Executor for {outcome} not yet implemented")
        
        return executor_class
    
    @staticmethod
    def execute_outcome(outcome, gamestate, batter, pitcher, matchup_token, hit_info=None, is_error=False):
        """
        Execute an outcome using its registered executor.
        
        Args:
            outcome: Outcome enum value
            gamestate: Current game state object
            batter: Batter player object
            pitcher: Pitcher player object
            matchup_token: MatchupToken with context
            base_runner_mgr: BaseRunnerManager for advancing runners
            hit_info: Optional hit location/info (for balls in play)
            is_error: Whether a fielding error occurred on the play
            
        Returns:
            PlayContext from the executor's execute method
        """
        executor_class = OutcomeFactory.get_executor(outcome)
        # Instantiate handler and execute (handlers can be stateless or stateful)
        return executor_class().execute(gamestate, batter, pitcher, matchup_token, hit_info, is_error)
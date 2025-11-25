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


class AtBatFactory:
    """ Stateless registry for all outcome executors. """
    
    # Dictionary mapping - cleaner and more maintainable than if-elif chain
    _EXECUTORS = {
        Outcome.SO: Strikeout(),
        Outcome.BB: BaseOnBalls(),
        Outcome.HP: HitByPitch(),
        Outcome.IH: InfieldHit(),
        Outcome.SL: Single(),
        Outcome.DL: Double(),
        Outcome.TL: Triple(),
        Outcome.HR: Homerun(),
        Outcome.GO: Groundout(),
        Outcome.FO: Flyout(),
        Outcome.LO: Lineout(),
        Outcome.PO: Popout(),
    }
    
    @staticmethod
    def execute_outcome(outcome, gamestate, batter, pitcher):
        """ Execute an outcome using its registered executor. """
        executor = AtBatFactory._EXECUTORS.get(outcome)
        if executor is None:
            raise KeyError(f"No executor registered for outcome: {outcome}")
        return executor.execute(gamestate, batter, pitcher)
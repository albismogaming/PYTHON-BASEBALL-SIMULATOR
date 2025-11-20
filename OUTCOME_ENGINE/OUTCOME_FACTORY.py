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
    Pre-instantiated executors for maximum performance.
    """
    
    # Pre-instantiated executor instances (created once at module load)
    _SO = Strikeout()
    _BB = BaseOnBalls()
    _HP = HitByPitch()
    _IH = InfieldHit()
    _SL = Single()
    _DL = Double()
    _TL = Triple()
    _HR = Homerun()
    _GO = Groundout()
    _FO = Flyout()
    _LO = Lineout()
    _PO = Popout()
    
    @staticmethod
    def execute_outcome(outcome, gamestate, batter, pitcher):
        """ Execute an outcome using its registered executor. """       
        
        # Direct dispatch - faster than dictionary lookup
        if outcome == Outcome.SO:
            return OutcomeFactory._SO.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.BB:
            return OutcomeFactory._BB.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.HP:
            return OutcomeFactory._HP.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.HR:
            return OutcomeFactory._HR.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.IH:
            return OutcomeFactory._IH.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.SL:
            return OutcomeFactory._SL.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.DL:
            return OutcomeFactory._DL.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.TL:
            return OutcomeFactory._TL.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.GO:
            return OutcomeFactory._GO.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.FO:
            return OutcomeFactory._FO.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.LO:
            return OutcomeFactory._LO.execute(gamestate, batter, pitcher)
        elif outcome == Outcome.PO:
            return OutcomeFactory._PO.execute(gamestate, batter, pitcher)
        else:
            raise KeyError(f"No executor registered for outcome: {outcome}")
from OUTCOME_FILES.PICKOFFS import Pickoff1st
from OUTCOME_FILES.STEALING import Stealing
from UTILITIES.ENUMS import Pitch, Micro, Macro
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
from OUTCOME_FILES.BALK import Balk
from OUTCOME_FILES.WILDPITCH import WildPitch
from OUTCOME_FILES.PASSEDBALL import PassedBall
from OUTCOME_FILES.PITCH_BL import PitchBall
from OUTCOME_FILES.PITCH_CS import PitchCalledStrike
from OUTCOME_FILES.PITCH_SW import PitchSwingStrike
from OUTCOME_FILES.PITCH_FL import PitchFoulBall


class AtBatFactory:
    """ Stateless registry for all outcome executors. """
    
    PITCH_EXECUTORS = {
        Pitch.BL: PitchBall(),
        Pitch.CS: PitchCalledStrike(),
        Pitch.SW: PitchSwingStrike(),
        Pitch.FL: PitchFoulBall(),
    }

    MICRO_EXECUTORS = {
        Micro.WP: WildPitch(),
        Micro.PB: PassedBall(),
        Micro.BK: Balk(),
        Micro.SB: Stealing(),
        Micro.P1: Pickoff1st(),
    }

    MACRO_EXECUTORS = {
        Macro.SO: Strikeout(),
        Macro.BB: BaseOnBalls(),
        Macro.HP: HitByPitch(),
        Macro.IH: InfieldHit(),
        Macro.SL: Single(),
        Macro.DL: Double(),
        Macro.TL: Triple(),
        Macro.HR: Homerun(),
        Macro.GO: Groundout(),
        Macro.FO: Flyout(),
        Macro.LO: Lineout(),
        Macro.PO: Popout(),
    }
    
    @classmethod
    def execute_event(cls, code, gamestate, token):
        if code in cls.PITCH_EXECUTORS:
            return cls.PITCH_EXECUTORS[code].execute(gamestate, token)
        if code in cls.MICRO_EXECUTORS:
            return cls.MICRO_EXECUTORS[code].execute(gamestate, token)
        if code in cls.MACRO_EXECUTORS:
            return cls.MACRO_EXECUTORS[code].execute(gamestate, token)

        raise KeyError(f"No executor registered for {code}")
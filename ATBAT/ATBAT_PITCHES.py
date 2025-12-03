import random
from UTILITIES.ENUMS import Pitch, Macro
from UTILITIES.RANDOM import get_random
from typing import Dict, Tuple, List


class PitchEngine:
    OUTCOME_MAP = {
        Macro.SO: "SO",
        Macro.BB: "BB",
        Macro.HP: "HP",
        Macro.IH: "IP",
        Macro.SL: "IP",
        Macro.DL: "IP",
        Macro.TL: "IP",
        Macro.HR: "IP",
        Macro.GO: "IP",
        Macro.FO: "IP",
        Macro.LO: "IP",
        Macro.PO: "IP",
    }

    PITCH_PROBS = {
        "BB": {
            (0,0): {Pitch.BL: 0.45, Pitch.CS: 0.35, Pitch.SW: 0.25, Pitch.FL: 0.05},
            (0,1): {Pitch.BL: 0.45, Pitch.CS: 0.35, Pitch.SW: 0.25, Pitch.FL: 0.05},
            (0,2): {Pitch.BL: 0.85, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.15},
            (1,0): {Pitch.BL: 0.55, Pitch.CS: 0.35, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (1,1): {Pitch.BL: 0.55, Pitch.CS: 0.35, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (1,2): {Pitch.BL: 0.85, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.15},
            (2,0): {Pitch.BL: 0.55, Pitch.CS: 0.35, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (2,1): {Pitch.BL: 0.55, Pitch.CS: 0.35, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (2,2): {Pitch.BL: 0.85, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.15},
            (3,0): {Pitch.BL: 0.65, Pitch.CS: 0.25, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (3,1): {Pitch.BL: 0.65, Pitch.CS: 0.25, Pitch.SW: 0.05, Pitch.FL: 0.05},
            (3,2): {Pitch.BL: 0.85, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.15},
        },
        "SO": {
            (0,0): {Pitch.BL: 0.40, Pitch.CS: 0.30, Pitch.SW: 0.20, Pitch.FL: 0.10},
            (0,1): {Pitch.BL: 0.30, Pitch.CS: 0.30, Pitch.SW: 0.25, Pitch.FL: 0.15},
            (0,2): {Pitch.BL: 0.20, Pitch.CS: 0.25, Pitch.SW: 0.30, Pitch.FL: 0.25},
            (1,0): {Pitch.BL: 0.25, Pitch.CS: 0.30, Pitch.SW: 0.25, Pitch.FL: 0.20},
            (1,1): {Pitch.BL: 0.25, Pitch.CS: 0.30, Pitch.SW: 0.30, Pitch.FL: 0.15},
            (1,2): {Pitch.BL: 0.15, Pitch.CS: 0.30, Pitch.SW: 0.30, Pitch.FL: 0.25},
            (2,0): {Pitch.BL: 0.15, Pitch.CS: 0.35, Pitch.SW: 0.30, Pitch.FL: 0.20},
            (2,1): {Pitch.BL: 0.15, Pitch.CS: 0.35, Pitch.SW: 0.30, Pitch.FL: 0.20},
            (2,2): {Pitch.BL: 0.15, Pitch.CS: 0.30, Pitch.SW: 0.30, Pitch.FL: 0.25},
            (3,0): {Pitch.BL: 0.00, Pitch.CS: 0.75, Pitch.SW: 0.20, Pitch.FL: 0.05},
            (3,1): {Pitch.BL: 0.00, Pitch.CS: 0.40, Pitch.SW: 0.40, Pitch.FL: 0.20},
            (3,2): {Pitch.BL: 0.00, Pitch.CS: 0.35, Pitch.SW: 0.40, Pitch.FL: 0.25},
        },
        "HP": {
            (0,0): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (0,1): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (0,2): {Pitch.BL: 0.65, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.10},
            (1,0): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (1,1): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (1,2): {Pitch.BL: 0.65, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.10},
            (2,0): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (2,1): {Pitch.BL: 0.30, Pitch.CS: 0.25, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (2,2): {Pitch.BL: 0.65, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.10},
            (3,0): {Pitch.BL: 0.00, Pitch.CS: 0.15, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (3,1): {Pitch.BL: 0.00, Pitch.CS: 0.15, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (3,2): {Pitch.BL: 0.00, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.25},
        },
        "IP": {
            (0,0): {Pitch.BL: 0.40, Pitch.CS: 0.30, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (0,1): {Pitch.BL: 0.35, Pitch.CS: 0.25, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (0,2): {Pitch.BL: 0.45, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.20},
            (1,0): {Pitch.BL: 0.35, Pitch.CS: 0.25, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (1,1): {Pitch.BL: 0.35, Pitch.CS: 0.25, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (1,2): {Pitch.BL: 0.45, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.20},
            (2,0): {Pitch.BL: 0.35, Pitch.CS: 0.25, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (2,1): {Pitch.BL: 0.35, Pitch.CS: 0.25, Pitch.SW: 0.10, Pitch.FL: 0.10},
            (2,2): {Pitch.BL: 0.45, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.20},
            (3,0): {Pitch.BL: 0.00, Pitch.CS: 0.75, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (3,1): {Pitch.BL: 0.00, Pitch.CS: 0.55, Pitch.SW: 0.15, Pitch.FL: 0.05},
            (3,2): {Pitch.BL: 0.00, Pitch.CS: 0.00, Pitch.SW: 0.00, Pitch.FL: 0.15},
        }
    }

    @staticmethod
    def choose_pitch(outcome: Macro, balls: int, strikes: int) -> Pitch:
        outcome_group = PitchEngine.OUTCOME_MAP.get(outcome, outcome)
        state = PitchEngine.PITCH_PROBS.get(outcome_group, {}).get((balls, strikes))
        if not state:
            raise ValueError(f"Missing pitch state for {outcome_group} at {balls}-{strikes}")

        # Pick a pitch using the probabilities
        pitch_types, weights = zip(*state.items())
        r = random.random()
        cum = 0
        for p, w in zip(pitch_types, weights):
            cum += w
            if r < cum:
                return p
        return Pitch.IP  # Fallback, should not reach here

    @staticmethod
    def update_count(balls: int, strikes: int, pitch: Pitch) -> Tuple[int, int]:
        if pitch == Pitch.BL:
            balls += 1
        elif pitch in (Pitch.SW, Pitch.CS):
            strikes += 1
        elif pitch == Pitch.FL:
            if strikes < 2:
                strikes += 1
        return balls, strikes

    @staticmethod
    def is_complete(pitch: Pitch, balls: int, strikes: int) -> bool:
        if pitch == Pitch.IP:
            return True  # ball in play / hit
        if balls > 3:
            return True  # walk
        if strikes > 2:
            return True  # strikeout
        return False

    @staticmethod
    def generate_sequence(outcome: Macro) -> List[Pitch]:
        sequence = []
        balls = strikes = 0

        while True:
            pitch = PitchEngine.choose_pitch(outcome, balls, strikes)
            sequence.append(pitch)
            balls, strikes = PitchEngine.update_count(balls, strikes, pitch)
            if PitchEngine.is_complete(pitch, balls, strikes):
                break

        return sequence
    
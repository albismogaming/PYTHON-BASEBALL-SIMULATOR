from UTILITIES.ENUMS import Outcome
from UTILITIES.RANDOM import get_random


class PitchCountGenerator:
    """Generates realistic pitch counts based on at-bat outcomes.

    Stateless generator - returns pitch count based on outcome type and baseball logic.
    Uses fast approximation instead of numpy for maximum performance.
    All methods are static, no instance state needed.
    """

    # Simplified pitch count ranges for different outcomes (min, max)
    PITCH_COUNT_RANGES = {
        Outcome.HP: (1, 3),
        Outcome.BB: (4, 8),
        Outcome.SO: (3, 8),
        Outcome.HR: (1, 4),
        Outcome.TL: (1, 5),
        Outcome.DL: (1, 4),
        Outcome.SL: (1, 4),
        Outcome.IH: (1, 3),
        Outcome.GO: (1, 4),
        Outcome.FO: (1, 4),
        Outcome.LO: (1, 3),
        Outcome.PO: (1, 3),
    }
    
    @staticmethod
    def generate_pitches_thrown(outcome):
        """Generate a realistic pitch count for a given at-bat outcome."""        
        # Get the pitch count range for this outcome
        min_pitches, max_pitches = PitchCountGenerator.PITCH_COUNT_RANGES.get(outcome, (1, 4))
        
        # Fast random selection from range
        return min_pitches + int(get_random() * (max_pitches - min_pitches + 1))
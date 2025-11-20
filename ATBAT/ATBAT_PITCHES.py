from UTILITIES.ENUMS import Outcome
from UTILITIES.DISTRIBUTIONS import triangular
import numpy as np


class PitchCountGenerator:
    """Generates realistic pitch counts based on at-bat outcomes.

    Stateless generator - returns pitch count based on outcome type and baseball logic.
    All methods are static, no instance state needed.
    """

    # Pitch count distributions for different outcomes
    # Format: (min, mode, max) for triangular distribution
    PITCH_COUNT_RANGES = {
        "HP": (1, 1, 12),
        "BB": (4, 6, 12),
        "SO": (3, 5, 12),
        "HR": (1, 3, 12),
        "TL": (2, 4, 12),
        "DL": (1, 4, 12),
        "SL": (1, 3, 12),
        "IH": (1, 2, 12),
        "GO": (1, 3, 12),
        "FO": (1, 3, 12),
        "LO": (1, 2, 12),
        "PO": (1, 3, 12),
        "OUT": (1, 3, 12),
        "CON": (1, 3, 12)
    }
    
    @staticmethod
    def generate_pitches_thrown(outcome):
        """
        Generate a realistic pitch count for a given at-bat outcome.
        
        Uses triangular distribution for natural variation in pitch counts.
        
        Args:
            outcome: The final outcome of the at-bat (Outcome enum or string)
            
        Returns:
            int: Number of pitches in the at-bat (1-12)
        """
        # Convert outcome enum to name string
        outcome_name = outcome.name if hasattr(outcome, 'name') else str(outcome)
        
        # Get the pitch count range for this outcome
        if outcome_name in PitchCountGenerator.PITCH_COUNT_RANGES:
            min_pitches, mode_pitches, max_pitches = PitchCountGenerator.PITCH_COUNT_RANGES[outcome_name]
        else:
            # Default to generic contact range if outcome not found
            min_pitches, mode_pitches, max_pitches = PitchCountGenerator.PITCH_COUNT_RANGES["CONTACT"]
        
        # Use triangular distribution for realistic pitch counts
        # Mode is the most likely value, with tails at min and max
        pitch_count = int(triangular(min_pitches, mode_pitches, max_pitches))
        
        # Ensure pitch count is at least 1
        return max(1, pitch_count)
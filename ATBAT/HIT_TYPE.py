import numpy as np
from UTILITIES.ENUMS import HitTypes, Outcome


class BattedBallTypeGenerator:
    """
    Stateless class for determining the type of batted ball (GB, FB, LD, PU).
    Uses base outcome distributions weighted by batter profile.
    
    Profile weights adjust the tendency toward different batted ball types:
    1 = Contact Hitter (more GB, more LD on hits)
    2 = Power Hitter (more FB on power, standard elsewhere)
    3 = All-Around Hitter (balanced, slight FB tendency)
    4 = Slap Hitter (fewer GB on hits, more FB)
    5 = Power Contact (more LD, less FB than pure power)
    """
    
    @classmethod
    def determine_hit_type(cls, outcome_name: str, batter_profile: int = 3) -> HitTypes:
        """
        Determine the batted ball type using weighted probability distributions.
        
        Args:
            outcome_name: Full outcome name (e.g., 'SINGLE', 'HOMERUN', 'FLYOUT')
            batter_profile: Integer 1-5 representing hitting profile
            
        Returns:
            HitTypes enum (GB, FB, LD, PU)
        """
        
        # Get base probabilities for outcome
        base_probs = cls._get_outcome_distribution(outcome_name)
        
        # Apply profile weights
        weighted_probs = cls._apply_profile_weights(base_probs, batter_profile)
        
        # Normalize to ensure sum = 1.0
        total = sum(weighted_probs)
        final_probs = [p / total for p in weighted_probs]
        
        # Select batted ball type
        hit_types = [HitTypes.GB, HitTypes.FB, HitTypes.LD, HitTypes.PU]
        index = np.random.choice(len(hit_types), p=final_probs)
        result = hit_types[index]
        return result
    
    @classmethod
    def _get_outcome_distribution(cls, outcome_name: str) -> list:
        """
        Get base batted ball type distribution for each outcome.
        Order: [GROUNDBALL, FLYBALL, LINEDRIVE, POPUP]
        """
        outcome_distributions = {
            Outcome.SL.value: [0.470, 0.045, 0.480, 0.005],
            Outcome.DL.value: [0.140, 0.170, 0.690, 0.000],
            Outcome.TL.value: [0.080, 0.360, 0.560, 0.000],
            Outcome.HR.value: [0.000, 0.830, 0.170, 0.000],
            Outcome.GO.value: [1.000, 0.000, 0.000, 0.000],
            Outcome.FO.value: [0.000, 1.000, 0.000, 0.000],
            Outcome.LO.value: [0.000, 0.000, 1.000, 0.000],
            Outcome.PO.value: [0.000, 0.000, 0.000, 1.000]
        }
        return outcome_distributions.get(outcome_name, [0.25, 0.25, 0.25, 0.25])
    
    @classmethod
    def _apply_profile_weights(cls, base_probs: list, batter_profile: int) -> list:
        """
        Apply multiplier weights based on batter profile.
        Adjusts tendency toward GB/FB/LD based on hitter type.
        
        Order: [GROUNDBALL, FLYBALL, LINEDRIVE, POPUP]
        """
        profile_weights = {
            1: [1.05, 0.90, 1.00, 1.00],  # Contact: More GB, fewer FB
            2: [1.02, 1.05, 0.95, 0.80],  # Power: More FB, fewer LD/PU
            3: [1.00, 1.00, 1.00, 1.00],  # All-Around: Balanced (no adjustment)
            4: [0.92, 1.25, 0.88, 1.00],  # Slap: Much more FB, fewer GB/LD
            5: [0.98, 0.85, 1.12, 0.70],  # Power Contact: More LD, fewer FB/PU
        }
        
        weights = profile_weights.get(batter_profile, [1.0, 1.0, 1.0, 1.0])
        return [p * w for p, w in zip(base_probs, weights)]

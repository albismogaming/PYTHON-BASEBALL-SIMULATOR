import numpy as np
from UTILITIES.ENUMS import HitSectors, HitTypes, Outcome


class SprayDirectionGenerator:
    """
    Stateless class for determining spray direction (which sector the ball goes to).
    Uses a base distribution weighted by:
    1. Outcome type (power outcomes pull more)
    2. Batted ball type (GB/FB/LD/PU as multipliers)
    3. Batter profile (hitting approach: opposite, balanced, pull)
    4. Batter handedness (flips probabilities for lefties)
    
    Sector order for probabilities (right-handed batter perspective):
    [LL, LF, LC, CF, RC, RF, RL] = [Pull Line, Pull, Pull-Center, Center, Oppo-Center, Oppo, Oppo Line]
    For left-handed batters, the list is reversed.
    """
    
    @classmethod
    def determine_spray_direction(cls, outcome_name: str, batter_handedness: str, 
                                 hit_type: HitTypes, batter_profile: int = 1) -> HitSectors:
        """
        Determine which sector the ball was hit to using weighted distributions.
        
        Args:
            outcome_name: Full outcome name (e.g., 'SINGLE', 'HOMERUN')
            batter_handedness: 'R' or 'L'
            hit_type: HitTypes enum (GB, FB, LD, PU)
            batter_profile: Integer 1-5 representing hitting approach
                           1 = Extreme pull hitter
                           2 = Pull hitter  
                           3 = Balanced hitter (default)
                           4 = Opposite field tendency
                           5 = Extreme opposite field hitter
            
        Returns:
            HitSectors enum (LL, LF, LC, CF, RC, RF, RL)
        """
        # Get base distribution for outcome
        base_probs = cls._get_outcome_distribution(outcome_name)
        
        # Apply batted ball type weight
        weighted_probs = cls._apply_hit_type_weight(base_probs, hit_type)
        
        # Apply batter profile adjustment
        adjusted_probs = cls._apply_profile_adjustment(weighted_probs, batter_profile)
        
        # Flip for left-handed batters (mirror image)
        if batter_handedness == 'L':
            adjusted_probs = adjusted_probs[::-1]
        
        # Normalize to ensure probabilities sum to 1.0
        total = sum(adjusted_probs)
        final_probs = [p / total for p in adjusted_probs]
        
        # Select sector
        sectors = [HitSectors.LL, HitSectors.LF, HitSectors.LC, HitSectors.CF, HitSectors.RC, HitSectors.RF, HitSectors.RL]
        
        index = np.random.choice(len(sectors), p=final_probs)
        return sectors[index]
    
    @classmethod
    def _get_outcome_distribution(cls, outcome_name: str) -> list:
        """
        Get base spray distribution for outcome type.
        Order: [LL, LF, LC, CF, RC, RF, RL] (right-handed perspective)
        """
        outcome_distributions = {
            Outcome.SL.value: [0.10, 0.15, 0.25, 0.20, 0.15, 0.10, 0.05],      # Balanced, spray hits
            Outcome.DL.value: [0.08, 0.12, 0.28, 0.22, 0.18, 0.09, 0.03],      # Gap tendency
            Outcome.TL.value: [0.03, 0.07, 0.25, 0.30, 0.25, 0.08, 0.02],      # Alleys/gaps
            Outcome.HR.value: [0.15, 0.25, 0.30, 0.15, 0.10, 0.04, 0.01],     # Pull power
            Outcome.GO.value: [0.12, 0.20, 0.28, 0.20, 0.12, 0.06, 0.02],   # Infield spread
            Outcome.FO.value: [0.05, 0.10, 0.25, 0.30, 0.20, 0.08, 0.02],      # Defensive positioning
            Outcome.LO.value: [0.08, 0.15, 0.27, 0.22, 0.18, 0.08, 0.02],     # Direct at fielders
            Outcome.PO.value: [0.10, 0.18, 0.28, 0.22, 0.14, 0.06, 0.02],      # Infield popups
        }
        return outcome_distributions.get(outcome_name, [0.10, 0.15, 0.25, 0.20, 0.15, 0.10, 0.05])
    
    @classmethod
    def _apply_hit_type_weight(cls, base_probs: list, hit_type: HitTypes) -> list:
        """
        Apply multipliers based on batted ball type.
        GB = more pull, FB = more center/oppo, LD = balanced, PU = infield bias
        """
        # Multipliers for [LL, LF, LC, CF, RC, RF, RL]
        type_weights = {
            HitTypes.GB: [1.3, 1.2, 1.1, 0.9, 0.8, 0.7, 0.6],   # Grounders pull more
            HitTypes.FB: [0.7, 0.8, 0.9, 1.2, 1.1, 1.0, 0.8],   # Flyballs to center/oppo
            HitTypes.LD: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],   # Line drives balanced
            HitTypes.PU: [1.1, 1.2, 1.3, 1.1, 1.0, 0.9, 0.8],   # Popups slightly pull
        }
        
        weights = type_weights.get(hit_type, [1.0] * 7)
        return [p * w for p, w in zip(base_probs, weights)]
    
    @classmethod
    def _apply_profile_adjustment(cls, probs: list, batter_profile: int) -> list:
        """
        Adjust probabilities based on batter's spray tendency profile.
        1 = Extreme pull, 3 = Balanced, 5 = Extreme opposite field
        """
        # Multipliers for [LL, LF, LC, CF, RC, RF, RL]
        profile_adjustments = {
            1: [1.8, 1.6, 1.3, 0.8, 0.6, 0.4, 0.3],   # Extreme pull
            2: [1.4, 1.3, 1.2, 0.9, 0.8, 0.6, 0.5],   # Pull
            3: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],   # Balanced (no adjustment)
            4: [0.5, 0.6, 0.8, 0.9, 1.2, 1.3, 1.4],   # Opposite field
            5: [0.3, 0.4, 0.6, 0.8, 1.3, 1.6, 1.8],   # Extreme opposite
        }
        
        adjustments = profile_adjustments.get(batter_profile, [1.0] * 7)
        return [p * adj for p, adj in zip(probs, adjustments)]
    


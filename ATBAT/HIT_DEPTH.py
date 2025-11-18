from UTILITIES.RANDOM import *
from UTILITIES.DISTRIBUTIONS import *
from UTILITIES.ENUMS import HitDepths, HitSectors, HitTypes, Outcome
from typing import Tuple, Union
import numpy as np

class HitDepthGenerator:
    """
    Determines hit depth (SHALLOW, MEDIUM, DEEP, EXTRA DEEP) based on:
    - Outcome type (HR, SINGLE, DOUBLE, etc.)
    - Hit type (GROUNDBALL, FLYBALL, LINEDRIVE, POPUP)
    - Spray sector (center field vs corners)
    """
    
    @staticmethod
    def _get_base_distribution(outcome_name: str, hit_type: HitTypes) -> Tuple[float, float, float]:
        """
        Get base triangular distribution parameters for outcome + hit type combination.
        Returns (left, mode, right) representing depth probability curve.
        """
        base_params = {
            # Homeruns - Always deep/extra deep
            (Outcome.HR.value, HitTypes.FB): (0.70, 0.90, 1.0),
            (Outcome.HR.value, HitTypes.LD): (0.60, 0.85, 1.0),
            
            # Triples - Very deep (mostly gaps)
            (Outcome.TL.value, HitTypes.FB): (0.60, 0.80, 1.0),
            (Outcome.TL.value, HitTypes.LD): (0.50, 0.75, 0.95),
            
            # Doubles - Medium to deep
            (Outcome.DL.value, HitTypes.FB): (0.35, 0.65, 0.90),
            (Outcome.DL.value, HitTypes.LD): (0.30, 0.60, 0.85),
            (Outcome.DL.value, HitTypes.GB): (0.25, 0.50, 0.75),  # Gap grounders
            
            # Singles - Shallow to medium (varies by type)
            (Outcome.SL.value, HitTypes.LD): (0.15, 0.40, 0.65),
            (Outcome.SL.value, HitTypes.GB): (0.05, 0.30, 0.55),
            (Outcome.SL.value, HitTypes.FB): (0.10, 0.25, 0.50),  # Bloopers
            
            # Flyouts - Medium depth routine flies
            (Outcome.FO.value, HitTypes.FB): (0.25, 0.55, 0.85),
            (Outcome.FO.value, HitTypes.LD): (0.15, 0.45, 0.75),
            
            # Lineouts - Shallow to medium (caught on the fly)
            (Outcome.LO.value, HitTypes.LD): (0.10, 0.40, 0.70),
            
            # Groundouts - Shallow (infield)
            (Outcome.GO.value, HitTypes.GB): (0.0, 0.25, 0.50),
            
            # Popouts - Very shallow (infield popups)
            (Outcome.PO.value, HitTypes.PU): (0.0, 0.20, 0.40),
        }
        
        key = (outcome_name, hit_type)
        return base_params.get(key, (0.15, 0.45, 0.75))  # Default: medium tendency
    
    @staticmethod
    def _apply_sector_modifier(depth_value: Union[float, np.ndarray], sector: HitSectors) -> Union[float, np.ndarray]:
        """
        Adjust depth based on spray direction.
        Balls hit to center field tend to be deeper (longer fence distance).
        """
        # Center field hits tend deeper (more room)
        if sector in [HitSectors.CF.value, HitSectors.LC.value, HitSectors.RC.value]:
            return min(1.0, depth_value + 0.05)
        # Down the line hits slightly shallower (shorter fence)
        elif sector in [HitSectors.LL.value, HitSectors.RL.value]:
            return max(0.0, depth_value - 0.05)
        # Left/right field normal
        return depth_value
    
    @staticmethod
    def _map_to_depth_category(depth_value: Union[float, np.ndarray]) -> HitDepths:
        """
        Convert continuous depth value (0.0-1.0) to discrete depth category.
        Thresholds calibrated to match real baseball depth distribution.
        """
        if depth_value < 0.30:
            return HitDepths.SH    # Shallow (infield, shallow outfield)
        elif depth_value < 0.65:
            return HitDepths.MD    # Medium (normal outfield depth)
        elif depth_value < 0.85:
            return HitDepths.DP    # Deep (warning track, gaps)
        else:
            return HitDepths.XD    # Extra Deep (home run distance)
    
    @classmethod
    def determine_hit_depth(cls, 
                          outcome_name: str, 
                          hit_type: HitTypes,
                          sector: HitSectors = HitSectors.CF) -> HitDepths:
        """
        Determine hit depth using triangular distributions with contextual modifiers.
        
        Args:
            outcome_name: Outcome enum value (e.g., Outcome.SL.value = 'SINGLE')
            hit_type: HitTypes enum (GB, FB, LD, PU)
            sector: Spray direction (affects center vs corner depth)
            
        Returns:
            HitDepths enum: SH, MD, DP, or XD
        """
        # Step 1: Get base distribution for outcome + hit type
        left, mode, right = cls._get_base_distribution(outcome_name, hit_type)
        
        # Step 2: Sample from triangular distribution
        depth_value = triangular(left, mode, right)
        
        # Step 3: Apply contextual modifiers
        depth_value = cls._apply_sector_modifier(depth_value, sector)
        
        # Step 4: Map continuous value to discrete category
        return cls._map_to_depth_category(depth_value)
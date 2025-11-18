from UTILITIES.ENUMS import *
from typing import Tuple, Optional
import random


class BaseRunningManager:
    """
    Team-specific base running decision manager.
    Returns probability thresholds that outcome files use with random numbers.
    Methods can factor in game context (outs, score, inning) to adjust probabilities.
    """
    
    # ==================== FLYOUT - R3 TAG UP ====================
    
    @staticmethod
    def r3_tag_adv(
        outs: int = 0,
        hit_depth: Optional[HitDepths] = None,
        fielder: Optional[Positions] = None,
        runner_speed: int = 5,
        aggression: int = 5
    ) -> int:
        """
        Probability (per 1000) that R3 will ATTEMPT to tag and score on flyout.
        This is the decision to go or stay - made by third base coach.
        
        Args:
            outs: Current number of outs (0-2)
            hit_depth: Depth of fly ball (HitDepths.SH, MD, DP, XD)
            fielder: Position of fielder making catch
            runner_speed: Runner speed rating (1-10, default 5)
            aggression: Team base running aggression (1-10, default 5)
        
        Returns:
            Probability (per 1000) that runner attempts to tag.
            rand < threshold: Runner stays at 3rd (doesn't attempt)
            rand >= threshold: Runner tags and attempts to score
        
        Base attempt rates by depth:
        - SHORT: 15% attempt
        - MEDIUM: 55% attempt  
        - DEEP/EXTRA DEEP: 90% attempt
        """
        # Base attempt probability by depth
        if hit_depth == HitDepths.SH:
            base_prob = 150  # 15% attempt on shallow
        elif hit_depth in [HitDepths.DP, HitDepths.XD]:
            base_prob = 900  # 90% attempt on deep
        else:  # MEDIUM or None
            base_prob = 550  # 55% attempt on medium
        
        # With 2 outs, always try (inning ends anyway)
        if outs == 2:
            return 1000  # 100% attempt
        
        # With 0 outs, more conservative
        if outs == 0:
            base_prob -= 100
        
        # Strong arm fielders discourage attempts
        if fielder in [Positions._CF, Positions._RF]:
            base_prob -= 100  # Strong arms
        elif fielder == Positions._LF:
            base_prob += 100  # Weaker arm
        
        # Fast runners more likely to go
        speed_adj = (runner_speed - 5) * 30  # -120 to +120
        base_prob += speed_adj
        
        # Team aggression factor (1=conservative, 10=aggressive)
        aggression_adj = (aggression - 5) * 40  # -160 to +160
        base_prob += aggression_adj
        
        return max(50, min(1000, base_prob))  # 5-100%
    
    @staticmethod
    def r3_tag_out(
        hit_depth: Optional[HitDepths] = None,
        fielder: Optional[Positions] = None,
        runner_speed: int = 5
    ) -> int:
        """
        Probability (per 1000) that R3 is thrown out at home WHEN ATTEMPTING to tag.
        This models throw accuracy and runner speed vs. throw strength.
        
        Args:
            hit_depth: Depth of fly ball
            fielder: Position of fielder making catch
            runner_speed: Runner speed rating (1-10, default 5)
        
        Returns:
            Probability (per 1000) that runner is thrown out.
            rand < threshold: Thrown out at home
            rand >= threshold: Scores safely
        
        Base out rates when attempting:
        - SHORT: 35% thrown out (good throw, short distance)
        - MEDIUM: 15% thrown out
        - DEEP/EXTRA DEEP: 5% thrown out (long throw)
        """
        # Base out probability by depth
        if hit_depth == HitDepths.SH:
            out_prob = 350  # 35% out on shallow
        elif hit_depth in [HitDepths.DP, HitDepths.XD]:
            out_prob = 50   # 5% out on deep
        else:  # MEDIUM or None
            out_prob = 150  # 15% out on medium
        
        # Strong arm fielders increase out probability
        if fielder in [Positions._CF, Positions._RF]:
            out_prob += 80   # +8% for strong arms
        elif fielder == Positions._LF:
            out_prob -= 50   # -5% for weaker arm
        
        # Fast runners less likely to be thrown out
        speed_adj = (runner_speed - 5) * 25  # -100 to +100
        out_prob -= speed_adj  # Fast = lower out probability
        
        return max(20, min(500, out_prob))  # 2-50%
    


    


    


    

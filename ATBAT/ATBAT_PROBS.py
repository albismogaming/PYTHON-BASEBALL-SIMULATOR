from typing import Dict
from UTILITIES.RANDOM import get_random
import math as m
import random as r
import numpy as np

class ProbabilityModifier:
    """ Applies situational modifiers to precomputed base matchup probabilities. """
    
    @staticmethod
    def calculate_probability(batter_prob, pitcher_prob, batter_weight=0.50, pitcher_weight=0.50, *modifiers):
        """ Calculate combined probability using logit transformation with optional modifiers. """
        # Avoid division by zero and extreme values
        epsilon = 1e-6
        batter_prob = max(epsilon, min(batter_prob, 1 - epsilon))
        pitcher_prob = max(epsilon, min(pitcher_prob, 1 - epsilon))
        
        # Convert to log-odds (logit transformation)
        batter_logit = m.log(batter_prob / (1 - batter_prob))
        pitcher_logit = m.log(pitcher_prob / (1 - pitcher_prob))
        
        # Weighted average in log-odds space
        combined_logit = (batter_logit * batter_weight) + (pitcher_logit * pitcher_weight)
        
        # Apply modifiers in logit space (sum of log of each multiplier)
        mod_sum = 0.0
        for mod in modifiers:
            if mod > 0 and not m.isnan(mod) and not m.isinf(mod):
                mod_sum += m.log(mod)
            # else: ignore invalid modifiers
        
        # Final logit with modifiers
        final_logit = combined_logit + mod_sum
        
        # Convert back to probability (inverse logit)
        probability = 1.0 / (1.0 + m.exp(-final_logit))
        
        # Clamp to valid probability range
        return max(0.0, min(probability, 1.0))
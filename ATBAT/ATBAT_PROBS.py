from typing import Dict
from UTILITIES.RANDOM import get_random
import math as m

class ProbabilityModifier:
    """ Applies situational modifiers to precomputed base matchup probabilities. """
    
    @staticmethod
    def calculate_probability(batter_prob, pitcher_prob, batter_weight=0.50, pitcher_weight=0.50):
        """ Calculate combined probability using logit transformation (log-odds). """
        # Avoid division by zero and extreme values
        epsilon = 1e-6
        batter_prob = max(epsilon, min(batter_prob, 1 - epsilon))
        pitcher_prob = max(epsilon, min(pitcher_prob, 1 - epsilon))
        
        # Convert to log-odds (logit transformation)
        batter_logit = m.log(batter_prob / (1 - batter_prob))
        pitcher_logit = m.log(pitcher_prob / (1 - pitcher_prob))
        
        # Weighted average in log-odds space
        combined_logit = (batter_logit * batter_weight) + (pitcher_logit * pitcher_weight)
        
        # Convert back to probability (inverse logit)
        return 1 / (1 + m.exp(-combined_logit))

    @staticmethod
    def apply_modifiers(probabilities: Dict[str, float], modifiers: Dict[str, float]) -> Dict[str, float]:
        """ Apply situational modifiers to probabilities. """

        adjusted = {}
        for outcome, prob in probabilities.items():
            multiplier = modifiers.get(outcome, 1.0)
            adjusted[outcome] = prob * multiplier
        
        return adjusted
    
    # Base platoon modifiers (neutral matchup = 1.0)
    # These represent typical MLB platoon effects
    BASE_PLATOON_ADVANTAGE = {
        'BA': 1.10,     # Higher batting average for favorable matchup
        'SO': 0.90,     # Fewer strikeouts
        'BB': 1.10,     # Better discipline
        'HP': 1.05,     # Hit by pitch advantage
        'HR': 1.12,     # Power advantage for favorable matchup
        'IH': 1.08,     # Infield hits advantage
        'SL': 1.08,     # Singles advantage
        'DL': 1.08,     # Doubles advantage
        'TL': 1.10,     # Triples slightly boosted
        'GO': 0.92,     # Fewer groundouts
        'FO': 0.92,     # Fewer flyouts
        'LO': 0.92,     # Fewer lineouts
        'PO': 0.92,     # Fewer popouts
    }
    
    BASE_PLATOON_DISADVANTAGE = {
        'BA': 0.90,     # Lower batting average for unfavorable matchup
        'SO': 1.10,     # More strikeouts
        'BB': 0.90,     # Worse discipline
        'HP': 0.95,     # Hit by pitch disadvantage
        'HR': 0.88,     # Power disadvantage for unfavorable matchup
        'IH': 0.92,     # Infield hits disadvantage
        'SL': 0.92,     # Singles disadvantage
        'DL': 0.92,     # Doubles disadvantage
        'TL': 0.90,     # Triples slightly reduced
        'GO': 1.08,     # More groundouts
        'FO': 1.08,     # More flyouts
        'LO': 1.08,     # More lineouts
        'PO': 1.08,     # More popouts
    }
    
    @staticmethod
    def get_platoon_split_modifiers(batter, pitcher, use_variability: bool = True) -> Dict[str, float]:
        """ Calculate platoon modifiers for this specific matchup with optional randomized strength. """
        
        # Switch hitters always bat from favorable side
        if batter.bats == 'B':
            base_mods = ProbabilityModifier.BASE_PLATOON_ADVANTAGE
        # Same-handed = disadvantage (LHB vs LHP, RHB vs RHP)
        elif batter.bats == pitcher.throws:
            base_mods = ProbabilityModifier.BASE_PLATOON_DISADVANTAGE
        # Opposite-handed = advantage (LHB vs RHP, RHB vs LHP)
        else:
            base_mods = ProbabilityModifier.BASE_PLATOON_ADVANTAGE
        
        # Add variability: randomize strength from 50% to 100% of base effect
        if use_variability:
            # Random factor between 0.5 and 1.0 (different per matchup)
            strength = 0.5 + (get_random() * 0.5)
            
            # Apply strength to move modifiers closer to neutral (1.0)
            modifiers = {
                outcome: 1.0 + (multiplier - 1.0) * strength
                for outcome, multiplier in base_mods.items()
            }
        else:
            # Use full base modifiers
            modifiers = base_mods.copy()
        
        return modifiers
import numpy as np
from UTILITIES.SETTINGS import *


class ProbabilityCalculator:
    """
    Static utility methods for probability calculations.
    No instance needed - all methods are stateless.
    """
    
    @staticmethod
    def calculate_base_probability(batter_prob, pitcher_prob, league_prob):
        """
        Calculate combined probability using odds ratio method.
        
        Method: Calculate how much each player deviates from league average,
        then apply both deviations to the league baseline.
        
        This ensures:
        - League avg batter vs league avg pitcher = league avg result
        - Extreme values are properly bounded
        - Effects are multiplicative (as they are in real baseball)
        """
        # Avoid division by zero and extreme values
        epsilon = 0.0001
        batter_prob = np.clip(batter_prob, epsilon, 1 - epsilon)
        pitcher_prob = np.clip(pitcher_prob, epsilon, 1 - epsilon)
        league_prob = np.clip(league_prob, epsilon, 1 - epsilon)
        
        # Convert to odds: odds = prob / (1 - prob)
        batter_odds = batter_prob / (1 - batter_prob)
        pitcher_odds = pitcher_prob / (1 - pitcher_prob)
        league_odds = league_prob / (1 - league_prob)
        
        # Calculate odds ratios: how much better/worse than league
        # batter_ratio > 1 means better than average
        # pitcher_ratio > 1 means pitcher allows more (worse for pitcher)
        batter_ratio = batter_odds / league_odds
        pitcher_ratio = pitcher_odds / league_odds
        
        # Combine effects: start with league baseline, apply both player effects
        # This is the standard sabermetric approach
        combined_odds = league_odds * batter_ratio * pitcher_ratio
        
        # Convert odds back to probability: prob = odds / (1 + odds)
        probability = combined_odds / (1 + combined_odds)
        
        return np.clip(probability, 0, 1) # Ensure valid probability range

    @staticmethod
    def calculate_split_advantage(batter, pitcher) -> float:
        """
        Calculate platoon advantage multiplier.
        
        Returns:
            float: Multiplier to apply to probabilities (1.0 = neutral)
                >1.0 = favorable matchup
                <1.0 = unfavorable matchup
        """
        # Switch hitters ALWAYS have favorable matchup
        if batter.bats == 'B':
            return 1.0 + np.random.uniform(0.01, 0.10)  # e.g., +5% to +10%
        
        # Regular batters: check if favorable
        favorable = (
            (batter.bats == 'L' and pitcher.throws == 'R') or
            (batter.bats == 'R' and pitcher.throws == 'L')
        )
        
        if favorable:
            return 1.0 + np.random.uniform(0.01, 0.10)  # e.g., +5% to +10%
        else:
            return 1.0 - np.random.uniform(0.01, 0.10)  # e.g., -5% to -10%

    @staticmethod
    def apply_park_factors(probabilities, park_factors):
        """
        Apply park factors to probabilities.
        
        Args:
            probabilities: Dict of outcome probabilities
            park_factors: Dict of park factor multipliers per outcome
            
        Returns:
            dict: Adjusted probabilities
        """
        return {outcome: prob * park_factors.get(outcome, 1.0) 
                for outcome, prob in probabilities.items()}


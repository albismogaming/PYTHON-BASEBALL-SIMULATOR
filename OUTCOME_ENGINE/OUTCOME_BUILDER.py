from UTILITIES.ENUMS import Outcome
from ATBAT.ATBAT_PROBS import ProbabilityCalculator
from typing import Dict


class OutcomeBuilder:
    """
    Builds outcome probability distributions for at-bat simulations.
    Pure stateless utility - takes raw rates, returns combined probabilities.
    """
    
    @staticmethod
    def build_base_probabilities(batter_stats: Dict[str, float], 
                                    pitcher_stats: Dict[str, float],
                                    league_stats: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate combined probabilities for all outcomes using odds ratio method.
        Returns dict with enum member names as keys: 'SO', 'BB', 'HP', 'HR'
        """
        distribution = {}
        for outcome_type in [Outcome.SO, Outcome.BB, Outcome.HP, Outcome.HR]:
            outcome_key = outcome_type.name  # Use enum member name: 'SO', 'BB', 'HP', 'HR'

            batter_rate = batter_stats.get(outcome_key, 0.0)
            pitcher_rate = pitcher_stats.get(outcome_key, batter_rate)  # Fallback to batter if missing
            league_rate = league_stats.get(outcome_key, batter_rate)    # Fallback to batter if missing
            
            distribution[outcome_key] = ProbabilityCalculator.calculate_base_probability(
                batter_rate, pitcher_rate, league_rate
            )
        
        return distribution

    @staticmethod
    def build_hits_distribution(batter_stats: Dict[str, float], pitcher_stats: Dict[str, float], league_stats: Dict[str, float]) -> Dict[str, float]:
        """
        Build the distribution of hit types (SL, DL, TL, IH) based on batter/pitcher matchup.
        
        Uses odds ratio to combine pitcher and batter hit tendencies.
        Returns dict with enum member names as keys: 'SL', 'DL', 'TL', 'IH'
        
        Args:
            batter_hit_rates: dict with batter's hit rates keyed by enum member names
            pitcher_hit_rates: dict with pitcher's allowed hit rates keyed by enum member names
            league_hit_rates: dict with league average hit rates keyed by enum member names
        """
        
        distribution = {}
        for outcome_type in [Outcome.IH, Outcome.SL, Outcome.DL, Outcome.TL]:
            outcome_key = outcome_type.name  # Use enum member name: 'IH', 'SL', 'DL', 'TL'
            
            batter_rate = batter_stats.get(outcome_key, 0.0)
            pitcher_rate = pitcher_stats.get(outcome_key, batter_rate)
            league_rate = league_stats.get(outcome_key, batter_rate)
            
            combined_rate = ProbabilityCalculator.calculate_base_probability(
                batter_rate, pitcher_rate, league_rate
            )
            distribution[outcome_key] = max(0, combined_rate)
        
        # Normalize to ensure all probabilities sum to 1
        total = sum(distribution.values())
        if total > 0:
            distribution = {outcome: prob / total for outcome, prob in distribution.items()}
        
        return distribution
        
    @staticmethod
    def build_outs_distribution(pitcher_gbfb, batter_gbfb, league_gbfb):
        """
        Build the distribution of out types based on GB/FB ratios.
        
        Uses odds ratio to combine pitcher and batter GB/FB tendencies,
        then distributes fly ball outs among FO/LO/PO based on typical percentages.
        
        Args:
            pitcher_gbfb: Pitcher's ground ball to fly ball ratio
            batter_gbfb: Batter's ground ball to fly ball ratio
            
        Returns:
            dict: Distribution of out types {Outcome: probability}
        """
        # Calculate fly ball rate using odds ratio method
        # fly_ball_rate = 1 / (1 + GB/FB)
        pitcher_fb_rate = 1.0 / (1.0 + pitcher_gbfb)
        batter_fb_rate = 1.0 / (1.0 + batter_gbfb)
        league_fb_rate = 1.0 / (1.0 + league_gbfb)
        
        combined_fb_rate = ProbabilityCalculator.calculate_base_probability(
            batter_fb_rate, pitcher_fb_rate, league_fb_rate
        )
        
        # Distribute fly ball outs among types
        # Typical distribution: 56% flyouts, 26% lineouts, 18% popouts
        distribution = {
            Outcome.FO.name: combined_fb_rate * 0.56,
            Outcome.LO.name: combined_fb_rate * 0.26,
            Outcome.PO.name: combined_fb_rate * 0.18
        }
        
        # Ground outs are what remains
        distribution[Outcome.GO.name] = 1.0 - sum(distribution.values())
        
        return distribution

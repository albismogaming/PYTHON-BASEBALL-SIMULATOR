from typing import Dict


class ProbabilityModifier:
    """
    Applies situational modifiers to precomputed base matchup probabilities.
    
    Base matchup probabilities come from the precomputed table (batter vs pitcher).
    This class applies contextual adjustments like park factors, game situation, etc.
    """
    
    @staticmethod
    def apply_park_factors(probabilities: Dict[str, float], park_factors: Dict[str, float]) -> Dict[str, float]:
        """ Apply park factors to base probabilities. """
        
        adjusted = {}
        for outcome, prob in probabilities.items():
            # Apply park factor if it exists for this outcome
            if outcome in park_factors:
                adjusted[outcome] = prob * park_factors[outcome]
            else:
                adjusted[outcome] = prob
        
        return adjusted
    
    @staticmethod
    def apply_league_factors(probabilities: Dict[str, float], league_averages: Dict[str, float]) -> Dict[str, float]:
        """ Regress probabilities toward league average. """

        adjusted = {}
        for outcome, prob in probabilities.items():
            if outcome in league_averages:
                adjusted[outcome] = prob * league_averages[outcome]
            else:
                adjusted[outcome] = prob

        return adjusted
    
    @staticmethod
    def apply_situational_modifiers(probabilities: Dict[str, float], modifiers: Dict[str, float]) -> Dict[str, float]:
        """ Apply situational modifiers to probabilities. """

        adjusted = {}
        for outcome, prob in probabilities.items():
            multiplier = modifiers.get(outcome, 1.0)
            adjusted[outcome] = prob * multiplier
        
        return adjusted
    
    @staticmethod
    def apply_all_modifiers(base_probs: Dict[str, float], 
                            league_averages: Dict[str, float] | None = None, 
                            park_factors: Dict[str, float] | None = None,
                            situational_modifiers: Dict[str, float] | None = None) -> Dict[str, float]:
        """
        Apply all modifiers to base probabilities in sequence.
        
        Recommended pipeline:
        1. League regression (normalize to context)
        2. Park factors (stadium effects)
        3. Situational modifiers (clutch, fatigue, etc.)
        
        Args:
            base_probabilities: Base matchup probabilities from precomputed table
            league_averages: Optional league average rates for regression
            park_factors: Optional park factor adjustments
            situational_modifiers: Optional situational adjustments
            regression_weight: How much to regress toward league mean (default 0.1)
            
        Returns:
            dict: Fully adjusted probabilities
        """
        probs = base_probs.copy()
        
        # Apply league regression if provided
        if league_averages:
            probs = ProbabilityModifier.apply_league_factors(probs, league_averages)
        
        # Apply park factors if provided
        if park_factors:
            probs = ProbabilityModifier.apply_park_factors(probs, park_factors)
        
        # Apply situational modifiers if provided
        if situational_modifiers:
            probs = ProbabilityModifier.apply_situational_modifiers(probs, situational_modifiers)
        
        # Ensure all probabilities are within valid range [0, 1]
        probs = {outcome: max(0.0, min(1.0, prob)) 
                for outcome, prob in probs.items()}
        
        return probs
    
    @staticmethod
    def normalize_probabilities(probabilities: Dict[str, float]) -> Dict[str, float]:
        """ Normalize a set of probabilities to sum to 1.0. """
        total = sum(probabilities.values())
        
        if total == 0:
            # Avoid division by zero - return uniform distribution
            num_outcomes = len(probabilities)
            return {outcome: 1.0 / num_outcomes for outcome in probabilities}
        
        return {outcome: prob / total for outcome, prob in probabilities.items()}

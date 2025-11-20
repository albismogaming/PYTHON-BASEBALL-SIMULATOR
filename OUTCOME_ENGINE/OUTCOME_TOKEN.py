from ATBAT.ATBAT_PROBS import ProbabilityModifier
from UTILITIES.MATCHUP_CACHE import MatchupCache
from UTILITIES.ENUMS import Outcome
from UTILITIES.FILE_PATHS import MATCHUP_TABLE
from typing import Optional


class MatchupTokenGenerator:
    """
    Generates matchup probability tokens for at-bat simulation.
    
    Simply looks up precomputed probabilities and applies contextual modifiers
    (park factors, etc.). No complex calculation - just lookup and modify.
    """
    
    # Class-level cache instance (loaded once)
    _matchup_cache: Optional[MatchupCache] = None
    
    @classmethod
    def initialize_cache(cls, cache_path: str = MATCHUP_TABLE):
        """
        Initialize the matchup cache. Call this once at game startup.
        
        Args:
            cache_path: Path to precomputed matchup table
        """
        if cls._matchup_cache is None:
            cls._matchup_cache = MatchupCache(cache_path)
            cls._matchup_cache.load()
    
    @classmethod
    def generate_token(cls, gamestate, batter, pitcher):
        """
        Generate probability token from precomputed matchup table.
        
        Pipeline: lookup precomputed → apply park factors → return
        
        Returns: (base_probs, babip_prob, hits_keys, hits_vals, outs_keys, outs_vals)
        """
        # Initialize cache if not already done
        if cls._matchup_cache is None:
            cls.initialize_cache()
        
        # Lookup precomputed matchup probabilities
        assert cls._matchup_cache is not None
        matchup_probs = cls._matchup_cache.get_matchup(batter.team_abbrev, batter.player_id, pitcher.team_abbrev, pitcher.player_id)
        
        if matchup_probs is None:
            raise ValueError(
                f"No precomputed matchup found for batter {batter.player_id} vs pitcher {pitcher.player_id}. "
                f"Run PRECOMPUTE_MATCHUPS.py to generate the matchup table."
            )
        
        # Extract all outcome probabilities
        outcome_probs = {
            outcome: matchup_probs[outcome]
            for outcome in ['SO', 'BB', 'HP', 'HR', 'IH', 'SL', 'DL', 'TL', 'GO', 'FO', 'LO', 'PO']
        }
        
        # Get BABIP from precomputed data
        babip_prob = matchup_probs['BABIP_batter']
        
        # Apply park factors if present
        park_factors = gamestate.home_team.park_factors
        if park_factors:
            outcome_probs = ProbabilityModifier.apply_park_factors(outcome_probs, park_factors)
        
        return outcome_probs, babip_prob
    

    
import pickle
from typing import Dict, Tuple, Optional
from pathlib import Path
from UTILITIES.FILE_PATHS import MATCHUP_TABLE


class MatchupCache:
    """
    Fast lookup cache for precomputed batter-pitcher matchup probabilities.
    
    Usage:
        # Load the precomputed table once at startup
        cache = MatchupCache("GAME_DATA/matchup_table.pkl")
        
        # Fast lookup during simulation
        probs = cache.get_matchup(batter.player_id, pitcher.player_id)
    """
    
    def __init__(self, table_path: str = MATCHUP_TABLE):
        """
        Initialize the matchup cache.
        
        Args:
            table_path: Path to the precomputed matchup table pickle file
        """
        self.table_path = table_path
        self.matchup_table: Dict[Tuple[str, int, str, int], Dict[str, float]] = {}
        self._loaded = False
    
    def load(self) -> bool:
        """
        Load the precomputed matchup table from disk.
        
        Returns:
            True if successful, False otherwise
        """
        if not Path(self.table_path).exists():
            print(f"Warning: Matchup table not found at {self.table_path}")
            print("Run PRECOMPUTE_MATCHUPS.py to generate the table.")
            return False
        
        try:
            with open(self.table_path, 'rb') as f:
                self.matchup_table = pickle.load(f)
            self._loaded = True
            return True
        
        except Exception as e:
            print(f"Error loading matchup table: {e}")
            return False
    
    def get_matchup(self, batter_team: str, batter_id: int, pitcher_team: str, pitcher_id: int) -> Optional[Dict[str, float]]:
        """
        Get precomputed probabilities for a batter-pitcher matchup.
        
        Args:
            batter_team: Batter's team abbreviation
            batter_id: Batter's player ID
            pitcher_team: Pitcher's team abbreviation
            pitcher_id: Pitcher's player ID
            
        Returns:
            Dictionary of outcome probabilities, or None if not found
        """
        if not self._loaded:
            self.load()
        
        return self.matchup_table.get((batter_team, batter_id, pitcher_team, pitcher_id), None)
    
    def has_matchup(self, batter_team: str, batter_id: int, pitcher_team: str, pitcher_id: int) -> bool:
        """
        Check if a matchup exists in the precomputed table.
        
        Args:
            batter_team: Batter's team abbreviation
            batter_id: Batter's player ID
            pitcher_team: Pitcher's team abbreviation
            pitcher_id: Pitcher's player ID
            
        Returns:
            True if matchup exists, False otherwise
        """
        if not self._loaded:
            self.load()
        
        return (batter_team, batter_id, pitcher_team, pitcher_id) in self.matchup_table
    
    def get_outcome_prob(self, batter_team: str, batter_id: int, pitcher_team: str, pitcher_id: int, outcome: str) -> Optional[float]:
        """
        Get probability for a specific outcome in a matchup.
        
        Args:
            batter_team: Batter's team abbreviation
            batter_id: Batter's player ID
            pitcher_team: Pitcher's team abbreviation
            pitcher_id: Pitcher's player ID
            outcome: Outcome code (e.g., 'SO', 'BB', 'HR', 'SL')
            
        Returns:
            Probability value, or None if matchup/outcome not found
        """
        matchup = self.get_matchup(batter_team, batter_id, pitcher_team, pitcher_id)
        if matchup is None:
            return None
        return matchup.get(outcome, None)
    
    @property
    def is_loaded(self) -> bool:
        """Check if the matchup table has been loaded."""
        return self._loaded
    
    @property
    def size(self) -> int:
        """Get the number of matchups in the cache."""
        return len(self.matchup_table)
    
    def clear(self):
        """Clear the cached matchup table from memory."""
        self.matchup_table.clear()
        self._loaded = False


# Global singleton instance for easy access
_global_cache: Optional[MatchupCache] = None


def get_global_cache(table_path: str = "GAME_DATA/matchup_table.pkl") -> MatchupCache:
    """
    Get or create the global matchup cache instance.
    
    Args:
        table_path: Path to the matchup table (only used on first call)
        
    Returns:
        Global MatchupCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = MatchupCache(table_path)
        _global_cache.load()
    return _global_cache


def clear_global_cache():
    """Clear the global matchup cache."""
    global _global_cache
    if _global_cache is not None:
        _global_cache.clear()
        _global_cache = None

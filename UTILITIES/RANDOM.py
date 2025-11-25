import random

class RandomPool:
    """
    Pre-generated pool of random numbers for fast sequential access.
    Eliminates repeated random.random() call overhead during simulation.
    """
    def __init__(self, size=500, min_val=0.0, max_val=1.0):
        """
        Generate pool of random numbers within a specified range.
        
        Args:
            size: Number of random values to pre-generate (typical game uses ~200)
            min_val: Minimum value in the range (inclusive)
            max_val: Maximum value in the range (inclusive)
        """
        self.pool = [random.uniform(min_val, max_val) for _ in range(size)]
        self.index = 0
        self.size = size
    
    def next(self):
        """Get next random number from pool (wraps around if exhausted)."""
        value = self.pool[self.index]
        self.index = (self.index + 1) % self.size
        return value
    
    def reset(self):
        """Reset index to start of pool."""
        self.index = 0


# Global pools for different decision types
_random_pool = None       # General decisions (0.0 to 1.0)
_out_pool = None         # Out/safe decisions - low probabilities (0.001 to 0.100)
_adv_pool = None     # Advance decisions - medium probabilities (0.050 to 0.700)
_scr_pool = None       # Score decisions - medium-high probabilities (0.250 to 0.650)
_sac_pool = None       # Sacrifice decisions - low probabilities (0.001 to 0.100)

def init_random_pool(size=500):
    """
    Initialize all random pools for a game with appropriate ranges.
    
    Args:
        size: Number of random values to pre-generate per pool
    """
    global _random_pool, _out_pool, _adv_pool, _scr_pool, _sac_pool
    _random_pool = RandomPool(size, min_val=0.0, max_val=1.0)      # Full range for general use
    _out_pool = RandomPool(size, min_val=0.001, max_val=0.100)     # Low probabilities for outs
    _adv_pool = RandomPool(size, min_val=0.050, max_val=0.700) # Medium range for advances
    _scr_pool = RandomPool(size, min_val=0.250, max_val=0.650)   # Medium-high for scoring
    _sac_pool = RandomPool(size, min_val=0.001, max_val=0.100)     # Low probabilities for outs


def get_random():
    """Get next random number from the general pool."""
    return _random_pool.next()

def out_random():
    """Get next random threshold for out/safe decisions."""
    return _out_pool.next()

def adv_random():
    """Get next random threshold for advance/hold decisions."""
    return _adv_pool.next()

def scr_random():
    """Get next random threshold for score/stop decisions."""
    return _scr_pool.next()

def sac_random():
    """Get next random threshold for score/stop decisions."""
    return _sac_pool.next()
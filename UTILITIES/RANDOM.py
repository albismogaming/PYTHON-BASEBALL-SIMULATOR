import random

class RandomPool:
    """
    Pre-generated pool of random numbers for fast sequential access.
    Eliminates repeated random.random() call overhead during simulation.
    """
    def __init__(self, size=10000, min_val=0.0, max_val=1.0):
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
_rand_pool = None       # General decisions (0.0 to 1.0)
_outs_pool = None         # Out/safe decisions - low probabilities (0.001 to 0.100)
_advs_pool = None     # Advance decisions - medium probabilities (0.050 to 0.700)
_scrs_pool = None       # Score decisions - medium-high probabilities (0.250 to 0.650)
_sacs_pool = None       # Sacrifice decisions - low probabilities (0.001 to 0.100)
_stls_pool = None       # Steal decisions - medium-high probabilities (0.640 to 0.870)
_poff_pool = None       # Pickoff decisions - low probabilities (0.001 to 0.100)

def init_random_pool(size=10000):
    """ Initialize all random pools for a game with appropriate ranges. """
    global _rand_pool, _outs_pool, _advs_pool, _scrs_pool, _sacs_pool, _stls_pool, _poff_pool
    _rand_pool = RandomPool(size, min_val=0.000, max_val=1.000)      # Full range for general use
    _outs_pool = RandomPool(size, min_val=0.030, max_val=0.100)     # Low probabilities for outs
    _advs_pool = RandomPool(size, min_val=0.150, max_val=0.850)     # Medium range for advances
    _scrs_pool = RandomPool(size, min_val=0.350, max_val=0.750)     # Medium-high for scoring
    _sacs_pool = RandomPool(size, min_val=0.001, max_val=0.100)     # Low probabilities for outs
    _stls_pool = RandomPool(size, min_val=0.330, max_val=0.640)     # Low probabilities for steals
    _poff_pool = RandomPool(size, min_val=0.001, max_val=0.100)     # Low probabilities for pickoffs


def get_random():
    """Get next random number from the general pool."""
    return _rand_pool.next()

def out_random():
    """Get next random threshold for out/safe decisions."""
    return _outs_pool.next()

def adv_random():
    """Get next random threshold for advance/hold decisions."""
    return _advs_pool.next()

def scr_random():
    """Get next random threshold for score/stop decisions."""
    return _scrs_pool.next()

def sac_random():
    """Get next random threshold for score/stop decisions."""
    return _sacs_pool.next()

def stl_random():
    """Get next random threshold for steal/hold decisions."""
    return _stls_pool.next()

def poff_random():
    """Get next random threshold for pickoff decisions."""
    return _poff_pool.next()
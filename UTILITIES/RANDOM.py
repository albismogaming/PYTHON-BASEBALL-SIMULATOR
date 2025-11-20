import random

class RandomPool:
    """
    Pre-generated pool of random numbers for fast sequential access.
    Eliminates repeated random.random() call overhead during simulation.
    """
    def __init__(self, size=500):
        """
        Generate pool of random numbers.
        
        Args:
            size: Number of random values to pre-generate (typical game uses ~200)
        """
        self.pool = [random.random() for _ in range(size)]
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


# Global instance to be initialized per game
_random_pool = None

def init_random_pool(size=500):
    """Initialize the global random pool for a game."""
    global _random_pool
    _random_pool = RandomPool(size)

def get_random():
    """Get next random number from the global pool."""
    return _random_pool.next()

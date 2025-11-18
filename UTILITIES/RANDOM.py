import numpy as np

# ==================== HELPER FUNCTIONS ====================

def bernoulli(p: float) -> bool:
    """
    Bernoulli trial (single yes/no outcome)
    
    Args:
        p: Probability of success (0 to 1)
    
    Returns:
        True with probability p, False otherwise
    
    Use case: Completion/incompletion, fumble/no fumble, penalty/no penalty
    """
    return np.random.random() < p


def weighted_choice(choices: list, weights: list):
    """
    Choose from a list with weighted probabilities
    
    Args:
        choices: List of possible outcomes
        weights: List of probabilities (must sum to 1)
    
    Returns:
        One randomly selected choice
    
    Use case: Play outcomes with different probabilities
    """
    return np.random.choice(choices, p=weights)
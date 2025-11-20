import numpy as np
from typing import Union, Optional

# ==================== CONTINUOUS DISTRIBUTIONS ====================

def normal(mean: float = 0.0, std_dev: float = 1.0, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Normal (Gaussian) distribution
    
    Args:
        mean: Mean of the distribution
        std_dev: Standard deviation
        size: Number of samples (None returns single value)
    
    Returns:
        Random sample(s) from normal distribution
    
    Use case: Yards gained, time elapsed (symmetric around mean)
    """
    return np.random.normal(mean, std_dev, size)

def lognormal(mean: float = 0.0, sigma: float = 1.0, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Log-normal distribution (right-skewed)
    
    Args:
        mean: Mean of underlying normal distribution
        sigma: Standard deviation of underlying normal
        size: Number of samples
    
    Returns:
        Random sample(s) from log-normal distribution
    
    Use case: Big play potential, breakaway runs (mostly small, occasional huge)
    """
    return np.random.lognormal(mean, sigma, size)

def exponential(scale: float = 1.0, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Exponential distribution
    
    Args:
        scale: Scale parameter (1/lambda, mean of distribution)
        size: Number of samples
    
    Returns:
        Random sample(s) from exponential distribution
    
    Use case: Time between events, injury recovery time
    """
    return np.random.exponential(scale, size)

def gamma(shape: float, scale: float = 1.0, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Gamma distribution
    
    Args:
        shape: Shape parameter (k)
        scale: Scale parameter (theta)
        size: Number of samples
    
    Returns:
        Random sample(s) from gamma distribution
    
    Use case: Time until multiple events occur, aggregate performance
    """
    return np.random.gamma(shape, scale, size)

def beta(alpha: float, beta_param: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Beta distribution (bounded between 0 and 1)
    
    Args:
        alpha: Alpha parameter (shape)
        beta_param: Beta parameter (shape)
        size: Number of samples
    
    Returns:
        Random sample(s) from beta distribution (0 to 1)
    
    Use case: Success probabilities, completion percentages, win probability
    """
    return np.random.beta(alpha, beta_param, size)

def pareto(shape: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Pareto distribution (power law)
    
    Args:
        shape: Shape parameter (alpha)
        size: Number of samples
    
    Returns:
        Random sample(s) from Pareto distribution
    
    Use case: Extreme events, "heavy tail" outcomes (rare huge plays)
    """
    return np.random.pareto(shape, size)

def weibull(shape: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Weibull distribution
    
    Args:
        shape: Shape parameter (k)
        size: Number of samples
    
    Returns:
        Random sample(s) from Weibull distribution
    
    Use case: Time to failure, player fatigue over time
    """
    return np.random.weibull(shape, size)

def uniform(low: float = 0.0, high: float = 1.0, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Uniform distribution (all values equally likely)
    
    Args:
        low: Lower bound (inclusive)
        high: Upper bound (exclusive)
        size: Number of samples
    
    Returns:
        Random sample(s) from uniform distribution
    
    Use case: Random events, coin flips, unbiased selection
    """
    return np.random.uniform(low, high, size)

def triangular(left: float, mode: float, right: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Triangular distribution
    
    Args:
        left: Lower bound
        mode: Peak of distribution
        right: Upper bound
        size: Number of samples
    
    Returns:
        Random sample(s) from triangular distribution
    
    Use case: When you know min, max, and most likely value
    """
    return np.random.triangular(left, mode, right, size)

# ==================== DISCRETE DISTRIBUTIONS ====================

def poisson(lam: float, size: Optional[int] = None) -> Union[int, np.ndarray]:
    """
    Poisson distribution (count of events)
    
    Args:
        lam: Expected number of events (lambda)
        size: Number of samples
    
    Returns:
        Random sample(s) from Poisson distribution (integers)
    
    Use case: Number of scores per quarter, turnovers per game, sacks
    """
    return np.random.poisson(lam, size)

def binomial(n: int, p: float, size: Optional[int] = None) -> Union[int, np.ndarray]:
    """
    Binomial distribution (number of successes in n trials)
    
    Args:
        n: Number of trials
        p: Probability of success (0 to 1)
        size: Number of samples
    
    Returns:
        Random sample(s) from binomial distribution (integers)
    
    Use case: Completions out of attempts, successful plays out of total
    """
    return np.random.binomial(n, p, size)

def geometric(p: float, size: Optional[int] = None) -> Union[int, np.ndarray]:
    """
    Geometric distribution (number of trials until first success)
    
    Args:
        p: Probability of success (0 to 1)
        size: Number of samples
    
    Returns:
        Random sample(s) from geometric distribution (integers)
    
    Use case: Plays until first down, attempts until touchdown
    """
    return np.random.geometric(p, size)

def negative_binomial(n: float, p: float, size: Optional[int] = None) -> Union[int, np.ndarray]:
    """
    Negative binomial distribution (trials until n successes)
    
    Args:
        n: Number of successes
        p: Probability of success
        size: Number of samples
    
    Returns:
        Random sample(s) from negative binomial distribution
    
    Use case: Plays needed to score n touchdowns, overdispersed counts
    """
    return np.random.negative_binomial(n, p, size)

def hypergeometric(ngood: int, nbad: int, nsample: int, size: Optional[int] = None) -> Union[int, np.ndarray]:
    """
    Hypergeometric distribution (sampling without replacement)
    
    Args:
        ngood: Number of "success" states in population
        nbad: Number of "failure" states in population
        nsample: Number of items sampled
        size: Number of samples
    
    Returns:
        Random sample(s) from hypergeometric distribution
    
    Use case: Selecting players from a roster, sampling without replacement
    """
    return np.random.hypergeometric(ngood, nbad, nsample, size)

# ==================== SPECIALTY FUNCTIONS ====================

def truncated_normal(mean: float, std_dev: float, lower: float, upper: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Normal distribution truncated to [lower, upper] bounds
    
    Args:
        mean: Mean of distribution
        std_dev: Standard deviation
        lower: Lower bound (inclusive)
        upper: Upper bound (inclusive)
        size: Number of samples
    
    Returns:
        Random sample(s) from truncated normal distribution
    
    Use case: Yards gained (can't be less than -20 or more than 99)
    """
    if size is None:
        while True:
            value = np.random.normal(mean, std_dev)
            if lower <= value <= upper:
                return value
    else:
        samples = []
        while len(samples) < size:
            value = np.random.normal(mean, std_dev)
            if lower <= value <= upper:
                samples.append(value)
        return np.array(samples)

def skew_normal(location: float, scale: float, skew: float, size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Approximation of skew-normal distribution using gamma and normal
    
    Args:
        location: Location parameter
        scale: Scale parameter
        skew: Skewness parameter (positive = right skew)
        size: Number of samples
    
    Returns:
        Random sample(s) from skewed distribution
    
    Use case: Yards gained on runs (slight right skew for occasional big gains)
    """
    # Approximate skew-normal using delta method
    if skew == 0:
        return np.random.normal(location, scale, size)
    
    # Use gamma for right skew
    if skew > 0:
        shape = 4 / (skew ** 2)
        samples = np.random.gamma(shape, scale / np.sqrt(shape), size)
        return location + samples - (shape * scale / np.sqrt(shape))
    else:
        # Flip for left skew
        shape = 4 / (skew ** 2)
        samples = np.random.gamma(shape, scale / np.sqrt(shape), size)
        return location - samples + (shape * scale / np.sqrt(shape))

def mixture_normal(means: list[float], std_devs: list[float], weights: list[float], size: Optional[int] = None) -> Union[float, np.ndarray]:
    """
    Mixture of normal distributions
    
    Args:
        means: List of means for each component
        std_devs: List of standard deviations
        weights: List of weights (must sum to 1)
        size: Number of samples
    
    Returns:
        Random sample(s) from mixture distribution
    
    Use case: Combining different play outcomes (e.g., 80% normal gain, 20% big play)
    """
    if size is None:
        # Choose component based on weights
        component = np.random.choice(len(means), p=weights)
        return np.random.normal(means[component], std_devs[component])
    else:
        # Choose components for each sample
        components = np.random.choice(len(means), size=size, p=weights)
        samples = np.array([np.random.normal(means[c], std_devs[c]) for c in components])
        return samples


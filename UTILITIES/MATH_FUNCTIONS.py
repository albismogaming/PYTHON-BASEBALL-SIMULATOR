import math


def sigmoid(x: float, steepness: float = 1.0, midpoint: float = 0.0) -> float:
    """
    Sigmoid (logistic) function for smooth probability transitions.
    
    Returns a value between 0 and 1 that smoothly transitions
    from 0 to 1 as x increases past the midpoint.
    
    Args:
        x: Input value
        steepness: Controls transition sharpness (higher = sharper)
                  Default 1.0 gives standard sigmoid
        midpoint: The x value where sigmoid = 0.5
                 Default 0.0 centers at origin
    
    Returns:
        Value between 0 and 1
    
    Examples:
        sigmoid(0, 1, 0)    -> 0.5   (at midpoint)
        sigmoid(5, 1, 0)    -> 0.993 (well above midpoint)
        sigmoid(-5, 1, 0)   -> 0.007 (well below midpoint)
        sigmoid(0, 10, 0)   -> 0.5   (steeper but still 0.5 at midpoint)
    
    Visualization:
        steepness = 0.5 (gradual)    steepness = 2.0 (sharp)
        
        1.0 |      ___---           1.0 |       __
            |    _/                     |      /
        0.5 |   /                   0.5 |     |
            |  /                        |    /
        0.0 |_/                     0.0 |___/
            └────────────                └────────
              midpoint                      midpoint
    """
    try:
        return 1 / (1 + math.exp(-steepness * (x - midpoint)))
    except OverflowError:
        # Handle extreme values
        return 0.0 if x < midpoint else 1.0


def inverse_sigmoid(x: float, steepness: float = 1.0, midpoint: float = 0.0) -> float:
    """
    Inverted sigmoid: 1 - sigmoid(x).
    
    Useful when you want high values of x to produce low output.
    Returns 1 at low x, 0 at high x.
    
    Args:
        x: Input value
        steepness: Controls transition sharpness
        midpoint: The x value where output = 0.5
    
    Returns:
        Value between 0 and 1 (inverted)
    
    Examples:
        inverse_sigmoid(0, 1, 0)  -> 0.5   (at midpoint)
        inverse_sigmoid(5, 1, 0)  -> 0.007 (high x gives low output)
        inverse_sigmoid(-5, 1, 0) -> 0.993 (low x gives high output)
    """
    return 1 - sigmoid(x, steepness, midpoint)


def linear_scale(value: float, in_min: float, in_max: float, 
                 out_min: float, out_max: float) -> float:
    """
    Linear scaling from one range to another.
    
    Maps value from [in_min, in_max] to [out_min, out_max].
    
    Args:
        value: Input value to scale
        in_min: Minimum of input range
        in_max: Maximum of input range
        out_min: Minimum of output range
        out_max: Maximum of output range
    
    Returns:
        Scaled value in output range
    
    Examples:
        linear_scale(5, 0, 10, 0, 100)    -> 50
        linear_scale(0, -10, 10, 0, 1)    -> 0.5
        linear_scale(7, 0, 10, -1, 1)     -> 0.4
    """
    if in_max == in_min:
        return out_min
    
    # Normalize to 0-1 range
    normalized = (value - in_min) / (in_max - in_min)
    
    # Scale to output range
    return out_min + normalized * (out_max - out_min)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Value clamped to [min_val, max_val]
    
    Examples:
        clamp(5, 0, 10)    -> 5
        clamp(-5, 0, 10)   -> 0
        clamp(15, 0, 10)   -> 10
    """
    return max(min_val, min(max_val, value))


def smooth_step(x: float, edge0: float = 0.0, edge1: float = 1.0) -> float:
    """
    Smooth interpolation between 0 and 1 using Hermite polynomial.
    
    Similar to sigmoid but with flat derivatives at edges.
    Useful for smooth transitions between discrete states.
    
    Args:
        x: Input value
        edge0: Lower edge (returns 0 when x <= edge0)
        edge1: Upper edge (returns 1 when x >= edge1)
    
    Returns:
        Value between 0 and 1
    
    Examples:
        smooth_step(0.5, 0, 1)  -> 0.5
        smooth_step(0.25, 0, 1) -> 0.156
        smooth_step(0.75, 0, 1) -> 0.844
    """
    # Clamp x to [edge0, edge1]
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    
    # Hermite interpolation: 3t² - 2t³
    return t * t * (3.0 - 2.0 * t)

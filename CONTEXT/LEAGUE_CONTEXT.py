from dataclasses import dataclass

@dataclass
class LeagueData:
    """
    League-average rates for all major outcomes.
    Used as baseline probabilities in odds ratio calculations.
    """
    year: int
    babip_factor: float
    base_factors: dict[str, float]
    hit_factors: dict[str, float]
    gbfb_factor: float
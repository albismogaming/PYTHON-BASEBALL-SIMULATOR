from dataclasses import dataclass

@dataclass
class LeagueData:
    """
    League-average rates for all major outcomes.
    Used as optional regression/normalization in probability modifiers.
    """
    year: int
    factors: dict[str, float]  # All outcome rates: SO, BB, HP, HR, IH, SL, DL, TL, BABIP, GBFB
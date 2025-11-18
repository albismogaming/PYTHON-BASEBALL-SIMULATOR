from dataclasses import dataclass
from typing import Dict

@dataclass
class Stadium:
    """
    Stadium with park-specific factors for all outcome types.
    Park factors are relative to league average (1.00).
    
    park_factors keys: 'SL', 'DL', 'TL', 'HR', 'GBFB'
    """
    stadium_name: str
    team_abbrev: str
    park_factors: Dict[str, float]  # Dictionary of park factor multipliers
    
    def __repr__(self):
        return f"Stadium({self.stadium_name}, {self.team_abbrev})"
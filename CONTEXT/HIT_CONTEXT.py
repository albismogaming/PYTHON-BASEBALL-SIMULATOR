from dataclasses import dataclass
from UTILITIES.ENUMS import HitDepths, HitSectors, HitTypes, Positions

@dataclass
class HitInfo:
    """Hit information determined by HitResultGenerator."""
    hit_type: HitTypes           # "FLY", "LINE", "GROUND", "POP"
    hit_sector: HitSectors       # HitSectors enum (LL, LF, LC, CF, RC, RF, RL)
    hit_depth: HitDepths            # "SHALLOW", "MEDIUM", "DEEP"
    hit_fielder: Positions       # Fielder position enum
    retrosheet_code: str = ""    # Retrosheet location code (e.g., "F89D", "G56", "L7S")
from dataclasses import dataclass
from typing import Dict


@dataclass
class Token:
    """
    Input token for at-bat simulation.
    Contains all context and probabilities needed to simulate a plate appearance.
    
    Probabilities are pre-calculated with all adjustments applied:
    - Base odds ratio (batter vs pitcher vs league)
    - Platoon advantage (split)
    - Park factors
    - Leverage/clutch (if applicable)
    """
    batter: object                          # Batter player object
    pitcher: object                         # Pitcher player object
    
    # Balls in play probabilities
    babip_prob: float                       # Probability of hit (vs out) on balls in play
    base_probs: Dict[str, float]            # Base advancement probabilities (SO, BB, HP, HR)
    hits_probs: Dict[str, float]            # Hit type distribution (SL, DL, TL, IH - sums to 1.0)
    outs_probs: Dict[str, float]            # Out type distribution (GO, FO, LO, PO - sums to 1.0)
    
    # Context
    game_situation: dict                    # Game context (inning, outs, runners, score)
    timestamp: str                          # When the token was created

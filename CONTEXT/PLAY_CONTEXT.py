from dataclasses import dataclass, field
from typing import Optional
from CONTEXT.PLAYER_CONTEXT import Player
from GAME_LOGIC.BASESTATE import BaseState
from UTILITIES.ENUMS import Macro, Micro, Pitch

@dataclass
class PlayResult:
    type: Macro | Micro | Pitch
    batter: Optional[Player] = None
    pitcher: Optional[Player] = None
    hits: int = 0
    runs: int = 0
    rbis: int = 0
    outs: int = 0
    errs: int = 0
    balls_delta: int = 0
    strikes_delta: int = 0
    bases_before: Optional[BaseState] = None
    bases_after: Optional[BaseState] = None
    scoring: list = field(default_factory=list)


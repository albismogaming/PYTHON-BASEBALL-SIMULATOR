from UTILITIES.ENUMS import Base
from CONTEXT.PLAYER_CONTEXT import Player
from typing import Optional, Tuple
from copy import deepcopy


class BaseState:
    def __init__(self, fst = None, snd = None, thd = None):
        self.fst = fst
        self.snd = snd
        self.thd = thd

    def copy(self):
        return BaseState(self.fst, self.snd, self.thd) 

    def deepcopy(self):
        return deepcopy(self)

    def to_tuple(self) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """Convert to immutable tuple of player IDs for hashing/caching.
        Much faster than dict for comparison and hashing."""
        return (
            self.fst.id if self.fst else None,
            self.snd.id if self.snd else None,
            self.thd.id if self.thd else None,
        )

    @classmethod
    def from_basestate(cls, other: 'BaseState'):
        """Copy from another BaseState (preferred over from_dict)."""
        return cls(fst=other.fst, snd=other.snd, thd=other.thd)

    def get(self, base):
        if base is Base.FST:
            return self.fst
        if base is Base.SND:
            return self.snd
        if base is Base.THD:
            return self.thd

    def set(self, base, player):
        if base is Base.FST:
            self.fst = player
        if base is Base.SND:
            self.snd = player
        if base is Base.THD:
            self.thd = player

    def clr(self, base):
        self.set(base, None)

    def clear_all(self):
        self.fst = self.snd = self.thd = None
    
    def is_empty(self) -> bool:
        """Check if all bases are empty (faster than to_dict check)."""
        return self.fst is None and self.snd is None and self.thd is None
    
    def __repr__(self):
        """Better debugging output."""
        return f"BaseState(1st={self.fst}, 2nd={self.snd}, 3rd={self.thd})"
    
    def __eq__(self, other):
        """Compare base states directly without dict conversion."""
        if not isinstance(other, BaseState):
            return False
        return (self.fst == other.fst and self.snd == other.snd and self.thd == other.thd)
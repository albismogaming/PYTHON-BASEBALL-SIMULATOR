from dataclasses import dataclass, field
from typing import List
from CONTEXT.STADIUM_CONTEXT import Stadium
from CONTEXT.PLAYER_CONTEXT import Player

@dataclass
class Team:
    """
    Team data container - holds roster and metadata.
    Pure data, no game-time behavior (lineup management, pitching changes).
    """
    # Identity
    name: str
    abbreviation: str
    market: str  # City/region (e.g., "Los Angeles", "New York")
    
    # Stadium
    stadium: Stadium
    
    # Roster
    batters: List[Player] = field(default_factory=list)
    pitchers: List[Player] = field(default_factory=list)
    
    # Record
    wins: int = 0
    losses: int = 0
    
    def __repr__(self):
        return f"{self.market} {self.name} ({self.abbreviation})"
    
    @property
    def full_name(self):
        """Get team's full name (market + name)."""
        return f"{self.market} {self.name}"
    
    @property
    def record(self):
        """Get team's win-loss record."""
        return f"{self.wins}-{self.losses}"
    
    @property
    def win_percentage(self):
        """Calculate team's winning percentage."""
        total = self.wins + self.losses
        return self.wins / total if total > 0 else 0.0
    
    def get_batter_by_position(self, position: str) -> List[Player]:
        """Get all batters at a specific position."""
        return [b for b in self.batters if b.position == position]
    
    def get_pitcher_by_id(self, player_id: int) -> Player:
        """Get pitcher by ID."""
        return next((p for p in self.pitchers if p.player_id == player_id))
    
    def get_batter_by_id(self, player_id: int) -> Player:
        """Get batter by ID."""
        return next((b for b in self.batters if b.player_id == player_id))

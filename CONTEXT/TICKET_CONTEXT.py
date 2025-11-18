from dataclasses import dataclass
from CONTEXT.PLAY_CONTEXT import PlayContext


@dataclass
class Ticket:
    """
    Ticket wrapping a PlayContext for execution and tracking.
    Simple container that holds the complete play information.
    """
    play_context: PlayContext
    
    def __post_init__(self):
        """Validate that play_context is provided."""
        if self.play_context is None:
            raise ValueError("Ticket must contain a PlayContext")
    
    @property
    def batter(self):
        """Quick access to batter from play context."""
        return self.play_context.batter
    
    @property
    def pitcher(self):
        """Quick access to pitcher from play context."""
        return self.play_context.pitcher
    
    @property
    def outcome(self):
        """Quick access to outcome description from play context."""
        return self.play_context.description
    
    @property
    def is_complete(self):
        """Check if the play is complete."""
        return self.play_context.is_complete
    
    def mark_complete(self):
        """Mark the ticket as complete."""
        self.play_context.is_complete = True
        self.play_context.at_bat_complete = True
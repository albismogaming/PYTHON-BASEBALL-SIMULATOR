from typing import List, Optional
from CONTEXT.PLAYER_CONTEXT import Player
from CONTEXT.TEAM_CONTEXT import Team

class TeamManager:
    """
    Manages game-time behavior for a team.
    
    Responsibilities:
    - Track current batter in lineup
    - Rotate batting order
    - Manage pitching changes
    - Track current pitcher
    """
    
    def __init__(self, team: Team):
        self.team = team
        
        # Batting order
        self.batting_order: List[Player] = []
        self.current_batter_index: int = 0
        
        # Pitching
        self.current_pitcher: Optional[Player] = None
        self.starting_pitcher: Optional[Player] = None
        self.available_relievers: List[Player] = []
        self.used_pitchers: List[Player] = []
    
    def set_batting_order(self, order: List[Player]):
        """
        Set the team's batting order for the game.
        
        Args:
            order: List of Player objects in batting order (1-9)
        """
        if len(order) != 9:
            raise ValueError(f"Batting order must have 9 players, got {len(order)}")
        
        self.batting_order = order
        self.current_batter_index = 0
    
    def get_next_batter(self) -> Player:
        """
        Get the next batter in the lineup and advance the index.
        
        Returns:
            Next Player in batting order
        """
        batter = self.batting_order[self.current_batter_index]
        self.current_batter_index = (self.current_batter_index + 1) % 9
        return batter
    
    def peek_next_batter(self) -> Player:
        """Get the next batter without advancing the index."""
        return self.batting_order[self.current_batter_index]
    
    def set_starting_pitcher(self, pitcher: Player):
        """
        Set the starting pitcher for the game.
        
        Args:
            pitcher: Player object from team's pitchers list
        """
        if pitcher not in self.team.pitchers:
            raise ValueError(f"{pitcher.full_name} not found in team's pitcher roster")
        
        self.current_pitcher = pitcher
        self.starting_pitcher = pitcher
        self.used_pitchers.append(pitcher)
        
        # Set available relievers (all pitchers except starter)
        self.available_relievers = [p for p in self.team.pitchers if p != pitcher]
    
    def change_pitcher(self, new_pitcher: Player):
        """
        Make a pitching change.
        
        Args:
            new_pitcher: Player object from available relievers
        """
        if new_pitcher not in self.available_relievers:
            raise ValueError(f"{new_pitcher.full_name} not available for relief")
        
        # Update current pitcher
        self.current_pitcher = new_pitcher
        self.used_pitchers.append(new_pitcher)
        self.available_relievers.remove(new_pitcher)
    
    def get_current_pitcher(self) -> Player:
        """Get the current pitcher."""
        if not self.current_pitcher:
            raise ValueError("No pitcher currently set")
        return self.current_pitcher
    
    def get_batting_order_string(self) -> str:
        """Get formatted string of batting order."""
        lines = []
        for idx, player in enumerate(self.batting_order, 1):
            lines.append(f"{idx}. {player.position:3s} {player.full_name}")
        return "\n".join(lines)
    
    def reset_lineup(self):
        """Reset lineup position to top of order."""
        self.current_batter_index = 0

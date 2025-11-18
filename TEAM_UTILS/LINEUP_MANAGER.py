import random
from typing import List
from CONTEXT.PLAYER_CONTEXT import Player


class LineupManager:
    """
    Manages batting lineup selection and rotation during a game.
    
    Responsibilities:
    - Select 9 players by position (handles DH fallback)
    - Generate batting order with randomness
    - Track current batter and rotate through lineup
    """
    
    def __init__(self, batters: List[Player]):
        """
        Initialize lineup manager with team's batters.
        
        Args:
            batters: List of Player objects (batters only, no pitchers)
        """
        self.batters = batters
        self.batting_order: List[Player] = []
        self.current_batter_index = 0
        self.players_used: List[Player] = []
        
        # Required defensive positions (DH is optional fallback)
        self.required_positions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
    
    def select_lineup(self, randomize: bool = True) -> List[Player]:
        """
        Select 9 batters for the lineup by position.
        
        Args:
            randomize: Whether to add randomness to lineup order
            
        Returns:
            List of 9 Player objects in batting order
        """
        selected = []
        used_players = []  # Use list instead of set since Player is unhashable
        
        # First, fill required defensive positions
        for position in self.required_positions:
            # Get available players at this position
            available = [p for p in self.batters 
                        if p.position == position and p not in used_players]
            
            if not available:
                raise ValueError(f"No available player found for position {position}")
            
            # Pick best available (or random if randomize=True)
            if randomize:
                player = random.choice(available)
            else:
                # Sort by batting average
                player = max(available, key=lambda p: p.average)
            
            selected.append(player)
            used_players.append(player)
        
        # 9th spot: Try to find a DH, otherwise use best available batter
        available_dh = [p for p in self.batters 
                       if p.position == 'DH' and p not in used_players]
        
        if available_dh:
            # DH exists - use it
            if randomize:
                player = random.choice(available_dh)
            else:
                player = max(available_dh, key=lambda p: p.average)
        else:
            # No DH - use best available position player as fallback
            available = [p for p in self.batters if p not in used_players]
            
            if not available:
                raise ValueError("Not enough batters to fill 9-man lineup")
            
            if randomize:
                player = random.choice(available)
            else:
                player = max(available, key=lambda p: p.average)
        
        selected.append(player)
        
        # Optionally shuffle batting order for more randomness
        if randomize:
            random.shuffle(selected)
        
        self.batting_order = selected
        self.current_batter_index = 0
        return selected
    
    def set_batting_order(self, order: List[Player]):
        """
        Manually set the batting order.
        
        Args:
            order: List of exactly 9 Player objects
        """
        if len(order) != 9:
            raise ValueError(f"Batting order must have 9 players, got {len(order)}")
        
        self.batting_order = order
        self.current_batter_index = 0
    
    def get_current_batter(self) -> Player:
        """
        Get the current batter without advancing the lineup.
        
        Returns:
            Current Player in batting order
        """
        if not self.batting_order:
            raise ValueError("Batting order not set - call select_lineup() first")
        
        return self.batting_order[self.current_batter_index]
    
    def get_next_batter(self) -> Player:
        """
        Get the next batter in the lineup and advance index.
        
        Returns:
            Next Player in batting order
        """
        if not self.batting_order:
            raise ValueError("Batting order not set - call select_lineup() first")
        
        batter = self.batting_order[self.current_batter_index]
        self.current_batter_index = (self.current_batter_index + 1) % 9
        
        # Track players who have batted
        if batter not in self.players_used:
            self.players_used.append(batter)
        
        return batter
    
    def peek_next_batter(self) -> Player:
        """Get the next batter without advancing index."""
        if not self.batting_order:
            raise ValueError("Batting order not set - call select_lineup() first")
        
        return self.batting_order[self.current_batter_index]
    
    def get_lineup_string(self) -> str:
        """Get formatted string of current batting order."""
        if not self.batting_order:
            return "No batting order set"
        
        lines = []
        for idx, player in enumerate(self.batting_order, 1):
            lines.append(f"{idx}. {player.position:3s} {player.full_name}")
        return "\n".join(lines)

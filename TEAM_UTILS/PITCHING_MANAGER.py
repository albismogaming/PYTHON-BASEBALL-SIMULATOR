import random
from typing import List, Optional, Dict
from CONTEXT.PLAYER_CONTEXT import Player


# Simple pitching limits
STARTER_PITCH_LIMIT = 95
STARTER_INNING_LIMIT = 6.0
RELIEVER_PITCH_LIMIT = 30
RELIEVER_INNING_LIMIT = 2.0


class PitchingManager:
    """ Manages pitching staff during a game. """
    
    def __init__(self, pitchers: List[Player]):
        """
        Initialize pitching manager with team's pitchers.
        
        Args:
            pitchers: List of Player objects (pitchers only)
        """
        self.all_pitchers = pitchers
        
        # Split starters and relievers by position
        self.starting_pitchers = [p for p in pitchers if p.position == 'SP']
        self.relief_pitchers = [p for p in pitchers if p.position == 'RP']
        
        # Game state
        self.current_pitcher: Optional[Player] = None
        self.starting_pitcher: Optional[Player] = None
        self.pitchers_used: List[Player] = []
    
    def select_starting_pitcher(self, randomize: bool = True) -> Player:
        """
        Select starting pitcher for the game.
        
        Args:
            randomize: If True, randomly select from starters. If False, pick best by ERA/average.
            
        Returns:
            Selected starting pitcher
        """
        if not self.starting_pitchers:
            raise ValueError("No starting pitchers available")
        
        if randomize:
            pitcher = random.choice(self.starting_pitchers)
        else:
            # Pick best starter by average (lower is better for pitchers)
            pitcher = min(self.starting_pitchers, key=lambda p: p.average)
        
        self.current_pitcher = pitcher
        self.starting_pitcher = pitcher
        self.pitchers_used.append(pitcher)
        
        return pitcher

    def change_pitcher(self, new_pitcher: Optional[Player] = None) -> Player:
        """
        Make a pitching change.
        
        Args:
            new_pitcher: Specific pitcher to bring in. If None, selects best available reliever.
            
        Returns:
            New pitcher brought in
        """
        if new_pitcher:
            # Manual pitcher selection
            if new_pitcher in self.pitchers_used:
                raise ValueError(f"{new_pitcher.full_name} has already pitched in this game")
            
            if new_pitcher not in self.all_pitchers:
                raise ValueError(f"{new_pitcher.full_name} not on pitching staff")
        else:
            # Auto-select best available reliever
            new_pitcher = self.get_best_available_reliever()
            
            if not new_pitcher:
                # No relievers left - use unused starter as long relief
                available_starters = self.get_available_starters()
                if not available_starters:
                    raise ValueError("No pitchers available for relief")
                new_pitcher = available_starters[0]
        
        # Make the change
        self.current_pitcher = new_pitcher
        self.pitchers_used.append(new_pitcher)
        
        return new_pitcher
    
    def get_current_pitcher(self) -> Player:
        """Get the current pitcher."""
        if not self.current_pitcher:
            raise ValueError("No pitcher currently set - call select_starting_pitcher() first")
        return self.current_pitcher
    
    def get_available_relievers(self) -> List[Player]:
        """Get list of relievers who haven't pitched yet."""
        return [p for p in self.relief_pitchers if p not in self.pitchers_used]
    
    def get_available_starters(self) -> List[Player]:
        """Get list of starters who haven't pitched yet."""
        return [p for p in self.starting_pitchers if p not in self.pitchers_used]
    
    def has_available_relievers(self) -> bool:
        """Check if any relievers are still available."""
        return len(self.get_available_relievers()) > 0
    
    def get_best_available_reliever(self) -> Optional[Player]:
        """
        Get the best available relief pitcher based on performance.
        
        Returns:
            Best available reliever or None if none available
        """
        available = self.get_available_relievers()
        if not available:
            return None
        
        # Sort by average (lower is better for pitchers)
        return min(available, key=lambda p: p.average)
    
    def get_pitcher_stats(self, pitcher: Player) -> Dict[str, int]:
        """
        Get current game stats for a pitcher.
        
        Args:
            pitcher: The pitcher to get stats for
            
        Returns:
            Dictionary of pitcher stats
        """
        from TEAM_UTILS.STATS_MANAGER import StatsManager
        stats = StatsManager.get_pitcher_stats(pitcher)
        
        if not stats:
            return {
                'outs_recorded': 0,
                'innings_pitched': 0,
                'pitches_thrown': 0,
                'runs_allowed': 0,
                'hits_allowed': 0,
                'walks_issued': 0,
                'strikeouts': 0
            }
        
        return {
            'outs_recorded': stats.get('Outs', 0),
            'innings_pitched': stats.get('IP', 0.0),
            'pitches_thrown': stats.get('PT', 0),
            'runs_allowed': stats.get('R', 0),
            'hits_allowed': stats.get('H', 0),
            'walks_issued': stats.get('BB', 0),
            'strikeouts': stats.get('SO', 0)
        }
    
    def should_change_pitcher(self) -> bool:
        """
        Simple check: change pitcher if they've exceeded pitch count or innings limit.
        
        Returns:
            True if pitching change is needed
        """
        if not self.current_pitcher:
            return False
        
        # Check if any relievers available
        if not self.has_available_relievers():
            return False
        
        pitcher = self.current_pitcher
        stats = self.get_pitcher_stats(pitcher)
        
        # Check limits based on position
        if pitcher.position == 'SP':
            return (stats['pitches_thrown'] >= STARTER_PITCH_LIMIT or 
                    stats['innings_pitched'] >= STARTER_INNING_LIMIT)
        else:  # RP
            return (stats['pitches_thrown'] >= RELIEVER_PITCH_LIMIT or 
                    stats['innings_pitched'] >= RELIEVER_INNING_LIMIT)
    
    def reset_for_new_game(self):
        """Reset pitching manager for a new game."""
        self.current_pitcher = None
        self.starting_pitcher = None
        self.pitchers_used = []
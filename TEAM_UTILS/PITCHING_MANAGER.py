import random
from typing import List, Optional, Dict
from CONTEXT.PLAYER_CONTEXT import Player


# Pitching threshold constants
class PitchingThresholds:
    """Constants for pitching change decisions"""
    # Starting pitcher limits
    STARTER_PITCHES_LIMIT = 95
    STARTER_INNINGS_LIMIT = 6.0
    STARTER_RUNS_LIMIT = 4
    STARTER_HITS_LIMIT = 10
    STARTER_STRUGGLE_LIMIT = 4.0
    
    # Extended starter limits (blowouts/low leverage)
    EXTENDED_STARTER_PITCHES_LIMIT = 110
    EXTENDED_STARTER_INNINGS_LIMIT = 7.0
    EXTENDED_STARTER_RUNS_LIMIT = 6
    
    # Reliever limits
    RELIEVER_PITCHES_LIMIT = 30
    RELIEVER_INNINGS_LIMIT = 2.0
    RELIEVER_RUNS_LIMIT = 3
    RELIEVER_HITS_LIMIT = 4
    
    # Extended reliever limits (blowouts/low leverage)
    EXTENDED_RELIEVER_PITCHES_LIMIT = 40
    EXTENDED_RELIEVER_INNINGS_LIMIT = 3.0
    EXTENDED_RELIEVER_RUNS_LIMIT = 4


class PitchingManager:
    """
    Manages pitching staff during a game.
    
    Responsibilities:
    - Select starting pitcher
    - Manage bullpen (relief pitchers)
    - Track current pitcher and pitchers used
    - Determine when to make pitching changes
    """
    
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
        return {
            'outs_recorded': pitcher.pit_stats.get('outs_recorded', 0),
            'pitches_thrown': pitcher.pit_stats.get('pitches_thrown', 0),
            'runs_allowed': pitcher.pit_stats.get('runs_allowed', 0),
            'hits_allowed': pitcher.pit_stats.get('hits', 0),
            'walks_issued': pitcher.pit_stats.get('walks', 0),
            'strikeouts': pitcher.pit_stats.get('strikeouts', 0)
        }
    
    def calculate_innings_pitched(self, outs_recorded: int) -> float:
        """
        Calculate innings pitched from outs recorded.
        
        Args:
            outs_recorded: Total outs recorded
            
        Returns:
            Innings pitched as a float (e.g., 5.2 for 5 and 2/3 innings)
        """
        full_innings = outs_recorded // 3
        additional_outs = outs_recorded % 3
        return full_innings + (additional_outs / 3.0)
    
    def calculate_struggle_index(self, stats: Dict[str, int]) -> float:
        """
        Calculate a struggle index based on pitcher performance.
        Higher values indicate more struggle.
        
        Args:
            stats: Dictionary of pitcher stats
            
        Returns:
            Struggle index value
        """
        runs_weight = 0.5
        hits_weight = 0.2
        walks_weight = 0.1
        
        return (runs_weight * stats['runs_allowed'] + 
                hits_weight * stats['hits_allowed'] + 
                walks_weight * stats['walks_issued'])
    
    def can_finish_inning(self, pitcher: Player, outs_in_inning: int, 
                         pitch_threshold: float = 0.9) -> bool:
        """
        Determine if pitcher should be allowed to finish the current inning.
        
        Args:
            pitcher: The current pitcher
            outs_in_inning: Number of outs recorded in current inning (0-2)
            pitch_threshold: Percentage of pitch limit (default 0.9 = 90%)
            
        Returns:
            True if pitcher should finish the inning
        """
        if outs_in_inning == 2:  # Last out of inning
            stats = self.get_pitcher_stats(pitcher)
            
            if pitcher.position == 'SP':
                return stats['pitches_thrown'] < PitchingThresholds.STARTER_PITCHES_LIMIT * pitch_threshold
            else:  # RP
                return stats['pitches_thrown'] < PitchingThresholds.RELIEVER_PITCHES_LIMIT * pitch_threshold
        
        return False
    
    def _check_thresholds(self, stats: Dict[str, int], innings_pitched: float, 
                         position: str, is_extended: bool, high_leverage: bool) -> bool:
        """
        Helper method to check if pitcher has exceeded thresholds.
        
        Args:
            stats: Pitcher statistics
            innings_pitched: Innings pitched so far
            position: 'SP' or 'RP'
            is_extended: Whether to use extended thresholds (blowout/trailing)
            high_leverage: Whether this is a high-leverage situation
            
        Returns:
            True if thresholds are exceeded and change is needed
        """
        if position == 'SP':
            if is_extended:
                # Extended starter limits
                if (stats['pitches_thrown'] >= PitchingThresholds.EXTENDED_STARTER_PITCHES_LIMIT or
                    innings_pitched >= PitchingThresholds.EXTENDED_STARTER_INNINGS_LIMIT or
                    stats['runs_allowed'] >= PitchingThresholds.EXTENDED_STARTER_RUNS_LIMIT):
                    return True
            else:
                # Normal starter limits
                if (stats['pitches_thrown'] >= PitchingThresholds.STARTER_PITCHES_LIMIT or
                    innings_pitched >= PitchingThresholds.STARTER_INNINGS_LIMIT or
                    stats['runs_allowed'] >= PitchingThresholds.STARTER_RUNS_LIMIT or
                    stats['hits_allowed'] >= PitchingThresholds.STARTER_HITS_LIMIT or
                    self.calculate_struggle_index(stats) >= PitchingThresholds.STARTER_STRUGGLE_LIMIT):
                    return True
                
                # High-leverage adjustments (tighter leash)
                if high_leverage:
                    if (stats['pitches_thrown'] >= PitchingThresholds.STARTER_PITCHES_LIMIT * 0.8 or
                        stats['runs_allowed'] >= PitchingThresholds.STARTER_RUNS_LIMIT * 0.75):
                        return True
        
        elif position == 'RP':
            if is_extended:
                # Extended reliever limits
                if (stats['pitches_thrown'] >= PitchingThresholds.EXTENDED_RELIEVER_PITCHES_LIMIT or
                    innings_pitched >= PitchingThresholds.EXTENDED_RELIEVER_INNINGS_LIMIT or
                    stats['runs_allowed'] >= PitchingThresholds.EXTENDED_RELIEVER_RUNS_LIMIT):
                    return True
            else:
                # Normal reliever limits
                if (stats['pitches_thrown'] >= PitchingThresholds.RELIEVER_PITCHES_LIMIT or
                    innings_pitched >= PitchingThresholds.RELIEVER_INNINGS_LIMIT or
                    stats['runs_allowed'] >= PitchingThresholds.RELIEVER_RUNS_LIMIT or
                    stats['hits_allowed'] >= PitchingThresholds.RELIEVER_HITS_LIMIT):
                    return True
                
                # High-leverage adjustments (tighter leash)
                if high_leverage:
                    if (stats['pitches_thrown'] >= PitchingThresholds.RELIEVER_PITCHES_LIMIT * 0.8 or
                        stats['runs_allowed'] >= PitchingThresholds.RELIEVER_RUNS_LIMIT * 0.66):
                        return True
        
        return False
    
    def should_change_pitcher(self, 
                            current_inning: int,
                            current_outs: int,
                            score_differential: int = 0,
                            team_is_leading: bool = False) -> bool:
        """
        Comprehensive method to determine if a pitching change should be made.
        
        Args:
            current_inning: Current inning number (1-9+)
            current_outs: Total outs in the game (0-53+)
            score_differential: Absolute difference in score
            team_is_leading: Whether this team is currently leading
            
        Returns:
            True if pitching change is recommended
        """
        if not self.current_pitcher:
            return False
        
        pitcher = self.current_pitcher
        stats = self.get_pitcher_stats(pitcher)
        innings_pitched = self.calculate_innings_pitched(stats['outs_recorded'])
        
        # Calculate outs in current inning
        outs_in_inning = current_outs % 3
        
        # Check if at last out of inning - allow finishing if close to limit
        if outs_in_inning == 2 and self.can_finish_inning(pitcher, outs_in_inning):
            return False
        
        # Determine game situation
        blowout = (score_differential >= 6 if current_inning >= 7 else score_differential >= 8)
        high_leverage = (current_inning >= 8 and score_differential <= 3)
        team_trailing = not team_is_leading and score_differential > 0
        
        # Use extended limits in blowouts or when trailing badly
        is_extended = blowout or (team_trailing and score_differential > 5)
        
        # Check thresholds using helper method
        return self._check_thresholds(stats, innings_pitched, pitcher.position, 
                                     is_extended, high_leverage)
    
    def reset_for_new_game(self):
        """Reset pitching manager for a new game."""
        self.current_pitcher = None
        self.starting_pitcher = None
        self.pitchers_used = []
    
    def get_pitching_staff_string(self) -> str:
        """Get formatted string of pitching staff."""
        lines = []
        
        lines.append("STARTING PITCHERS:")
        for pitcher in self.starting_pitchers:
            used = "✓" if pitcher in self.pitchers_used else " "
            lines.append(f"  [{used}] {pitcher.full_name} - AVG: {pitcher.average:.3f}")
        
        lines.append("\nRELIEF PITCHERS:")
        for pitcher in self.relief_pitchers:
            used = "✓" if pitcher in self.pitchers_used else " "
            lines.append(f"  [{used}] {pitcher.full_name} - AVG: {pitcher.average:.3f}")
        
        return "\n".join(lines)

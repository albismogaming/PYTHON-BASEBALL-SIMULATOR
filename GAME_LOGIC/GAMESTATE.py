from UTILITIES.FILE_PATHS import *
from UTILITIES.ENUMS import *

class GameState:
    def __init__(self, away_team, home_team):
        self.away_team = away_team
        self.home_team = home_team
        
        self.current_inning = 1
        self.inninghalf = InningHalf.TOP

        self.batting_team = away_team if self.inninghalf == InningHalf.TOP else home_team
        self.fielding_team = home_team if self.inninghalf == InningHalf.TOP else away_team
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.bases = {Base.FST: None, Base.SND: None, Base.THD: None}

        self.hits_hit = 0
        self.runs_scored = 0
        self.errors_made = 0
        self.pickoffs = 0
        self.is_walk_off = False
        self.is_inning_over = False
        self.is_game_over = False

        self.stats = {
            'away_team': {'score': 0, 'hits': 0, 'errors': 0, 'score_by_inning': []},
            'home_team': {'score': 0, 'hits': 0, 'errors': 0, 'score_by_inning': []}
        }
    
    @property
    def current_team(self):
        """Get the key for the current batting team ('away_team' or 'home_team')."""
        return 'away_team' if self.inninghalf == InningHalf.TOP else 'home_team'
    
    # ============================================================
    # SCORE UPDATE METHODS
    # ============================================================
    
    def add_stats(self, hits=0, runs=0, outs=0):
        """
        Add hits, runs, and outs in a single call (performance optimization).
        
        Args:
            hits: Number of hits to add
            runs: Number of runs to add
            outs: Number of outs to add
        """
        if hits:
            self.stats[self.current_team]['hits'] += hits
            self.hits_hit += hits
        if runs:
            self.stats[self.current_team]['score'] += runs
            self.runs_scored += runs
        if outs:
            self.outs += outs
    
    def add_error(self, num_errors=1, team=None):
        """
        Add error(s) to a team's total (for fielding team).
        
        Args:
            num_errors: Number of errors to add (default 1)
            team: Team key. If None, uses the current fielding team
        """
        if team is None:
            # Error is charged to the fielding team (opposite of batting team)
            team = 'home_team' if self.inninghalf == InningHalf.TOP else 'away_team'
        
        self.stats[team]['errors'] += num_errors
    
    # ============================================================
    # INNING RESET METHODS
    # ============================================================
    
    def reset_half_inning(self):
        """
        Reset state for a new half-inning.
        Clears outs, bases, count, and per-play tracking.
        """
        self.outs = 0
        self.balls = 0
        self.strikes = 0
        self.bases = {Base.FST: None, Base.SND: None, Base.THD: None}
        self.hits_hit = 0
        self.runs_scored = 0
        self.pickoffs = 0
        self.is_inning_over = False
        
        # Ensure score_by_inning has an entry for current inning (initialize with 0 if needed)
        team = self.current_team
        while len(self.stats[team]['score_by_inning']) < self.current_inning:
            self.stats[team]['score_by_inning'].append(0)
    
    def reset_inning(self):
        """
        Reset state for a new inning.
        Clears outs, bases, count, and advances to next inning.
        """
        self.reset_half_inning()
        self.current_inning += 1
        self.inninghalf = InningHalf.TOP
        
        # Update batting and pitching teams for new inning
        self.batting_team = self.away_team if self.inninghalf == InningHalf.TOP else self.home_team
        self.pitching_team = self.home_team if self.inninghalf == InningHalf.TOP else self.away_team
    
    def toggle_inning_half(self):
        """
        Toggle between top and bottom of inning.
        Updates batting/pitching teams and resets half-inning state.
        """
        self.inninghalf = InningHalf.BOT if self.inninghalf == InningHalf.TOP else InningHalf.TOP
        self.reset_half_inning()
        
        # Update batting and pitching teams
        self.batting_team = self.away_team if self.inninghalf == InningHalf.TOP else self.home_team
        self.pitching_team = self.home_team if self.inninghalf == InningHalf.TOP else self.away_team
    
    # ============================================================
    # GAME CONTEXT METHODS
    # ============================================================
    
    def get_situation_dict(self):
        """
        Get current game situation as a dictionary for token generation.
        
        Returns:
            Dictionary with game context (inning, outs, score, runners, etc.)
        """
        return {
            'inning': self.current_inning,
            'inning_half': self.inninghalf.value,
            'outs': self.outs,
            'balls': self.balls,
            'strikes': self.strikes,
            'first_base': self.bases[Base.FST] is not None,
            'second_base': self.bases[Base.SND] is not None,
            'third_base': self.bases[Base.THD] is not None,
            'away_score': self.stats['away_team']['score'],
            'home_score': self.stats['home_team']['score'],
            'score_diff': abs(self.stats['away_team']['score'] - self.stats['home_team']['score'])
        }
    
    def get_base_state(self) -> int:
        """
        Get bitwise representation of the current base state.
        
        Returns:
            int: Bitwise base state where:
                - Bit 0 (value 1): Runner on 1st
                - Bit 1 (value 2): Runner on 2nd
                - Bit 2 (value 4): Runner on 3rd
                
        Examples:
            0 = empty bases
            1 = runner on 1st only
            3 = runners on 1st and 2nd
            7 = bases loaded
        """
        state = 0
        if self.bases[Base.FST] is not None:
            state |= 1  # Set bit 0
        if self.bases[Base.SND] is not None:
            state |= 2  # Set bit 1
        if self.bases[Base.THD] is not None:
            state |= 4  # Set bit 2
        return state
    
    def get_fielder(self, hit_info):
        """
        Get the defensive player who fields the ball based on hit_info.
        
        Args:
            hit_info: HitInfo object with hit_fielder (Positions enum)
            
        Returns:
            Player object at the fielding position, or None if not found
        """
        if not hit_info or not hasattr(hit_info, 'hit_fielder'):
            return None
        
        # Map Positions enum to position string
        position_map = {
            Positions._SP: 'SP',  # Pitcher
            Positions._RP: 'RP',  # Relief pitcher (treated as pitcher)
            Positions._1B: '1B',
            Positions._2B: '2B',
            Positions._3B: '3B',
            Positions._SS: 'SS',
            Positions._LF: 'LF',
            Positions._CF: 'CF',
            Positions._RF: 'RF'
        }
        
        position_str = position_map.get(hit_info.hit_fielder)
        if not position_str:
            return None
        
        # Special case: Pitcher fielding (SP/RP) - get current pitcher
        if position_str in ['SP', 'RP']:
            # Return the current pitcher from pitching team
            # This requires accessing the pitching manager, which should be passed separately
            # For now, we'll return None and let the caller handle pitcher lookups
            return None
        
        # Search fielding team's batters for player at this position
        for player in self.fielding_team.batters:
            if player.position == position_str:
                return player
        
        return None
    
    def can_game_end(self):
        """
        Check if the game can end based on current state.
        
        Returns:
            bool: True if game can end (walk-off or regulation complete)
        """
        # Walk-off already triggered
        if self.is_walk_off:
            self.is_game_over = True
            return True
        
        # Top of 9th or later: if home team is ahead after top half, game can end
        # (skip bottom of inning)
        if self.current_inning >= 9 and self.inninghalf == InningHalf.TOP:
            if self.outs >= 3 and self.stats['home_team']['score'] > self.stats['away_team']['score']:
                self.is_game_over = True
                return True
        
        # Bottom of 9th or later: if away team is ahead and bottom half ends, game over
        if self.current_inning >= 9 and self.inninghalf == InningHalf.BOT:
            if self.outs >= 3 and self.stats['away_team']['score'] > self.stats['home_team']['score']:
                self.is_game_over = True
                return True
        
        return False

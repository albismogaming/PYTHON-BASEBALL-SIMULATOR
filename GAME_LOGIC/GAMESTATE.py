from UTILITIES.SETTINGS import *
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
    # OUTS UPDATE METHODS
    # ============================================================
    
    def add_out(self, num_outs=1):
        """
        Add out(s) to the current count.
        
        Args:
            num_outs: Number of outs to add (default 1)
        """
        self.outs += num_outs
        if self.outs > 3:
            self.outs = 3
    
    def reset_outs(self):
        """Reset outs to 0 (used when inning changes)."""
        self.outs = 0
    
    # ============================================================
    # SCORE UPDATE METHODS
    # ============================================================
    
    def add_run(self, runs=1, team=None):
        """
        Add run(s) to a team's score.
        
        Args:
            runs: Number of runs to add (default 1)
            team: Team key ('away_team' or 'home_team'). If None, uses current batting team
        """
        if team is None:
            team = self.current_team
        
        self.stats[team]['score'] += runs
        
        # Update score_by_inning
        while len(self.stats[team]['score_by_inning']) < self.current_inning:
            self.stats[team]['score_by_inning'].append(0)
        
        self.stats[team]['score_by_inning'][self.current_inning - 1] += runs
        
        # Track runs scored this play
        self.runs_scored += runs
    
    def add_run_with_walkoff_check(self, runs=1):
        """
        Add run(s) with walk-off scenario handling.
        Limits runs to only what's needed to win if it's a walk-off situation.
        
        Args:
            runs: Number of runs that would score
        """
        team = self.current_team
        
        # Check if walk-off scenario
        if (self.inninghalf == InningHalf.BOT and 
            self.current_inning >= INNINGS and 
            self.stats["home_team"]["score"] <= self.stats["away_team"]["score"]):
            
            # Calculate runs needed to win
            runs_needed = (self.stats["away_team"]["score"] + 1) - self.stats["home_team"]["score"]
            runs = min(runs, runs_needed)
            
            # Add the runs
            self.add_run(runs, team)
            
            # Set walk-off
            self.is_walk_off = True
            self.is_inning_over = True
            self.is_game_over = True
        else:
            # Normal run scoring
            self.add_run(runs, team)
    
    # ============================================================
    # HITS AND ERRORS UPDATE METHODS
    # ============================================================
    
    def add_hit(self, num_hits=1, team=None):
        """
        Add hit(s) to a team's total.
        
        Args:
            num_hits: Number of hits to add (default 1)
            team: Team key. If None, uses current batting team
        """
        if team is None:
            team = self.current_team
        
        self.stats[team]['hits'] += num_hits
        self.hits_hit += num_hits
    
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
    
    def should_end_game(self):
        """
        Check if the game should end due to walk-off or completed innings.
        
        Returns:
            bool: True if game should end, False otherwise
        """
        # Walk-off scenario ends game immediately
        if self.is_walk_off:
            return True
        
        # Top of 9th or later: game ends if home team is ahead
        if self.current_inning >= INNINGS and self.inninghalf == InningHalf.TOP:
            if self.stats['home_team']['score'] > self.stats['away_team']['score']:
                return True
            return False
        
        # Bottom of 9th or later: game ends if away team is ahead
        if self.current_inning >= INNINGS and self.inninghalf == InningHalf.BOT:
            if self.stats['away_team']['score'] > self.stats['home_team']['score']:
                return True
        
        return False



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
    
    def get_base_state(self) -> str:
        """
        Get a string representation of the current base state.
        
        Returns:
            str: Base state code (e.g., "1_1_0" for runners on 1st and 2nd)
        """
        base_tuple = (
            self.bases[Base.FST] is not None,
            self.bases[Base.SND] is not None,
            self.bases[Base.THD] is not None
        )
        
        base_states = {
            (True, True, True): "1_1_1",
            (True, False, False): "1_0_0",
            (False, True, False): "0_1_0",
            (False, False, True): "0_0_1",
            (True, True, False): "1_1_0",
            (True, False, True): "1_0_1",
            (False, True, True): "0_1_1",
            (False, False, False): "0_0_0"
        }
        
        return base_states.get(base_tuple, "0_0_0")
    
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
        if self.current_inning >= INNINGS and self.inninghalf == InningHalf.TOP:
            if self.outs >= 3 and self.stats['home_team']['score'] > self.stats['away_team']['score']:
                self.is_game_over = True
                return True
        
        # Bottom of 9th or later: if away team is ahead and bottom half ends, game over
        if self.current_inning >= INNINGS and self.inninghalf == InningHalf.BOT:
            if self.outs >= 3 and self.stats['away_team']['score'] > self.stats['home_team']['score']:
                self.is_game_over = True
                return True
        
        return False

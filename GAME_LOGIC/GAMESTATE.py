from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.FILE_PATHS import *
from UTILITIES.ENUMS import *
from GAME_LOGIC.BASESTATE import BaseState


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
        self.bases = BaseState()

        self.hits_hit = 0
        self.runs_scored = 0
        self.errors_made = 0
        self.pickoffs = 0
        self.is_walk_off = False
        self.is_inning_over = False
        self.is_game_over = False

        # Direct score tracking for performance (avoid dictionary lookups)
        self.away_score = 0
        self.home_score = 0

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

    def apply_result(self, result: PlayResult):
        # 1. Update bases - now directly using BaseState (no dict conversion!)
        if result.bases_after:
            self.bases = result.bases_after
        else:
            # Fallback: shouldn't happen if outcomes set bases_after correctly
            print(f"WARNING: {result.type} outcome did not set bases_after!")

        # 2. Update count
        self.balls += result.balls_delta
        self.strikes += result.strikes_delta

        if result.hits:
            self.stats[self.current_team]['hits'] += result.hits
            self.hits_hit += result.hits
        if result.runs:
            self.stats[self.current_team]['score'] += result.runs
            self.runs_scored += result.runs
            # Update direct score tracking
            if self.inninghalf == InningHalf.TOP:
                self.away_score += result.runs
            else:
                self.home_score += result.runs
        if result.outs:
            self.outs += result.outs
        if result.errs:
            self.stats[self.current_team]['errors'] += result.errs
            self.errors_made += result.errs
    
    # ============================================================
    # INNING RESET METHODS
    # ============================================================
    
    def reset_count(self):
        """ Reset balls and strikes to zero. """
        self.balls = 0
        self.strikes = 0

    def reset_half_inning(self):
        """
        Reset state for a new half-inning.
        Clears outs, bases, count, and per-play tracking.
        """
        self.outs = 0
        self.balls = 0
        self.strikes = 0
        self.bases = BaseState()  # Clear bases only at start of NEW half-inning
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
        self.reset_half_inning()  # This now clears bases at the half-inning transition
        
        # Update batting and pitching teams
        self.batting_team = self.away_team if self.inninghalf == InningHalf.TOP else self.home_team
        self.pitching_team = self.home_team if self.inninghalf == InningHalf.TOP else self.away_team
    
    # ============================================================
    # GAME CONTEXT METHODS
    # ============================================================
    
    def check_walk_off(self):
        """
        Check if the current state results in a walk-off win for the home team.
        Sets is_walk_off and is_game_over flags if conditions are met.
        """
        if self.inninghalf == InningHalf.BOT and self.current_inning >= 9:
            if self.home_score > self.away_score:
                self.is_walk_off = True
                self.is_game_over = True
                return True
        return False
    
    def get_base_state(self) -> int:
        """ Get bitwise representation of the current base state.
        
        Examples:
            0 = empty bases
            1 = runner on 1st only
            3 = runners on 1st and 2nd
            7 = bases loaded
        """
        state = 0
        if self.bases.get(Base.FST) is not None:
            state |= 1  # Set bit 0
        if self.bases.get(Base.SND) is not None:
            state |= 2  # Set bit 1
        if self.bases.get(Base.THD) is not None:
            state |= 4  # Set bit 2
        return state
    
    def can_game_end(self):
        """ Check if the game can end based on current state. """       
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
    
    def should_end(self, is_macro_outcome: bool = False):
        """
        Check if current action or half-inning should end.
        
        Args:
            is_macro_outcome: True if this is the final macro outcome event
        
        Returns:
            Tuple (should_end_half_inning: bool, should_break_atbat: bool)
        """
        if self.outs >= 3 or self.can_game_end():
            return True, is_macro_outcome  # End half-inning, break at-bat if macro
        return False, False

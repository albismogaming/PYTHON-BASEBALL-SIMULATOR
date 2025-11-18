from UTILITIES.SETTINGS import *
from UTILITIES.ENUMS import *
import numpy as np


class GameStateChecks:
    """Handles all game state checks and validations."""
    
    def __init__(self, game_state):
        """
        Initialize the GameStateChecks with a reference to the game state.
        
        Args:
            game_state: The GameState object to perform checks on
        """
        self.game_state = game_state
    
    # ============================================================
    # INNING AND GAME COMPLETION CHECKS
    # ============================================================
    
    def should_end_inning(self):
        """
        Check if the inning should end (3 outs recorded).
        
        Returns:
            bool: True if inning should end, False otherwise
        """
        return self.game_state.outs >= 3

    
    def should_end_game(self):
        """
        Check if the game should end due to walk-off or completed innings.
        
        Returns:
            bool: True if game should end, False otherwise
        """
        gs = self.game_state
        
        # Walk-off scenario ends game immediately
        if gs.is_walk_off:
            return True
        
        # Top of 9th or later: game ends if home team is ahead
        if gs.current_inning >= INNINGS and gs.inninghalf == InningHalf.TOP:
            if gs.stats['home_team']['score'] > gs.stats['away_team']['score']:
                return True
            return False
        
        # Bottom of 9th or later: game ends if away team is ahead
        if gs.current_inning >= INNINGS and gs.inninghalf == InningHalf.BOT:
            if gs.stats['away_team']['score'] > gs.stats['home_team']['score']:
                return True
        
        return False
    
    def is_walk_off_scenario(self):
        """
        Check if current situation is a walk-off scenario.
        Home team batting in 9th+ inning and scoring would give them the lead.
        
        Returns:
            bool: True if walk-off scenario, False otherwise
        """
        gs = self.game_state
        return (
            gs.inninghalf == InningHalf.BOT and 
            gs.current_inning >= INNINGS and 
            gs.stats["home_team"]["score"] <= gs.stats["away_team"]["score"]
        )
    
    def get_walk_off_runs_needed(self, runs_scored):
        """
        Calculate how many runs are needed for a walk-off win.
        
        Args:
            runs_scored: Number of runs that would score on the play
            
        Returns:
            int: Minimum runs needed to win (capped at runs_scored)
        """
        gs = self.game_state
        
        if not self.is_walk_off_scenario():
            return runs_scored
        
        runs_needed = (gs.stats["away_team"]["score"] + 1) - gs.stats["home_team"]["score"]
        return min(runs_scored, runs_needed)
    
    # ============================================================
    # SCORE AND TEAM STATUS CHECKS
    # ============================================================
    
    def get_score_difference(self):
        """
        Get the absolute score difference between teams.
        
        Returns:
            int: Absolute difference in scores
        """
        gs = self.game_state
        return abs(gs.stats['home_team']['score'] - gs.stats['away_team']['score'])
    
    def is_close_game(self, threshold=2):
        """
        Check if the score difference is within a threshold.
        
        Args:
            threshold: Maximum score difference to consider game "close"
            
        Returns:
            bool: True if score difference <= threshold
        """
        return self.get_score_difference() <= threshold
    
    def is_team_trailing_by_two(self):
        """
        Check if either team is trailing by two or more runs.
        
        Returns:
            bool: True if score difference >= 2
        """
        return self.get_score_difference() >= 2
    
    def is_late_game(self, inning_threshold=7):
        """
        Check if game is in late innings.
        
        Args:
            inning_threshold: Inning number to consider "late game"
            
        Returns:
            bool: True if in late game situation
        """
        return self.game_state.current_inning >= inning_threshold
    
    def is_extra_innings(self):
        """
        Check if the game is in extra innings.
        
        Returns:
            bool: True if past regulation innings
        """
        return self.game_state.current_inning > INNINGS
    
    def get_leading_team(self):
        """
        Determine which team is currently leading.
        
        Returns:
            str: 'away_team', 'home_team', or 'tied'
        """
        gs = self.game_state
        home_score = gs.stats['home_team']['score']
        away_score = gs.stats['away_team']['score']
        
        if home_score > away_score:
            return 'home_team'
        elif away_score > home_score:
            return 'away_team'
        return 'tied'
    
    # ============================================================
    # BASE STATE CHECKS
    # ============================================================
       
    def has_runners_on(self):
        """
        Check if there are any runners on base.
        
        Returns:
            bool: True if any base is occupied
        """
        gs = self.game_state
        return any([
            gs.bases[Base.FST] is not None,
            gs.bases[Base.SND] is not None,
            gs.bases[Base.THD] is not None
        ])
    
    def has_runner_on_base(self, base):
        """
        Check if a specific base is occupied.
        
        Args:
            base: Base enum (Base.FST, Base.SND, or Base.THD)
            
        Returns:
            bool: True if base is occupied
        """
        return self.game_state.bases[base] is not None
    
    def bases_loaded(self):
        """
        Check if bases are loaded (all three bases occupied).
        
        Returns:
            bool: True if all bases occupied
        """
        gs = self.game_state
        return all([
            gs.bases[Base.FST] is not None,
            gs.bases[Base.SND] is not None,
            gs.bases[Base.THD] is not None
        ])
    
    def is_scoring_position(self):
        """
        Check if there's a runner in scoring position (2nd or 3rd).
        
        Returns:
            bool: True if runner on 2nd or 3rd
        """
        gs = self.game_state
        return (gs.bases[Base.SND] is not None or gs.bases[Base.THD] is not None)
    
    def get_runner_count(self):
        """
        Count the number of runners currently on base.
        
        Returns:
            int: Number of occupied bases (0-3)
        """
        gs = self.game_state
        return sum([
            gs.bases[Base.FST] is not None,
            gs.bases[Base.SND] is not None,
            gs.bases[Base.THD] is not None
        ])
    
    def get_runners_list(self):
        """
        Get a list of all runners currently on base with their positions.
        
        Returns:
            list: List of tuples (base, runner_object)
        """
        gs = self.game_state
        runners = []
        for base in [Base.FST, Base.SND, Base.THD]:
            if gs.bases[base] is not None:
                runners.append((base, gs.bases[base]))
        return runners
    
    # ============================================================
    # SITUATIONAL EVENT CHECKS
    # ============================================================
    
    def check_for_wild_pitch_or_passed_ball(self):
        """
        Randomly determine if a wild pitch or passed ball occurs.
        
        Returns:
            str: 'W' for wild pitch, 'P' for passed ball, or None
        """
        rand_value = np.random.random()
        if rand_value < WILDPITCH:
            return 'W'
        elif rand_value < PASSBALL:
            return 'P'
        return None
    
    def check_for_pickoff(self):
        """
        Determine if a pickoff attempt should occur based on game situation.
        Considers runner presence, speed, and outs.
        
        Returns:
            str: '1' for pickoff at first, '2' for pickoff at second, or None
        """
        gs = self.game_state
        base_state = gs.get_base_state()
        
        runner_on_first = gs.bases.get(Base.FST)
        runner_on_second = gs.bases.get(Base.SND)
        
        # No pickoff possible without runners on 1st or 2nd
        if base_state not in ['1_0_0', '0_1_0', '1_1_0']:
            return None
        
        # Initialize pickoff probabilities
        pickoff_prob_first = PICKOFF_1ST if runner_on_first else 0
        pickoff_prob_second = PICKOFF_2ND if runner_on_second else 0
        
        # Adjust for runner speed (faster runners draw more pickoff attempts)
        if runner_on_first and hasattr(runner_on_first, 'speed'):
            pickoff_prob_first += runner_on_first.speed * 0.004
        if runner_on_second and hasattr(runner_on_second, 'speed'):
            pickoff_prob_second += runner_on_second.speed * 0.002
        
        # Adjust for outs (more pickoffs with fewer outs)
        outs_adjustment = {0: 0.03, 1: 0.02, 2: 0.01}[gs.outs]
        if runner_on_first:
            pickoff_prob_first += outs_adjustment
        if runner_on_second:
            pickoff_prob_second += outs_adjustment
        
        # Determine pickoff attempt
        if runner_on_first and hasattr(runner_on_first, 'speed') and runner_on_first.speed > 5:
            if np.random.random() < pickoff_prob_first:
                return '1'
        
        if runner_on_second and hasattr(runner_on_second, 'speed') and runner_on_second.speed > 5:
            if np.random.random() < pickoff_prob_second:
                return '2'
        
        return None
    
    def check_for_stealing(self, pitch_type):
        """
        Check if a steal attempt should occur based on game situation.
        Returns specific marker based on pitch type.
        
        Args:
            pitch_type: Type of pitch ('B', 'S', or 'C')
            
        Returns:
            str: 'T' (steal on ball), 'U' (steal on swinging strike), 
                 'V' (steal on called strike), or None
        """
        gs = self.game_state
        
        runner_on_first = gs.bases.get(Base.FST)
        runner_on_second = gs.bases.get(Base.SND)
        
        # Only steal with runner on first, no one on second, and fast runner
        if not runner_on_first or runner_on_second:
            return None
        
        if not hasattr(runner_on_first, 'speed') or runner_on_first.speed < 5:
            return None
        
        steal_prob = STEALING_PROB
        
        # Late-game, close score adjustment
        if gs.current_inning > 6 and self.is_close_game(2):
            steal_prob += 0.05
        
        # Adjust for outs
        if gs.outs == 0:
            steal_prob += 0.03
        elif gs.outs == 1:
            steal_prob += 0.04
        elif gs.outs == 2:
            steal_prob += 0.05
        
        # Attempt steal
        if np.random.random() < steal_prob:
            if pitch_type == 'B':
                return 'T'  # Steal on ball
            elif pitch_type == 'S':
                return 'U'  # Steal on swinging strike
            elif pitch_type == 'C':
                return 'V'  # Steal on called strike
        
        return None
    
    # ============================================================
    # COUNT VALIDATION
    # ============================================================
    
    def is_full_count(self):
        """
        Check if count is full (3 balls, 2 strikes).
        
        Returns:
            bool: True if count is 3-2
        """
        gs = self.game_state
        return gs.balls == 3 and gs.strikes == 2
    
    def is_hitters_count(self):
        """
        Check if count favors the hitter (more balls than strikes).
        
        Returns:
            bool: True if hitter's count
        """
        gs = self.game_state
        return gs.balls > gs.strikes
    
    def is_pitchers_count(self):
        """
        Check if count favors the pitcher (more strikes than balls).
        
        Returns:
            bool: True if pitcher's count
        """
        gs = self.game_state
        return gs.strikes > gs.balls
    
    def is_two_strike_count(self):
        """
        Check if batter has two strikes.
        
        Returns:
            bool: True if 2 strikes
        """
        return self.game_state.strikes == 2
    
    def is_three_ball_count(self):
        """
        Check if count has three balls.
        
        Returns:
            bool: True if 3 balls
        """
        return self.game_state.balls == 3
    
    # ============================================================
    # DEFENSIVE SITUATION CHECKS
    # ============================================================
    
    def is_double_play_possible(self):
        """
        Check if a double play is possible (runner on first, less than 2 outs).
        
        Returns:
            bool: True if double play possible
        """
        gs = self.game_state
        return gs.outs < 2 and gs.bases[Base.FST] is not None
    
    def is_force_out_at_second(self):
        """
        Check if there's a force play at second base.
        
        Returns:
            bool: True if force at second
        """
        return self.game_state.bases[Base.FST] is not None
    
    def is_force_out_at_third(self):
        """
        Check if there's a force play at third base.
        
        Returns:
            bool: True if force at third
        """
        gs = self.game_state
        return gs.bases[Base.FST] is not None and gs.bases[Base.SND] is not None
    
    def is_force_out_at_home(self):
        """
        Check if there's a force play at home plate.
        
        Returns:
            bool: True if force at home (bases loaded)
        """
        return self.bases_loaded()
    
    # ============================================================
    # STRATEGIC SITUATION CHECKS
    # ============================================================
    
    def is_sac_bunt_situation(self):
        """
        Check if it's a typical sacrifice bunt situation.
        Runner on first or second, less than 2 outs.
        
        Returns:
            bool: True if sac bunt situation
        """
        gs = self.game_state
        if gs.outs >= 2:
            return False
        return gs.bases[Base.FST] is not None or gs.bases[Base.SND] is not None
    
    def is_sac_fly_situation(self):
        """
        Check if a sacrifice fly could score a run.
        Runner on third, less than 2 outs.
        
        Returns:
            bool: True if sac fly can score
        """
        gs = self.game_state
        return gs.outs < 2 and gs.bases[Base.THD] is not None
    
    def is_infield_in_situation(self):
        """
        Check if defense might play infield in.
        Close game, late innings, runner on third, less than 2 outs.
        
        Returns:
            bool: True if infield in situation
        """
        if not self.is_close_game(1):
            return False
        if not self.is_late_game(7):
            return False
        gs = self.game_state
        return gs.outs < 2 and gs.bases[Base.THD] is not None
    
    def is_intentional_walk_situation(self):
        """
        Check if strategic intentional walk makes sense.
        First base open, power hitter, close game situation.
        
        Returns:
            bool: True if IBB situation
        """
        gs = self.game_state
        if gs.bases[Base.FST] is not None:
            return False
        if not self.is_close_game(2):
            return False
        return self.is_late_game(7)








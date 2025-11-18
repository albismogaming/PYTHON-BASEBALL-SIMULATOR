from UTILITIES.SETTINGS import *
from UTILITIES.ENUMS import PitchResult, Outcome
import numpy as np


class PitchSequenceGenerator:
    """Generates pitch sequences using Markov chain transitions.

    Stateless generator - produces realistic pitch sequences based only on final outcome.
    All methods are static, no instance state needed.
    """

    # Starting pitch probabilities (0-0 count)
    FIRST_PITCH_PROBS = {
        PitchResult.B.value: 0.35,  # Ball
        PitchResult.C.value: 0.40,  # Called strike
        PitchResult.S.value: 0.15,  # Swinging strike
        PitchResult.F.value: 0.10   # Foul ball
    }
    
    # Transition probabilities based on count state (balls, strikes)
    # Keys are PitchResult enum values: B=Ball, C=Called Strike, S=Swinging Strike, F=Foul
    TRANSITIONS = {
        # Behind in count (more balls than strikes)
        (1, 0): {"B": 0.38, "C": 0.38, "S": 0.14, "F": 0.10},
        (2, 0): {"B": 0.40, "C": 0.36, "S": 0.14, "F": 0.10},
        (3, 0): {"B": 0.42, "C": 0.35, "S": 0.13, "F": 0.10},
        (2, 1): {"B": 0.38, "C": 0.37, "S": 0.15, "F": 0.10},
        (3, 1): {"B": 0.40, "C": 0.35, "S": 0.15, "F": 0.10},
        
        # Even count
        (1, 1): {"B": 0.36, "C": 0.38, "S": 0.16, "F": 0.10},
        (2, 2): {"B": 0.37, "C": 0.36, "S": 0.17, "F": 0.10},
        
        # Ahead in count (more strikes than balls)
        (0, 1): {"B": 0.32, "C": 0.42, "S": 0.16, "F": 0.10},
        (0, 2): {"B": 0.30, "C": 0.40, "S": 0.18, "F": 0.12},
        (1, 2): {"B": 0.33, "C": 0.39, "S": 0.17, "F": 0.11},
        
        # Full count (3-2)
        (3, 2): {"B": 0.38, "C": 0.36, "S": 0.16, "F": 0.10}
    }
    
    @staticmethod
    def get_next_pitch(balls, strikes, outcome_type=None):
        """
        Get next pitch result based on current count using Markov chain.
        
        Args:
            balls: Current ball count
            strikes: Current strike count
            outcome_type: Type of final outcome ("WALK", "STRIKEOUT", "IN_PLAY")
                         Used to prevent impossible transitions
            
        Returns:
            str: PitchResult enum value (B, C, S, F)
        """
        count_state = (balls, strikes)
        
        # Use first pitch probabilities if starting fresh
        if count_state == (0, 0):
            probs = PitchSequenceGenerator.FIRST_PITCH_PROBS.copy()
        # Use count-specific probabilities
        elif count_state in PitchSequenceGenerator.TRANSITIONS:
            probs = PitchSequenceGenerator.TRANSITIONS[count_state].copy()
        else:
            # Default to balanced probabilities for unexpected states
            probs = {"B": 0.35, "C": 0.38, "S": 0.17, "F": 0.10}
        
        # CRITICAL: With 2 strikes, can't generate called/swinging strikes (except for strikeouts)
        if strikes == 2 and outcome_type != "SO":
            # Convert strike probabilities to fouls
            strike_prob = probs.get("C", 0) + probs.get("S", 0)
            probs["F"] = probs.get("F", 0) + strike_prob
            probs["C"] = 0
            probs["S"] = 0
        
        # Terminal state logic: prevent impossible outcomes on 3-2 count
        if count_state == (3, 2) and outcome_type == "IN_PLAY":
            # Ball in play on 3-2: can't be a ball (would be walk) or strike (would be strikeout)
            # Only fouls allowed
            probs = {"F": 1.0}
        
        # With 3 balls and not a walk outcome, reduce ball probability
        if balls == 3 and outcome_type != "BB":
            # Shift ball probability to other pitches
            ball_prob = probs.get("B", 0)
            probs["B"] = ball_prob * 0.3  # Reduce significantly
            # Distribute to fouls and remaining strikes
            extra = ball_prob * 0.7
            if "F" in probs:
                probs["F"] += extra * 0.7
            remaining = extra * 0.3
            count_others = sum(1 for k in ["C", "S"] if probs.get(k, 0) > 0)
            if count_others > 0:
                per_other = remaining / count_others
                for k in ["C", "S"]:
                    if probs.get(k, 0) > 0:
                        probs[k] += per_other
        
        # Normalize probabilities
        total = sum(probs.values())
        if total > 0:
            probs = {k: v / total for k, v in probs.items()}
        
        # Select pitch based on probabilities
        outcomes = list(probs.keys())
        probabilities = list(probs.values())
        return np.random.choice(outcomes, p=probabilities)
    
    @staticmethod
    def generate_sequence(outcome):
        """
        Generate a pitch sequence for a given at-bat outcome using Markov chain.
        
        Args:
            outcome: The final outcome of the at-bat (Outcome enum)
            
        Returns:
            list: Sequence of pitch codes leading to the outcome
        """
        # Convert outcome enum to name string
        outcome_name = outcome.name if hasattr(outcome, 'name') else str(outcome)
        
        # Special case: HBP on first pitch
        if outcome_name == "HP":
            return [PitchResult.H.value]
        
        # Special case: Walk - must get to 4 balls
        if outcome_name == "BB":
            return PitchSequenceGenerator._generate_walk_sequence()
        
        # Special case: Strikeout - must get to 3 strikes
        if outcome_name == "SO":
            return PitchSequenceGenerator._generate_strikeout_sequence()
        
        # Ball in play outcomes (HR, SL, DL, TL, GO, FO, LO, PO, IH)
        return PitchSequenceGenerator._generate_in_play_sequence()
    
    @staticmethod
    def _generate_walk_sequence():
        """Generate a realistic sequence leading to a walk (4 balls).
        
        Guarantees the sequence ends with the 4th ball.
        Max sequence length: 14 pitches.
        """
        sequence = []
        balls = 0
        strikes = 0
        MAX_PITCHES = 14
        
        while balls < 4 and len(sequence) < MAX_PITCHES:
            pitch = PitchSequenceGenerator.get_next_pitch(balls, strikes, outcome_type="BB")
            sequence.append(pitch)
            
            if pitch == "B":
                balls += 1
            elif pitch in ["C", "S"]:
                if strikes < 2:
                    strikes += 1
            elif pitch == "F":
                if strikes < 2:
                    strikes += 1
                # Foul with 2 strikes doesn't increment
        
        # Force walk if hit max pitches
        if balls < 4:
            sequence.append("B")
        
        return sequence
    
    @staticmethod
    def _generate_strikeout_sequence():
        """Generate a realistic sequence leading to a strikeout (3 strikes).
        
        Guarantees the sequence ends with a strike (either "C" or "S").
        Max sequence length: 14 pitches.
        """
        sequence = []
        balls = 0
        strikes = 0
        MAX_PITCHES = 14
        
        while strikes < 3 and len(sequence) < MAX_PITCHES:
            pitch = PitchSequenceGenerator.get_next_pitch(balls, strikes, outcome_type="SO")
            
            if pitch == "B":
                balls += 1
                sequence.append(pitch)
            elif pitch == "C" or pitch == "S":
                strikes += 1
                sequence.append(pitch)
            elif pitch == "F":
                # Add foul ball
                sequence.append(pitch)
                # Only increment strikes if below 2 strikes
                if strikes < 2:
                    strikes += 1
                # With 2 strikes, keep generating pitches until we get a strike
        
        # Force strikeout if hit max pitches
        if strikes < 3:
            sequence.append("S")
        
        # Sequence ends with the 3rd strike (last pitch will be "C" or "S")
        return sequence
    
    @staticmethod
    def _generate_in_play_sequence():
        """Generate a sequence for ball put in play (hit or out).
        
        On 3-2 counts, prevents generating walks (4 balls) or strikeouts (3 strikes).
        Guarantees sequence ends with 'X'.
        Max sequence length: 14 pitches.
        """
        sequence = []
        balls = 0
        strikes = 0
        MAX_PITCHES = 14
        
        # Generate pitches until ball is put in play
        # Ball in play more likely on certain counts
        while True:
            pitch = PitchSequenceGenerator.get_next_pitch(balls, strikes, outcome_type="IN_PLAY")
            sequence.append(pitch)
            
            # Update count based on pitch type
            if pitch == "B":
                balls += 1
            elif pitch in ["C", "S"]:
                if strikes < 2:
                    strikes += 1
            elif pitch == "F":
                if strikes < 2:
                    strikes += 1
                # Foul with 2 strikes doesn't increment
            # Note: On 3-2 count with IN_PLAY outcome, get_next_pitch only returns "F" (foul)
            
            # Check if ball should be put in play
            if PitchSequenceGenerator._should_put_ball_in_play(balls, strikes, len(sequence)):
                sequence.append(PitchResult.X.value)  # Ball in play
                break
            
            # Force in play if hit max pitches
            if len(sequence) >= MAX_PITCHES:
                sequence.append(PitchResult.X.value)
                break
        
        return sequence
    
    @staticmethod
    def _should_put_ball_in_play(balls, strikes, pitch_count):
        """
        Determine if ball should be put in play based on count and pitch number.
        
        Args:
            balls: Current ball count
            strikes: Current strike count
            pitch_count: Number of pitches so far
            
        Returns:
            bool: True if ball should be put in play
        """
        # Base probability increases with pitch count
        base_prob = 0.15 + (pitch_count * 0.05)
        
        # Adjust based on count
        if strikes == 2:
            base_prob += 0.15  # More likely to put in play with 2 strikes
        
        if balls >= 2:
            base_prob += 0.10  # More aggressive with 2+ balls
        
        # Hitter's counts increase contact probability
        if balls > strikes:
            base_prob += 0.10
        
        # Cap at 50% per pitch
        base_prob = min(base_prob, 0.50)
        
        return np.random.random() < base_prob



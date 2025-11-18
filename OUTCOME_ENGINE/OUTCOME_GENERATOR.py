from UTILITIES.RANDOM import *
from OUTCOME_ENGINE.OUTCOME_BUILDER import *
import numpy as np

class OutcomeGenerator:
    @staticmethod
    def generate_final_outcome(token):
        """Generate the final outcome of the at-bat based on probabilities."""
        rand_val = np.random.rand()
        cumulative = 0.0

        so_rate = token.base_probs.get('SO', 0)
        bb_rate = token.base_probs.get('BB', 0)
        hp_rate = token.base_probs.get('HP', 0)
        hr_rate = token.base_probs.get('HR', 0)

        # Check each outcome using cumulative probability ranges
        cumulative += so_rate
        if rand_val < cumulative:
            token.outcome = Outcome.SO
            return token.outcome

        cumulative += bb_rate
        if rand_val < cumulative:
            token.outcome = Outcome.BB
            return token.outcome
        
        cumulative += hp_rate
        if rand_val < cumulative:
            token.outcome = Outcome.HP
            return token.outcome
        
        cumulative += hr_rate
        if rand_val < cumulative:
            token.outcome = Outcome.HR
            return token.outcome
        
        # Remaining probability = ball in play
        outcome = OutcomeGenerator.generate_in_play_outcome(token)
        token.outcome = outcome
        return outcome

    @staticmethod
    def generate_in_play_outcome(token):
        """
        Determine the specific outcome when the ball is put in play.
        
        Uses BABIP to determine hit vs out, then selects specific type from distribution.
        """
        rand_val = np.random.rand()
        
        # Use BABIP to determine hit vs out
        if rand_val < token.babip_prob:
            # Hit - select type from hits distribution
            # Keys should already be enum member names: 'SL', 'DL', 'TL', 'IH'
            outcomes = list(token.hits_probs.keys())
            weights = list(token.hits_probs.values())
            selected = str(np.random.choice(outcomes, p=weights))
            return Outcome[selected]  # Access enum by member name: Outcome['SL'], Outcome['DL'], etc.
        else:
            # Out - select type from outs distribution
            # Keys should be enum member names: 'GO', 'FO', 'LO', 'PO'
            outcomes = list(token.outs_probs.keys())
            weights = list(token.outs_probs.values())
            selected = str(np.random.choice(outcomes, p=weights))
            return Outcome[selected]  # Access enum by member name: Outcome['GO'], Outcome['FO'], etc.
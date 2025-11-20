from UTILITIES.RANDOM import get_random
from UTILITIES.ENUMS import Outcome


class OutcomeGenerator:
    @staticmethod
    def generate_final_outcome(outcome_probs, babip_prob):
        """Generate the final outcome of the at-bat based on probabilities."""
        rand_val = get_random()

        # Check base outcomes in order (SO, BB, HP, HR)
        cumulative = 0.0
        cumulative += outcome_probs['SO']
        if rand_val < cumulative:
            return Outcome.SO
        
        cumulative += outcome_probs['BB']
        if rand_val < cumulative:
            return Outcome.BB
        
        cumulative += outcome_probs['HP']
        if rand_val < cumulative:
            return Outcome.HP
        
        cumulative += outcome_probs['HR']
        if rand_val < cumulative:
            return Outcome.HR
        
        # Remaining probability = ball in play
        return OutcomeGenerator.generate_in_play_outcome(outcome_probs, babip_prob)

    @staticmethod
    def generate_in_play_outcome(outcome_probs, babip_prob):
        """
        Determine the specific outcome when the ball is put in play.
        
        Uses BABIP to determine hit vs out, then selects specific type from distribution.
        """
        # Use BABIP to determine hit vs out
        if get_random() < babip_prob:
            # Hit - check each type cumulatively
            rand = get_random()
            hit_total = outcome_probs['IH'] + outcome_probs['SL'] + outcome_probs['DL'] + outcome_probs['TL']
            
            cumulative = 0.0
            cumulative += outcome_probs['IH'] / hit_total
            if rand < cumulative:
                return Outcome.IH
            
            cumulative += outcome_probs['SL'] / hit_total
            if rand < cumulative:
                return Outcome.SL
            
            cumulative += outcome_probs['DL'] / hit_total
            if rand < cumulative:
                return Outcome.DL
            
            return Outcome.TL  # Last option
        else:
            # Out - check each type cumulatively
            rand = get_random()
            out_total = outcome_probs['GO'] + outcome_probs['FO'] + outcome_probs['LO'] + outcome_probs['PO']
            
            cumulative = 0.0
            cumulative += outcome_probs['GO'] / out_total
            if rand < cumulative:
                return Outcome.GO
            
            cumulative += outcome_probs['FO'] / out_total
            if rand < cumulative:
                return Outcome.FO
            
            cumulative += outcome_probs['LO'] / out_total
            if rand < cumulative:
                return Outcome.LO
            
            return Outcome.PO  # Last option
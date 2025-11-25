from ATBAT.ATBAT_FACTORY import AtBatFactory
from ATBAT.ATBAT_PITCHES import PitchCountGenerator
from ATBAT.ATBAT_PROBS import ProbabilityModifier
from TEAM_UTILS.STATS_MANAGER import StatsManager
from UTILITIES.ENUMS import Outcome
from UTILITIES.RANDOM import get_random
from DATA_LOADERS.LEAGUE_STATS_LOADER import LeagueLoader

class AtBatSimulator:
    """ Step-by-step at-bat simulation with live probability calculation. """
    
    # Pre-defined outcome lists (avoid recreating on every at-bat)
    _BASE = (('SO', Outcome.SO), ('BB', Outcome.BB), ('HP', Outcome.HP), ('HR', Outcome.HR))
    _HITS = (('IH', Outcome.IH), ('SL', Outcome.SL), ('DL', Outcome.DL), ('TL', Outcome.TL))
    _OUTS = (('GO', Outcome.GO), ('FO', Outcome.FO), ('LO', Outcome.LO), ('PO', Outcome.PO))
    
    @staticmethod
    def step_initialize_matchup(batting_lineup_mgr, pitching_team_mgr):
        """ Get the current batter and pitcher, then calculate base matchup probabilities. """      

        batter = batting_lineup_mgr.get_current_batter()
        pitcher = pitching_team_mgr.get_current_pitcher()
        
        # Calculate base probabilities for all outcomes (before modifiers)
        base_probs = {}
        
        base_probs['BA'] = ProbabilityModifier.calculate_probability(
            batter.base_stats['BA'], pitcher.base_stats['BA']
        )

        # Base outcomes (SO, BB, HP, HR)
        for outcome in ['SO', 'BB', 'HP', 'HR']:
            batter_prob = batter.base_stats[outcome]
            pitcher_prob = pitcher.base_stats[outcome]
            base_probs[outcome] = ProbabilityModifier.calculate_probability(batter_prob, pitcher_prob)
        
        # Hit outcomes (IH, SL, DL, TL)
        for outcome in ['IH', 'SL', 'DL', 'TL']:
            batter_prob = batter.hits_stats[outcome]
            pitcher_prob = pitcher.hits_stats[outcome]
            base_probs[outcome] = ProbabilityModifier.calculate_probability(batter_prob, pitcher_prob)
        
        # Out outcomes (GO, FO, LO, PO)
        for outcome in ['GO', 'FO', 'LO', 'PO']:
            batter_prob = batter.outs_stats[outcome]
            pitcher_prob = pitcher.outs_stats[outcome]
            base_probs[outcome] = ProbabilityModifier.calculate_probability(batter_prob, pitcher_prob)
        
        return batter, pitcher, base_probs

    @classmethod
    def generate_matchup_probs(cls, gamestate, batter, pitcher, base_probs):
        """ Apply modifiers to base matchup probabilities. """
        # Start with base probabilities (already calculated in initialize_matchup)
        outcome_probs = base_probs
        
        # Get BABIP from base probabilities
        babip_prob = outcome_probs['BA']
        
        # Apply league factors for normalization (if available and non-neutral)
        league_factors = LeagueLoader.get_league_factors()
        if league_factors:
            outcome_probs = ProbabilityModifier.apply_modifiers(outcome_probs, league_factors)
        
        # Apply park factors if present
        park_factors = gamestate.home_team.park_factors
        if park_factors:
            outcome_probs = ProbabilityModifier.apply_modifiers(outcome_probs, park_factors)
        
        # Apply platoon splits with variability
        platoon_mods = ProbabilityModifier.get_platoon_split_modifiers(batter, pitcher, use_variability=True)
        if platoon_mods:
            outcome_probs = ProbabilityModifier.apply_modifiers(outcome_probs, platoon_mods)
        
        return outcome_probs, babip_prob

    @classmethod
    def generate_final_outcome(cls, outcome_probs, babip_prob):
        """Generate the final outcome of the at-bat based on probabilities."""
        rand_val = get_random()
        cumulative = 0.0
        
        # Check base outcomes in order (SO, BB, HP, HR)
        for outcome_key, outcome_enum in cls._BASE:
            cumulative += outcome_probs[outcome_key]
            if rand_val < cumulative:
                return outcome_enum
        
        # Ball in play - use a separate random call to determine hit vs out with BABIP
        if get_random() < babip_prob:
            # Hits - select from hit distribution
            hit_total = outcome_probs['IH'] + outcome_probs['SL'] + outcome_probs['DL'] + outcome_probs['TL']
            hit_cum = 0.0
            
            for outcome_key, outcome_enum in cls._HITS:
                hit_cum += outcome_probs[outcome_key] / hit_total
                if rand_val < hit_cum:
                    return outcome_enum
            return Outcome.SL  # Fallback to last hit outcome
        else:
            # Outs - select from out distribution
            out_total = outcome_probs['GO'] + outcome_probs['FO'] + outcome_probs['LO'] + outcome_probs['PO']
            out_cum = 0.0
            
            for outcome_key, outcome_enum in cls._OUTS:
                out_cum += outcome_probs[outcome_key] / out_total
                if rand_val < out_cum:
                    return outcome_enum
            return Outcome.PO  # Fallback to last out outcome

    @classmethod
    def simulate_at_bat(cls, gamestate, batter, pitcher, base_probs):
        """ Simulate a complete at-bat: apply modifiers, determine outcome, and execute it. """
        # Apply modifiers to base probabilities
        outcome_probs, modified_babip = cls.generate_matchup_probs(gamestate, batter, pitcher, base_probs)
        
        # Generate outcome
        outcome = cls.generate_final_outcome(outcome_probs, modified_babip)
        pitches_thrown = PitchCountGenerator.generate_pitches_thrown(outcome)
        
        # Execute outcome
        result = AtBatFactory.execute_outcome(outcome=outcome, gamestate=gamestate, batter=batter, pitcher=pitcher)
        
        # Extract result values once (avoid repeated .get() calls)
        hits = result['hits']
        runs = result['runs']
        outs = result['outs']
        rbis = result['rbis']
        
        # Update game state with the result
        gamestate.add_stats(hits=hits, runs=runs, outs=outs)
        
        # Record stats using the outcome data
        runs_scored = 1 if outcome == Outcome.HR else 0  # Only batter scores on HR
        StatsManager.record_at_bat(batter, pitcher, outcome, pitches_thrown, runs_scored, rbis, outs)
    
    @staticmethod
    def step_advance_batter(batting_lineup_mgr):
        """ Step 5: Advance to the next batter in the lineup. """       
        batting_lineup_mgr.get_next_batter()
        
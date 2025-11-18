from ATBAT.ATBAT_PROBS import ProbabilityCalculator
from CONTEXT.STADIUM_CONTEXT import Stadium
from CONTEXT.TOKEN_CONTEXT import Token
from OUTCOME_ENGINE.OUTCOME_BUILDER import OutcomeBuilder
from datetime import datetime


class MatchupTokenGenerator:
    """
    Generates MatchupToken objects for at-bat simulation.
    Combines batter/pitcher data with game situation to create complete context.
    """
    
    @staticmethod
    def generate_token(batter, pitcher, league, gamestate):
        """
        Generate a token with all probabilities calculated and adjusted.
        
        Pipeline: base odds ratio → split advantage → park factors → normalize
        """
        # Calculate BABIP (single value)
        babip_prob = ProbabilityCalculator.calculate_base_probability(
            batter.b_babip, pitcher.p_babip, league.babip_factor
        )
        
        # Build base outcome probabilities (SO, BB, HP, HR)
        base_probs = OutcomeBuilder.build_base_probabilities(
            batter.bat_base_stats, pitcher.pit_base_stats, league.base_factors
        )
        
        # Build hit type distribution (SL, DL, TL, IH)
        hits_probs = OutcomeBuilder.build_hits_distribution(
            batter.bat_hit_stats, pitcher.pit_hit_stats, league.hit_factors
        )
        
        # Build out type distribution (GO, FO, LO, PO)
        outs_probs = OutcomeBuilder.build_outs_distribution(
            batter.b_gbfb, pitcher.p_gbfb, league.gbfb_factor
        )
        
        # Apply split advantage to base outcomes and hits
        split_multiplier = ProbabilityCalculator.calculate_split_advantage(batter, pitcher)
        base_probs = {k: v * split_multiplier for k, v in base_probs.items()}
        hits_probs = {k: v * split_multiplier for k, v in hits_probs.items()}
        
        # Apply park factors (stadium-specific adjustments)
        park_factors = gamestate.home_team.stadium.park_factors
        base_probs = ProbabilityCalculator.apply_park_factors(base_probs, park_factors)
        hits_probs = ProbabilityCalculator.apply_park_factors(hits_probs, park_factors)
        
        # Normalize hit and out distributions (these are conditional probabilities)
        hits_total = sum(hits_probs.values())
        if hits_total > 0:
            hits_probs = {k: v / hits_total for k, v in hits_probs.items()}
        
        # Outs already normalized by OutcomeBuilder
        
        return Token(
            batter=batter,
            pitcher=pitcher,
            babip_prob=babip_prob,
            base_probs=base_probs,
            hits_probs=hits_probs,
            outs_probs=outs_probs,
            game_situation=gamestate.get_situation_dict(),
            timestamp=datetime.now().isoformat()
        )
    

    
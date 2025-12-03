from re import I
from ATBAT.ATBAT_PITCHES import PitchEngine as PE
from ATBAT.ATBAT_PROBS import ProbabilityModifier
from CONTEXT.ATBAT_CONTEXT import AtBatToken, AtBatEvent, AtBatResult
from UTILITIES.ENUMS import EventType, Pitch, Micro, Macro, StatKey
from UTILITIES.RANDOM import get_random
from DATA_LOADERS.LEAGUE_STATS_LOADER import LeagueLoader


class AtBatSimulator:
    """ Step-by-step at-bat simulation with live probability calculation. """
    # Pre-defined outcome lists (avoid recreating on every at-bat)
    _BASE = (('SO', Macro.SO), ('BB', Macro.BB), ('HP', Macro.HP), ('HR', Macro.HR))
    _HITS = (('IH', Macro.IH), ('SL', Macro.SL), ('DL', Macro.DL), ('TL', Macro.TL))
    _OUTS = (('GO', Macro.GO), ('FO', Macro.FO), ('LO', Macro.LO), ('PO', Macro.PO))
    
    # Micro event probabilities
    _MICRO_PROBS = {
        'WP': 0.005,      # Wild pitch (per ball)
        'PB': 0.002,      # Passed ball (per ball)
        'BK': 0.001,      # Balk (per pitch - rare)
        'SB': 0.150,      # Stolen base (per ball - context dependent)
        'P1': 0.010       # Pickoff attempt (per pitch with runner on 1st)
    }
    
    @staticmethod
    def initialize_matchup(batting_lineup_mgr, pitching_team_mgr):
        batter = batting_lineup_mgr.get_current_batter()
        pitcher = pitching_team_mgr.get_current_pitcher()

        return AtBatToken(batter=batter, pitcher=pitcher)

    @staticmethod
    def get_effective_handedness(batter, pitcher):
        """ Determine effective batting handedness considering switch hitters. """
        # Switch hitters always bat opposite the pitcher
        batter_eff = "R" if pitcher.throws == "L" else "L" if batter.bats == "B" else batter.bats
        pitcher_eff = pitcher.throws
        
        return batter_eff, pitcher_eff

    @classmethod
    def generate_matchup_probs(cls, gamestate, token):
        """ Generate adjusted outcome probabilities for the current batter-pitcher matchup. """
        leag = LeagueLoader.get_league_factors() or {}
        park = gamestate.home_team.park_factors or {}

        b_eff, p_eff = cls.get_effective_handedness(token.batter, token.pitcher)
        b_stats = token.batter.stats_vl if p_eff == "L" else token.batter.stats_vr
        p_stats = token.pitcher.stats_vl if b_eff == "L" else token.pitcher.stats_vr

        base_probs = {}
        for stat_key in StatKey:
            key_str = stat_key.value
            base_probs[key_str] = ProbabilityModifier.calculate_probability(
                b_stats[key_str], 
                p_stats[key_str], 
                0.50, 0.50, 
                leag.get(key_str, 1.0), 
                park.get(key_str, 1.0),
            )

        outcome_probs = base_probs.copy()
        return outcome_probs

    @classmethod
    def generate_macro_outcome(cls, outcome_probs):
        """Generate the final outcome of the at-bat based on probabilities."""
        base_rand = get_random()
        base_cum = 0.0
        
        for outcome_key, outcome_enum in cls._BASE:
            base_cum += outcome_probs[outcome_key]
            if base_rand < base_cum:
                return outcome_enum
        
        babip_rand = get_random()
        
        if babip_rand < outcome_probs['BA']:
            # It's a hit - determine which type
            hit_rand = get_random()
            hit_cum = 0.0
            hit_total = sum(outcome_probs[key] for key, _ in cls._HITS)
            
            if hit_total > 0:
                for outcome_key, outcome_enum in cls._HITS:
                    hit_cum += outcome_probs[outcome_key] / hit_total
                    if hit_rand < hit_cum:
                        return outcome_enum
            
            return Macro.SL  # Fallback if no hit type selected
        else:
            # It's an out - determine which type
            out_rand = get_random()
            out_cum = 0.0
            out_total = sum(outcome_probs[key] for key, _ in cls._OUTS)
            
            if out_total > 0:
                for outcome_key, outcome_enum in cls._OUTS:
                    out_cum += outcome_probs[outcome_key] / out_total
                    if out_rand < out_cum:
                        return outcome_enum
            
            return Macro.GO # Fallback if no hit type selected

    @classmethod
    def generate_modified_sequence(cls, gamestate, outcome: Macro):
        """ Generate a pitch sequence for the given outcome using PitchEngine. """
        events = []
        pitches = PE.generate_sequence(outcome)
        pickoffs = 0

        # Process all pitches except the final one (which ends the at-bat)
        for pitch in pitches[:-1]:
            # 0. Check for pickoff attempt (independent of pitch, can happen any time)
            if gamestate.bases.fst is not None and pickoffs < 2:
                if get_random() < cls._MICRO_PROBS['P1']:
                    events.append(AtBatEvent(
                        event_type=EventType.MICRO, 
                        event_code=Micro.P1,
                        event_data={}
                    ))
                    pickoffs += 1

            # 1. Add the pitch event
            events.append(AtBatEvent(
                event_type=EventType.PITCH, 
                event_code=pitch, 
                event_data={}
            ))

            # 2. Check for micro events after this pitch (only one per pitch)
            if pitch == Pitch.BL:  # Ball - Wild pitch or Passed ball
                if get_random() < cls._MICRO_PROBS['WP']:
                    events.append(AtBatEvent(
                        event_type=EventType.MICRO, 
                        event_code=Micro.WP,
                        event_data={}
                    ))
                elif get_random() < cls._MICRO_PROBS['PB']:
                    events.append(AtBatEvent(
                        event_type=EventType.MICRO, 
                        event_code=Micro.PB,
                        event_data={}
                    ))

            elif get_random() < cls._MICRO_PROBS['BK']:  # Balk (rare, on any non-ball pitch)
                events.append(AtBatEvent(
                    event_type=EventType.MICRO, 
                    event_code=Micro.BK,
                    event_data={}
                ))

            elif pitch != Pitch.FL:
                if gamestate.bases.fst is not None and gamestate.bases.snd is None: 
                    if get_random() < cls._MICRO_PROBS['SB']:  # Called strike - Stolen base
                        events.append(AtBatEvent(
                            event_type=EventType.MICRO, 
                            event_code=Micro.SB,
                            event_data={}
                        ))

        # Final pitch (ends the at-bat)
        events.append(AtBatEvent(
            event_type=EventType.PITCH,
            event_code=pitches[-1],
            event_data={}
        ))

        return events

    @classmethod
    def simulate_at_bat(cls, gamestate, token):
        events = []

        probs = cls.generate_matchup_probs(gamestate, token)
        outcome = cls.generate_macro_outcome(probs)
        events = cls.generate_modified_sequence(gamestate, outcome)

        # Add the final macro outcome
        events.append(AtBatEvent(
            event_type=EventType.MACRO,
            event_code=outcome,
            event_data={}
        ))

        return AtBatResult(events=events)

    @staticmethod
    def advance_next_batter(batting_lineup_mgr):
        """ Step 5: Advance to the next batter in the lineup. """       
        batting_lineup_mgr.get_next_batter()
        
from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE
import random

class PassedBall:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="PASSED BALL",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=False,
            is_complete=True,
            at_bat_complete=False,
            is_error=is_error
        )

        # Parse base state
        base_state = gamestate.get_base_state()
        r1 = base_state[0] == "1"
        r2 = base_state[2] == "1"
        r3 = base_state[4] == "1"

        # Process R3 → R2 → R1 (reverse order)
        if r3:
            play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
            play_context.runs_scored += 1
        
        # R2: Only forced if R1 occupied
        if r2:
            play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
        
        # R1: Always forced (batter needs 1st)
        if r1:
            play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)

        return play_context
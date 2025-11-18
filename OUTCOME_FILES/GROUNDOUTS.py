from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from OUTCOME_FILES.GSINGLEOUTS import GSingleOuts
from OUTCOME_FILES.GDOUBLEOUTS import GDoubleOuts
import random

class Groundout:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="GROUNDOUT",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=False,
            is_complete=True,
            at_bat_complete=True,
            is_error=is_error
        )
        
        base_state = gamestate.get_base_state()
        rand = random.randint(1, 1000)

        if base_state in ["1_1_1", "1_1_0", "1_0_1", "1_0_0"]:
            if gamestate.outs < 2:
                if rand < 455:
                    GDoubleOuts.execute(play_context, gamestate, base_state, batter)
                
                else:
                    GSingleOuts.execute(play_context, gamestate, base_state, batter)

            else:
                GSingleOuts.execute(play_context, gamestate, base_state, batter)

        else:
            GSingleOuts.execute(play_context, gamestate, base_state, batter)

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)

        return play_context
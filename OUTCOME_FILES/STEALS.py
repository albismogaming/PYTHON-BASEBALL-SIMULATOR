from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
import random

class BaseStealing:
    def execute(self, gamestate, batter, pitcher, matchup_token, base_runner_mgr, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="STEAL SECOND ATTEMPT",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=False,
            is_complete=True,
            at_bat_complete=False,
            is_error=is_error
        )

        if gamestate.bases[Base.THD] != None:
            play_context.on_thd = base_runner_mgr.hld_runner(Base.THD)

        if gamestate.bases[Base.SND] != None:
            play_context.on_snd = base_runner_mgr.hld_runner(Base.SND)

        if gamestate.bases[Base.FST] != None:
            if gamestate.bases[Base.SND] != None:
                randval = random.randint(1, 1000)
                if randval <= 210:
                    play_context.on_fst = base_runner_mgr.out_runner(Base.FST, Base.SND)
                    play_context.outs_recorded += 1
                
                elif randval <= 240:
                    play_context.on_fst = base_runner_mgr.hld_runner(Base.FST)

                else:
                    play_context.on_fst = base_runner_mgr.adv_runner(Base.FST, Base.SND)
            else:
                    play_context.on_fst = base_runner_mgr.hld_runner(Base.FST)

        return play_context
from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE
from TEAM_UTILS.BASE_RUNNING_MANAGER import BaseRunningManager as BRM
import random as r

class Flyout:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="FLYOUT",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=True,
            is_complete=True,
            at_bat_complete=True,
            is_error=is_error
        )

        # Parse base state
        base_state = gamestate.get_base_state()
        r1 = base_state[0] == "1"
        r2 = base_state[2] == "1"
        r3 = base_state[4] == "1"

        if r3:
            adv = r.randint(1, 1000)
            out = r.randint(1, 1000)
            
            adv_prob = BRM.r3_tag_adv(outs=gamestate.outs, hit_depth=hit_info.hit_depth, fielder=hit_info.hit_fielder)
            out_prob = BRM.r3_tag_out(hit_depth=hit_info.hit_depth, fielder=hit_info.hit_fielder)

            if gamestate.outs < 2:
                if adv <= adv_prob:
                    if out <= out_prob:
                        play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                        play_context.outs_recorded += 1

                    else:
                        play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                        play_context.runs_scored += 1

                else:
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
            
            else:
                play_context.on_thd = BRE.adv_runner(gamestate, Base.THD, Base.HME)

        if r2:
            play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)

        if r1:
            play_context.on_fst = BRE.hld_runner(gamestate, Base.FST)
        
        play_context.on_bat = BRE.out_batter(gamestate, Base.HME, batter)
        play_context.outs_recorded += 1

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)
        
        return play_context
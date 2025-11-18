from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE
import random

class Pickoff1st:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="PICKOFF TO FIRST",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=False,
            is_complete=True,
            at_bat_complete=False,
            is_error=is_error
        )

        base_state = gamestate.get_base_state()
        
        # Execute runner movements based on base state
        if base_state == "1_0_0":
            play_context.on_fst = BRE.hld_runner(gamestate, Base.FST)

        elif base_state == "0_1_0":
            play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
            
        elif base_state == "0_0_1":
            play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
            
        elif base_state == "1_1_0":
            play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
            play_context.on_fst = BRE.hld_runner(gamestate, Base.FST)
            
        elif base_state == "1_0_1":
            play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
            play_context.on_fst = BRE.hld_runner(gamestate, Base.FST)

        elif base_state == "0_1_1":
            play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
            play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
            
        elif base_state == "1_1_1":
            play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
            play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
            play_context.on_fst = BRE.hld_runner(gamestate, Base.FST)
        
        else:
            # Bases empty (0_0_0) - most common scenario (~60% of at-bats)
            # No runner advancement needed, batter walks to 1st only
            pass

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)
        
        return play_context
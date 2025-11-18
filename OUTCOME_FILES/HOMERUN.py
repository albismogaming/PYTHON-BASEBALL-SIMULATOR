from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE
from TEAM_UTILS.BASE_RUNNING_MANAGER import BaseRunningManager as BRM


class Homerun:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="HOMERUN",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=1,
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
            play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
            play_context.runs_scored += 1

        if r2:
            play_context.on_snd = BRE.scr_runner(gamestate, Base.SND)
            play_context.runs_scored += 1

        if r1:
            play_context.on_fst = BRE.scr_runner(gamestate, Base.FST)
            play_context.runs_scored += 1

        # Batter always advances to 1st on a walk
        play_context.on_bat = BRE.scr_batter(gamestate, batter)
        play_context.runs_scored += 1

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)
        
        return play_context



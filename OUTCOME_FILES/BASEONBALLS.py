from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayContext
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE


class BaseOnBalls:
    def execute(self, gamestate, batter, pitcher, matchup_token, hit_info, is_error=False):
        play_context = PlayContext(
            batter=batter,
            pitcher=pitcher,
            description="BASE ON BALLS",
            token=matchup_token,
            hit_info=hit_info,
            hits_hit=0,
            is_ball_in_play=False,
            is_complete=True,
            at_bat_complete=True,
            is_error=is_error
        )

        # Parse base state
        base_state = gamestate.get_base_state()
        r1 = base_state[0] == "1"
        r2 = base_state[2] == "1"
        r3 = base_state[4] == "1"

        # Process R3 → R2 → R1 (reverse order)
        # R3: Only forced if bases loaded
        if r3:
            if r1 and r2:
                # Bases loaded - R3 forced home
                play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                play_context.runs_scored += 1
            else:
                # R3 not forced - holds
                play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
        
        # R2: Only forced if R1 occupied
        if r2:
            if r1:
                # R2 forced to 3rd (R1 needs 2nd)
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
            else:
                # R2 not forced - holds
                play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
        
        # R1: Always forced (batter needs 1st)
        if r1:
            play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)

        # Batter always advances to 1st on a walk
        play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)

        # Update game state
        gamestate.add_hit(play_context.hits_hit)
        gamestate.add_run(play_context.runs_scored)
        gamestate.add_out(play_context.outs_recorded)

        return play_context
    


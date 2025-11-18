import random
import numpy as np
from UTILITIES.ENUMS import *
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE

class GDoubleOuts:
    @staticmethod
    def execute(play_context, gamestate, base_state, batter):
        rand_one = random.randint(1, 1000)


        if base_state == "1_0_0":
            # Classic 6-4-3 or 4-6-3 double play
            play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
            play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
            play_context.outs_recorded += 2


        elif base_state == "1_1_0":
            if rand_one < 280:  # 28% - Runner on 2nd advances to 3rd, DP at 2nd and 1st
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2

            elif rand_one < 980:  # 70% - Runner on 2nd out at 3rd, runner on 1st out at 2nd
                play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2

            else:  # 2% - Runner on 2nd out at 3rd, batter out at 1st, runner on 1st advances to 2nd
                play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2


        elif base_state == "1_0_1":
            # 6-4-3 or 4-6-3 double play, runner on 3rd scores (unless DP ends inning)
            if gamestate.outs == 1:  # DP ends inning, run doesn't count
                play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2

            else:  # 0 outs, run scores
                play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.runs_scored += 1
                play_context.outs_recorded += 2


        elif base_state == "1_1_1":
            if rand_one < 200:  # 20% - Out at home, then out at 1st (home-first DP)
                play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2

            elif rand_one < 240:  # 4% - Out at home, then out at 3rd (home-third DP)
                play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 2

            elif rand_one < 960:  # 72% - Standard 6-4-3 DP, runner on 3rd scores (unless DP ends inning)
                if gamestate.outs == 1:  # DP ends inning, run doesn't count
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 2

                else:  # 0 outs, run scores
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 2

            else:  # 4% - Out at 3rd and out at 2nd (rare), runner on 3rd scores (unless DP ends inning)
                if gamestate.outs == 1:  # DP ends inning, run doesn't count
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 2

                else:  # 0 outs, run scores
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 2




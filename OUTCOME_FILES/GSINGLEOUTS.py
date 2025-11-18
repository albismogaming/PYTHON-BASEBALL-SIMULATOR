import random
import numpy as np
from UTILITIES.ENUMS import *
from ENGINES.ENG_BASERUNNING import BaseRunnerEngine as BRE


class GSingleOuts:
    @staticmethod
    def execute(play_context, gamestate, base_state, batter):
        rand_one = random.randint(1, 1000)
        rand_two = random.randint(1, 1000)

        if base_state == "0_0_0":
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)

                play_context.outs_recorded += 1


        elif base_state == "1_0_0":
            if gamestate.outs < 2:
                if rand_two < 650:
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                else:
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:
                if rand_two < 350:
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                else:
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1


        elif base_state == "0_1_0":
            if gamestate.outs < 2:
                if rand_one < 550:  # 55% chance of advancing to third, runner out at first
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                elif rand_one < 575: 
                    play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                else:  # 6% chance of runner on second out and batter safe at first
                    play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1
            else:
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 1


        elif base_state == "0_0_1":
            if gamestate.outs < 2:
                if rand_one < 340:
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 1

                elif rand_one < 375:
                    play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                else:
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:
                play_context.on_thd = BRE.adv_runner(gamestate, Base.THD, Base.HME)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 1


        elif base_state == "1_1_0":
            if gamestate.outs < 2:
                if rand_one < 35:
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                elif rand_one < 600:
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1
                
                else:
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)

                play_context.outs_recorded += 1


        elif base_state == "1_0_1":
            if gamestate.outs < 2:
                if rand_one < 150:  # 15% - Out at home, runners advance to 2nd and 1st
                    play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                elif rand_one < 500:  # 35% - Force at 2nd, runner on 3rd scores, batter safe at 1st
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1
                    play_context.runs_scored += 1
                
                elif rand_one < 800:  # 30% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd scores
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1
                    play_context.runs_scored += 1
                
                else:  # 20% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd holds
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:  # 2 outs - batter out ends the inning, no runs score
                play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 1


        elif base_state == "0_1_1":
            if gamestate.outs < 2:
                if rand_one < 600:  # 60% - Batter out at 1st, runner on 3rd scores, runner on 2nd to 3rd
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 1

                elif rand_one < 850:  # 25% - Batter out at 1st, runner on 3rd scores, runner on 2nd holds
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 1

                elif rand_one < 950:  # 10% - Out at home, runner on 2nd to 3rd, batter safe at 1st
                    play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                else:  # 5% - Batter out at 1st, both runners hold
                    play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:  # 2 outs - batter out ends inning, no runs score
                play_context.on_thd = BRE.hld_runner(gamestate, Base.THD)
                play_context.on_snd = BRE.hld_runner(gamestate, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 1


        elif base_state == "1_1_1":
            if gamestate.outs < 2:
                if rand_one < 400:  # 40% - Out at home, bases stay loaded
                    play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

                elif rand_one < 750:  # 35% - Force at 2nd, runner on 3rd scores, runners on 1st and 3rd after
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.out_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 1

                elif rand_one < 900:  # 15% - Batter out at 1st, all runners advance, run scores
                    play_context.on_thd = BRE.scr_runner(gamestate, Base.THD)
                    play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                    play_context.runs_scored += 1
                    play_context.outs_recorded += 1

                else:  # 10% - Out at 3rd, other runners advance
                    play_context.on_thd = BRE.out_runner(gamestate, Base.THD, Base.HME)
                    play_context.on_snd = BRE.out_runner(gamestate, Base.SND, Base.THD)
                    play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                    play_context.on_bat = BRE.adv_batter(gamestate, Base.FST, batter)
                    play_context.outs_recorded += 1

            else:  # 2 outs - batter out ends inning, no runs score
                play_context.on_thd = BRE.adv_runner(gamestate, Base.THD, Base.HME)
                play_context.on_snd = BRE.adv_runner(gamestate, Base.SND, Base.THD)
                play_context.on_fst = BRE.adv_runner(gamestate, Base.FST, Base.SND)
                play_context.on_bat = BRE.out_batter(gamestate, Base.FST, batter)
                play_context.outs_recorded += 1






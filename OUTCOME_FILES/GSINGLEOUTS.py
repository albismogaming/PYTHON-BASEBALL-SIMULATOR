from UTILITIES.RANDOM import get_random
from UTILITIES.ENUMS import *

class GSingleOuts:
    @staticmethod
    def execute(gamestate, base_state, batter):
        hits = 0
        runs = 0
        outs = 0
        rand_one = get_random()
        rand_two = get_random()
    
        if base_state == 0:
                outs += 1

        elif base_state == 1:
            if gamestate.outs < 2:
                if rand_two < 0.650:
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                else:
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

            else:
                if rand_two < 0.350:
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                else:
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1

        elif base_state == 2:
            if gamestate.outs < 2:
                if rand_one < 0.550:  # 55% chance of advancing to third, runner out at first
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1
                elif rand_one < 0.575:
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                else:
                    outs += 1
            else:
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = None
                outs += 1

        elif base_state == 4:
            if gamestate.outs < 2:
                if rand_one < 0.340:
                    gamestate.bases[Base.THD] = None
                    runs += 1
                    outs += 1
                elif rand_one < 0.375:
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                else:
                    outs += 1

            else:
                gamestate.bases[Base.THD] = None
                outs += 1

        elif base_state == 3:
            if gamestate.outs < 2:
                if rand_one < 0.035:
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                elif rand_one < 0.600:
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1
                
                else:
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1

            else:
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
                outs += 1

        elif base_state == 5:
            if gamestate.outs < 2:
                if rand_one < 0.150:  # 15% - Out at home, runners advance to 2nd and 1st
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                elif rand_one < 0.500:  # 35% - Force at 2nd, runner on 3rd scores, batter safe at 1st
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1
                    runs += 1
                
                elif rand_one < 0.800:  # 30% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd scores
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1
                    runs += 1
                
                else:  # 20% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd holds
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1

            else:  # 2 outs - batter out ends the inning, no runs score
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    outs += 1

        elif base_state == 6:
            if gamestate.outs < 2:
                if rand_one < 0.600:  # 60% - Batter out at 1st, runner on 3rd scores, runner on 2nd to 3rd
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    runs += 1
                    outs += 1

                elif rand_one < 0.850:  # 25% - Batter out at 1st, runner on 3rd scores, runner on 2nd holds
                    gamestate.bases[Base.THD] = None
                    runs += 1
                    outs += 1

                elif rand_one < 0.950:  # 10% - Out at home, runner on 2nd to 3rd, batter safe at 1st
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                else:  # 5% - Batter out at 1st, both runners hold
                    outs += 1

            else:  # 2 outs - batter out ends inning, no runs score
                outs += 1

        elif base_state == 7:
            if gamestate.outs < 2:
                if rand_one < 0.400:  # 40% - Out at home, bases stay loaded
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

                elif rand_one < 0.750:  # 35% - Force at 2nd, runner on 3rd scores, runners on 1st and 3rd after
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    runs += 1
                    outs += 1

                elif rand_one < 0.900:  # 15% - Batter out at 1st, all runners advance, run scores
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    runs += 1
                    outs += 1

                else:  # 10% - Out at 3rd, other runners advance
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 1

            else:  # 2 outs - batter out ends inning, no runs score
                gamestate.bases[Base.THD] = None
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
                outs += 1

        return hits, runs, outs






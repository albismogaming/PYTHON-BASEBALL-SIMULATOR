from UTILITIES.RANDOM import get_random
from UTILITIES.ENUMS import *

class GDoubleOuts:
    @staticmethod
    def execute(gamestate, base_state, batter):
        hits = 0
        runs = 0
        outs = 0
        rand_one = get_random()


        if base_state == 1:
            # Classic 6-4-3 or 4-6-3 double play
            gamestate.bases[Base.FST] = None
            outs += 2


        elif base_state == 3:
            if rand_one < 0.280:  # 28% - Runner on 2nd advances to 3rd, DP at 2nd and 1st
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.FST] = None
                outs += 2

            elif rand_one < 0.980:  # 70% - Runner on 2nd out at 3rd, runner on 1st out at 2nd
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.FST] = None
                gamestate.bases[Base.FST] = batter
                outs += 2

            else:  # 2% - Runner on 2nd out at 3rd, batter out at 1st, runner on 1st advances to 2nd
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
                outs += 2


        elif base_state == 5:
            # 6-4-3 or 4-6-3 double play, runner on 3rd scores (unless DP ends inning)
            if gamestate.outs == 1:  # DP ends inning, run doesn't count
                gamestate.bases[Base.FST] = None
                outs += 2

            else:  # 0 outs, run scores
                gamestate.bases[Base.THD] = None
                gamestate.bases[Base.FST] = None
                runs += 1
                outs += 2


        elif base_state == 7:
            if rand_one < 200:  # 20% - Out at home, then out at 1st (home-first DP)
                gamestate.bases[Base.THD] = None
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
                outs += 2

            elif rand_one < 0.240:  # 4% - Out at home, then out at 3rd (home-third DP)
                gamestate.bases[Base.THD] = None
                gamestate.bases[Base.SND] = None
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
                gamestate.bases[Base.FST] = batter
                outs += 2

            elif rand_one < 0.960:  # 72% - Standard 6-4-3 DP, runner on 3rd scores (unless DP ends inning)
                if gamestate.outs == 1:  # DP ends inning, run doesn't count
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = None 
                    outs += 2

                else:  # 0 outs, run scores
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
                    runs += 1
                    outs += 2

            else:  # 4% - Out at 3rd and out at 2nd (rare), runner on 3rd scores (unless DP ends inning)
                if gamestate.outs == 1:  # DP ends inning, run doesn't count
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    outs += 2

                else:  # 0 outs, run scores
                    gamestate.bases[Base.THD] = None
                    gamestate.bases[Base.SND] = None
                    gamestate.bases[Base.FST] = None
                    gamestate.bases[Base.FST] = batter
                    runs += 1
                    outs += 2
        
        return hits, runs, outs


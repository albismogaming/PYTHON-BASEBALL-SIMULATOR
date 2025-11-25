from requests import get
from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random, scr_random, out_random, adv_random, sac_random

class Flyout:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 1

        bases = gamestate.bases
        r1 = bases[Base.FST] is not None
        r2 = bases[Base.SND] is not None
        r3 = bases[Base.THD] is not None

        # Inline base state check
        if r3:
            if gamestate.outs < 2:
                if get_random() < sac_random():  # Dynamic threshold for scoring from 3rd
                    # 7.8% - R3 tags and scores without throw
                    gamestate.bases[Base.THD] = None
                    runs += 1

                elif get_random() < adv_random():       
                    if get_random() < out_random():
                        # 6.4% thrown out at home
                        gamestate.bases[Base.THD] = None
                        outs += 1
                    else:
                        # 93.6% safe at home
                        gamestate.bases[Base.THD] = None
                        runs += 1
            else:
                # 2 outs - runner clears base without scoring (out ends inning)
                gamestate.bases[Base.THD] = None
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
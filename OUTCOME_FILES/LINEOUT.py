from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random

class Lineout:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 1

        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        if r3:
            if gamestate.outs < 2:
                adv = get_random()

                if adv <= 0.078:
                    # 7.8% - R3 tags and scores without throw
                    gamestate.bases[Base.THD] = None
                    runs += 1

                elif adv <= 0.386:  # 0.078 + 0.308 = cumulative
                    # 30.8% - R3 attempts to tag
                    out = get_random()

                    if out <= 0.084:
                        # 8.4% thrown out at home
                        gamestate.bases[Base.THD] = None
                        outs += 1
                    else:
                        # 91.6% safe at home
                        gamestate.bases[Base.THD] = None
                        runs += 1
                # else: 61.4% - R3 holds
            
            else:
                # 2 outs - runner clears base without scoring (out ends inning)
                gamestate.bases[Base.THD] = None
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
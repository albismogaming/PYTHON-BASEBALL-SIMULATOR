from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random

class Flyout:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 1

        # Inline base state check
        if gamestate.bases[Base.THD] is not None:
            if gamestate.outs < 2:
                adv = get_random()

                if adv <= 0.078:
                    # 7.8% - R3 tags and scores without throw
                    gamestate.bases[Base.THD] = None
                    runs += 1

                elif adv <= 0.526:  # 0.078 + 0.448 = cumulative
                    # 44.8% - R3 attempts to tag
                    out = get_random()

                    if out <= 0.064:
                        # 6.4% thrown out at home
                        gamestate.bases[Base.THD] = None
                        outs += 1
                    else:
                        # 93.6% safe at home
                        gamestate.bases[Base.THD] = None
                        runs += 1
                # else: 47.4% - R3 holds
            
            else:
                # 2 outs - runner clears base without scoring (out ends inning)
                gamestate.bases[Base.THD] = None
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
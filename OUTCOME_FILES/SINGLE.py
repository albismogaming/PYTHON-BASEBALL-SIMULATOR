from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random

class Single:
    def execute(self, gamestate, batter, pitcher):
        hits = 1
        runs = 0
        outs = 0

        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        if r3:
            gamestate.bases[Base.THD] = None
            runs += 1
        
        if r2:
            if get_random() <= 0.560:
                if get_random() <= 0.048:
                    gamestate.bases[Base.SND] = None
                    outs += 1
                else:
                    gamestate.bases[Base.SND] = None
                    runs += 1
            else:
                gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
                gamestate.bases[Base.SND] = None

        if r1:
            if not r2 and not r3:
                if get_random() <= 0.330:
                    if get_random() <= 0.058:
                        gamestate.bases[Base.FST] = None
                        outs += 1
                    else:
                        gamestate.bases[Base.FST] = None
                        runs += 1

                else:
                    gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                    gamestate.bases[Base.FST] = None
            else:
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None

        # Always advance batter to 1st
        gamestate.bases[Base.FST] = batter
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
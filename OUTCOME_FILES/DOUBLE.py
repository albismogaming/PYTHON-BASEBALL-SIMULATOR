from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random

class Double:
    def execute(self, gamestate, batter, pitcher):
        hits = 1
        runs = 0
        outs = 0
        
        # Inline base state checks
        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        if r3:
            gamestate.bases[Base.THD] = None
            runs += 1
        
        if r2:
            gamestate.bases[Base.SND] = None
            runs += 1

        if r1:
            if get_random() <= 0.570:
                if get_random() <= 0.055:
                    gamestate.bases[Base.FST] = None
                    outs += 1
                else:
                    gamestate.bases[Base.FST] = None
                    runs += 1
            else:
                gamestate.bases[Base.THD] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None
        
        # Always advance batter to 2nd
        gamestate.bases[Base.SND] = batter
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
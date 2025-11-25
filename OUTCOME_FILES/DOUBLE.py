from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random, scr_random, out_random, adv_random

class Double:
    def execute(self, gamestate, batter, pitcher):
        hits = 1
        runs = 0
        outs = 0
        
        bases = gamestate.bases
        r1 = bases[Base.FST] is not None
        r2 = bases[Base.SND] is not None
        r3 = bases[Base.THD] is not None

        if r3:
            gamestate.bases[Base.THD] = None
            runs += 1
        
        if r2:
            gamestate.bases[Base.SND] = None
            runs += 1

        if r1:
            if get_random() <= scr_random():  # Dynamic threshold for scoring from 1st
                if get_random() <= out_random():
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
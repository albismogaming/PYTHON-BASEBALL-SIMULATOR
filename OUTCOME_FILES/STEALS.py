from UTILITIES.ENUMS import *
import random as r

class BaseStealing:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 0

        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        # Only attempt steal if R1 occupied and R2 empty (no double steal logic yet)
        if r1 and not r2:
            randval = r.randint(1, 1000)
            
            if randval <= 210:  # 21% - Caught stealing
                gamestate.bases[Base.FST] = None
                outs += 1
            
            elif randval <= 240:  # 3% - Delayed/held at first (pickoff attempt, etc)
                pass  # Runner stays at first, no state change needed
            
            else:  # 76% - Successful steal
                gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
                gamestate.bases[Base.FST] = None

        gamestate.add_stats(hits=hits, runs=runs, outs=outs)

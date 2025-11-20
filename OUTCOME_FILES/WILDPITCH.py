from UTILITIES.ENUMS import *

class WildPitch:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 0

        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        # Process R3 → R2 → R1 (reverse order)
        if r3:
            gamestate.bases[Base.THD] = None
            runs += 1
        
        if r2:
            gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
            gamestate.bases[Base.SND] = None

        if r1:
            gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
            gamestate.bases[Base.FST] = None   

        gamestate.add_stats(hits=hits, runs=runs, outs=outs)

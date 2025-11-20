from UTILITIES.ENUMS import *

class Pickoff1st:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 0

        r1 = gamestate.bases[Base.FST] is not None
        r2 = gamestate.bases[Base.SND] is not None
        r3 = gamestate.bases[Base.THD] is not None

        gamestate.add_stats(hits=hits, runs=runs, outs=outs)

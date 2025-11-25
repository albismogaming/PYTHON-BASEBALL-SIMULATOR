from UTILITIES.ENUMS import *

class Homerun:
    def execute(self, gamestate, batter, pitcher):
        hits = 1
        runs = 1
        outs = 0

        bases = gamestate.bases
        r1 = bases[Base.FST] is not None
        r2 = bases[Base.SND] is not None
        r3 = bases[Base.THD] is not None


        if r3:
            runs += 1
            gamestate.bases[Base.THD] = None
            
        if r2:
            runs += 1
            gamestate.bases[Base.SND] = None
            
        if r1:
            runs += 1
            gamestate.bases[Base.FST] = None
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }

        
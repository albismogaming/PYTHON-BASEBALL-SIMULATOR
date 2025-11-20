from UTILITIES.ENUMS import *

class Homerun:
    def execute(self, gamestate, batter, pitcher):
        hits = 1
        runs = 1
        outs = 0

        if gamestate.bases[Base.THD] is not None:
            runs += 1
            gamestate.bases[Base.THD] = None
            
        if gamestate.bases[Base.SND] is not None:
            runs += 1
            gamestate.bases[Base.SND] = None
            
        if gamestate.bases[Base.FST] is not None:
            runs += 1
            gamestate.bases[Base.FST] = None
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }

        
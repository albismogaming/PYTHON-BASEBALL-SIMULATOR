from UTILITIES.ENUMS import *

class Triple:
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
            gamestate.bases[Base.SND] = None
            runs += 1

        if r1:
            gamestate.bases[Base.FST] = None
            runs += 1

        # Batter always advances to 3rd on a triple
        gamestate.bases[Base.THD] = batter
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }

        
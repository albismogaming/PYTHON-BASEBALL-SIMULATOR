from UTILITIES.ENUMS import *
from OUTCOME_FILES.GSINGLEOUTS import GSingleOuts
from OUTCOME_FILES.GDOUBLEOUTS import GDoubleOuts
from UTILITIES.RANDOM import get_random

class Groundout:
    def execute(self, gamestate, batter, pitcher):
        base_state = gamestate.get_base_state()

        if base_state in [1, 3, 5, 7]:
            if gamestate.outs < 2:
                if get_random() < 0.455:
                    hits, runs, outs = GDoubleOuts.execute(gamestate, base_state, batter)
                
                else:
                    hits, runs, outs = GSingleOuts.execute(gamestate, base_state, batter)

            else:
                hits, runs, outs = GSingleOuts.execute(gamestate, base_state, batter)

        else:
            hits, runs, outs = GSingleOuts.execute(gamestate, base_state, batter)
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }

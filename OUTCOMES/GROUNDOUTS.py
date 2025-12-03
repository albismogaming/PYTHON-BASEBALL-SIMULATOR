from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.ENUMS import *
from OUTCOME_FILES.GSINGLEOUTS import execute_FC
from OUTCOME_FILES.GDOUBLEOUTS import execute_DP
from UTILITIES.RANDOM import get_random


def execute_GO(gamestate, token) -> PlayResult:
    base_state = gamestate.get_base_state()

    if base_state in [1, 3, 5, 7]:
        if gamestate.outs < 2:
            if get_random() < 0.455:
                result = execute_DP(gamestate, base_state, token)
            
            else:
                result = execute_FC(gamestate, base_state, token)

        else:
            result = execute_FC(gamestate, base_state, token)

    else:
        result = execute_FC(gamestate, base_state, token)
    
    return result
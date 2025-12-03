from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random, scr_random, out_random, adv_random, sac_random
from CONTEXT.PLAY_CONTEXT import PlayResult


def execute_SO(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.SO, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    result.outs += 1

    result.bases_after = new_state
    
    return result


def execute_FO(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.FO, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        if gamestate.outs < 2:
            if get_random() < sac_random():
                new_state.thd = None
                result.runs += 1

            elif get_random() < adv_random():       
                if get_random() < out_random():
                    new_state.thd = None
                    result.outs += 1
                else:
                    new_state.thd = None
                    result.runs += 1
    
    result.outs += 1
    result.bases_after = new_state

    return result
    

def execute_LO(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.LO, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        if gamestate.outs < 2:
            if get_random() < sac_random():
                new_state.thd = None
                result.runs += 1

            elif get_random() < adv_random():       
                if get_random() < out_random():
                    new_state.thd = None
                    result.outs += 1
                else:
                    new_state.thd = None
                    result.runs += 1
    
    result.outs += 1
    result.bases_after = new_state

    return result


def execute_PO(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.PO, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    result.outs += 1

    result.bases_after = new_state
    
    return result
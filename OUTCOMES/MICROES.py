from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random, poff_random, stl_random


def execute_BK(gamestate, token) -> PlayResult:
    result = PlayResult(type=Micro.BK, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1

    if new_state.snd:
        new_state.thd = new_state.snd
        new_state.snd = None

    if new_state.fst:
        new_state.snd = new_state.fst
        new_state.fst = None

    result.bases_after = new_state
    
    return result


def execute_PB(gamestate, token) -> PlayResult:
    result = PlayResult(type=Micro.PB, batter=token.batter, pitcher=token.pitcher, balls_delta=1)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1
                
    if new_state.snd:
        new_state.thd = new_state.snd
        new_state.snd = None

    if new_state.fst:
        new_state.snd = new_state.fst
        new_state.fst = None

    result.bases_after = new_state

    return result


def execute_WP(gamestate, token) -> PlayResult:
    result = PlayResult(type=Micro.WP, batter=token.batter, pitcher=token.pitcher)
    bases = gamestate.bases
    result.bases_before = bases

    new_state = bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1
                
    if new_state.snd:
        new_state.thd = new_state.snd
        new_state.snd = None

    if new_state.fst:
        new_state.snd = new_state.fst
        new_state.fst = None

    result.bases_after = new_state

    return result


def execute_SB(gamestate, token) -> PlayResult:
    result = PlayResult(type=Micro.SB, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.fst and not new_state.snd:
        if get_random() <= stl_random():  # Successful steal
            new_state.snd = new_state.fst
            new_state.fst = None
        
        else:  # Caught stealing
            new_state.fst = None
            result.outs += 1

    result.bases_after = new_state
    return result


def execute_P1(gamestate, token) -> PlayResult:
    result = PlayResult(type=Micro.P1, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.fst:
        if get_random() < poff_random():
            # Pickoff successful
            new_state.fst = None
            result.outs += 1


    result.bases_after = new_state

    return result
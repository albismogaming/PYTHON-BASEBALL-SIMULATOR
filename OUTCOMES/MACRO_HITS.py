from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.ENUMS import *
from UTILITIES.RANDOM import get_random, adv_random, scr_random, out_random


def execute_IH(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.IH, batter=token.batter, pitcher=token.pitcher)
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
    
    new_state.fst = token.batter
    result.hits += 1
    result.bases_after = new_state
            
    return result


def execute_SL(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.SL, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases  # Store BaseState directly, no conversion
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1
    
    if new_state.snd:
        if get_random() < scr_random():  # Dynamic threshold for scoring from 2nd
            if get_random() < out_random():  # Dynamic threshold for getting thrown out
                new_state.snd = None
                result.outs += 1
            else:
                new_state.snd = None
                result.runs += 1
        else:
            new_state.thd = new_state.snd
            new_state.snd = None

    if new_state.fst:
        if not new_state.thd and not new_state.snd:
            if get_random() < adv_random():
                if get_random() < out_random():
                    new_state.fst = None
                    result.outs += 1

                else:
                    new_state.thd = new_state.fst
                    new_state.fst = None

            else:
                new_state.snd = new_state.fst
                new_state.fst = None

        else:
            new_state.snd = new_state.fst
            new_state.fst = None

    # Always advance batter to 1st
    new_state.fst = token.batter
    result.hits += 1
    result.bases_after = new_state  # Store BaseState directly, no conversion

    return result


def execute_DL(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.DL, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1

    if new_state.snd:
        new_state.snd = None
        result.runs += 1

    if new_state.fst:
        if get_random() <= scr_random():  # probability runner tries to score
            if get_random() <= out_random():  # probability thrown out
                new_state.fst = None
                result.outs += 1
            else:
                new_state.fst = None
                result.runs += 1
        else:
            new_state.thd = new_state.fst
            new_state.fst = None

    # Place batter on 2B
    new_state.snd = token.batter
    result.hits += 1

    # Finalize base state
    result.bases_after = new_state

    return result


def execute_TL(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.TL, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1

    if new_state.snd:
        new_state.snd = None
        result.runs += 1

    if new_state.fst:
        new_state.fst = None
        result.runs += 1

    new_state.thd = token.batter
    result.hits += 1
    result.bases_after = new_state

    return result


def execute_HR(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.HR, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()

    if new_state.thd:
        new_state.thd = None
        result.runs += 1

    if new_state.snd:
        new_state.snd = None
        result.runs += 1

    if new_state.fst:
        new_state.fst = None
        result.runs += 1

    result.hits += 1
    result.runs += 1
    result.bases_after = new_state

    return result
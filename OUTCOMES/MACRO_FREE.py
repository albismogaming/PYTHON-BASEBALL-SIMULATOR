from UTILITIES.ENUMS import *
from CONTEXT.PLAY_CONTEXT import PlayResult


def execute_BB(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.BB, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()
    
    if new_state.thd and new_state.snd and new_state.fst:
        new_state.thd = None
        result.runs += 1
    
    if new_state.snd and new_state.fst:
        new_state.thd = new_state.snd
        new_state.snd = None
    
    if new_state.fst:
        new_state.snd = new_state.fst
        new_state.fst = None

    # Batter gets hit and goes to 1st
    new_state.fst = token.batter
    result.bases_after = new_state
    
    return result
    

def execute_HP(gamestate, token) -> PlayResult:
    result = PlayResult(type=Macro.HP, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()
    
    # Runner on 3rd scores only if bases are loaded (forced to score)
    if new_state.thd and new_state.snd and new_state.fst:
        new_state.thd = None
        result.runs += 1
    
    # Runner on 2nd advances to 3rd (only if there's a runner on 1st to force them)
    if new_state.snd and new_state.fst:
        new_state.thd = new_state.snd
        new_state.snd = None
    
    # Runner on 1st ALWAYS advances to 2nd (forced by batter)
    if new_state.fst:
        new_state.snd = new_state.fst
        new_state.fst = None

    # Batter gets hit and goes to 1st
    new_state.fst = token.batter
    result.bases_after = new_state
    
    return result

    


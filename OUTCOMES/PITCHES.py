from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.ENUMS import Pitch


def execute_BL(gamestate, token) -> PlayResult:
    result = PlayResult(type=Pitch.BL, pitcher=token.pitcher, batter=token.batter, balls_delta=1)
    
    # Preserve current bases (pitch doesn't move runners)
    result.bases_before = gamestate.bases
    result.bases_after = gamestate.bases

    return result

def execute_CS(gamestate, token) -> PlayResult:
    result = PlayResult(type=Pitch.CS, pitcher=token.pitcher, batter=token.batter, strikes_delta=1)

    result.bases_before = gamestate.bases
    result.bases_after = gamestate.bases

    return result

def execute_FL(gamestate, token) -> PlayResult:
    result = PlayResult(type=Pitch.FL, pitcher=token.pitcher, batter=token.batter)
    if gamestate.strikes < 2:
        result.strikes_delta = 1

    result.bases_before = gamestate.bases
    result.bases_after = gamestate.bases
    
    return result

def execute_SW(gamestate, token) -> PlayResult:
    result = PlayResult(type=Pitch.SW, pitcher=token.pitcher, batter=token.batter, strikes_delta=1)

    result.bases_before = gamestate.bases
    result.bases_after = gamestate.bases

    return result
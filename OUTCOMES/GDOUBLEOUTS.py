from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.RANDOM import get_random
from UTILITIES.ENUMS import *

def execute_DP(gamestate, base_state, token) -> PlayResult:
    result = PlayResult(type=Macro.DP, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()
    rand_one = get_random()

    if base_state == 1:
        # Classic 6-4-3 or 4-6-3 double play
        new_state.fst = None
        result.outs += 2

    elif base_state == 3:
        if rand_one < 0.280:  # 28% - Runner on 2nd advances to 3rd, DP at 2nd and 1st
            new_state.thd = new_state.snd
            new_state.snd = None
            new_state.fst = None
            result.outs += 2

        elif rand_one < 0.980:  # 70% - Runner on 2nd out at 3rd, runner on 1st out at 2nd
            new_state.snd = None
            new_state.fst = None
            new_state.fst = token.batter
            result.outs += 2

        else:  # 2% - Runner on 2nd out at 3rd, batter out at 1st, runner on 1st advances to 2nd
            new_state.snd = None
            new_state.snd = new_state.fst
            new_state.fst = None
            result.outs += 2

    elif base_state == 5:
        # 6-4-3 or 4-6-3 double play, runner on 3rd scores (unless DP ends inning)
        if gamestate.outs == 1:  # DP ends inning, run doesn't count
            new_state.fst = None
            result.outs += 2

        else:  # 0 outs, run scores
            new_state.thd = None
            new_state.fst = None
            result.runs += 1
            result.outs += 2

    elif base_state == 7:
        if rand_one < 200:  # 20% - Out at home, then out at 1st (home-first DP)
            new_state.thd = None
            new_state.thd = new_state.snd
            new_state.snd = new_state.fst
            new_state.fst = None
            result.outs += 2

        elif rand_one < 0.240:  # 4% - Out at home, then out at 3rd (home-third DP)
            new_state.thd = None
            new_state.snd = None
            new_state.snd = new_state.fst
            new_state.fst = None
            new_state.fst = token.batter
            result.outs += 2

        elif rand_one < 0.960:  # 72% - Standard 6-4-3 DP, runner on 3rd scores (unless DP ends inning)
            if gamestate.outs == 1:  # DP ends inning, run doesn't count
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.fst = None 
                result.outs += 2

            else:  # 0 outs, run scores
                new_state.thd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                result.runs += 1
                result.outs += 2

        else:  # 4% - Out at 3rd and out at 2nd (rare), runner on 3rd scores (unless DP ends inning)
            if gamestate.outs == 1:  # DP ends inning, run doesn't count
                new_state.thd = None
                new_state.snd = None
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 2

            else:  # 0 outs, run scores
                new_state.thd = None
                new_state.snd = None
                new_state.fst = None
                new_state.fst = token.batter
                result.runs += 1
                result.outs += 2
    
    result.bases_after = new_state
    return result


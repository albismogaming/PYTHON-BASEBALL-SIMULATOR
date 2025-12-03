from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.RANDOM import get_random
from UTILITIES.ENUMS import *


def execute_FC(gamestate, base_state, token) -> PlayResult:
    result = PlayResult(type=Macro.GO, batter=token.batter, pitcher=token.pitcher)
    result.bases_before = gamestate.bases
    new_state = gamestate.bases.deepcopy()
    rand_one = get_random()
    rand_two = get_random()

    if base_state == 0:
        result.outs += 1

    elif base_state == 1:
        if gamestate.outs < 2:
            if rand_two < 0.650:
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

            else:
                new_state.snd = new_state.fst
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

        else:
            if rand_two < 0.350:
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

            else:
                new_state.snd = new_state.fst
                new_state.fst = None
                result.outs += 1

    elif base_state == 2:
        if gamestate.outs < 2:
            if rand_one < 0.700:  # 70% chance - routine ground out, runner holds at 2nd
                result.outs += 1

            else:  # 30% chance - runner advances to 3rd on ground out
                new_state.thd = new_state.snd
                new_state.snd = None
                result.outs += 1

        else:
            new_state.thd = new_state.snd
            new_state.snd = None
            result.outs += 1

    elif base_state == 4:
        if gamestate.outs < 2:
            if rand_one < 0.340:
                new_state.thd = None
                result.runs += 1
                result.outs += 1

            elif rand_one < 0.375:
                new_state.thd = None
                new_state.fst = token.batter
                result.outs += 1

            else:
                result.outs += 1

        else:
            new_state.thd = None
            result.outs += 1

    elif base_state == 3:
        if gamestate.outs < 2:
            if rand_one < 0.035:
                new_state.snd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

            elif rand_one < 0.600:
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1
            
            else:
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                result.outs += 1

        else:
            new_state.thd = new_state.snd
            new_state.snd = None
            new_state.snd = new_state.fst
            new_state.fst = None
            result.outs += 1

    elif base_state == 5:
        if gamestate.outs < 2:
            if rand_one < 0.150:  # 15% - Out at home, runners advance to 2nd and 1st
                new_state.thd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

            elif rand_one < 0.500:  # 35% - Force at 2nd, runner on 3rd scores, batter safe at 1st
                new_state.thd = None
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1
                result.runs += 1
            
            elif rand_one < 0.800:  # 30% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd scores
                new_state.thd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                result.outs += 1
                result.runs += 1
            
            else:  # 20% - Batter out at 1st, runner on 1st to 2nd, runner on 3rd holds
                new_state.snd = new_state.fst
                new_state.fst = None
                result.outs += 1

        else:  # 2 outs - batter out ends the inning, no runs score
                new_state.snd = new_state.fst
                new_state.fst = None
                result.outs += 1

    elif base_state == 6:
        if gamestate.outs < 2:
            if rand_one < 0.600:  # 60% - Batter out at 1st, runner on 3rd scores, runner on 2nd to 3rd
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                result.runs += 1
                result.outs += 1

            elif rand_one < 0.850:  # 25% - Batter out at 1st, runner on 3rd scores, runner on 2nd holds
                new_state.thd = None
                result.runs += 1
                result.outs += 1

            elif rand_one < 0.950:  # 10% - Out at home, runner on 2nd to 3rd, batter safe at 1st
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.fst = token.batter
                result.outs += 1

            else:  # 5% - Batter out at 1st, both runners hold
                result.outs += 1

        else:  # 2 outs - batter out ends inning, no runs score
            result.outs += 1

    elif base_state == 7:
        if gamestate.outs < 2:
            if rand_one < 0.400:  # 40% - Out at home, bases stay loaded
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

            elif rand_one < 0.750:  # 35% - Force at 2nd, runner on 3rd scores, runners on 1st and 3rd after
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.fst = None
                new_state.fst = token.batter
                result.runs += 1
                result.outs += 1

            elif rand_one < 0.900:  # 15% - Batter out at 1st, all runners advance, run scores
                new_state.thd = None
                new_state.thd = new_state.snd
                new_state.snd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                result.runs += 1
                result.outs += 1

            else:  # 10% - Out at 3rd, other runners advance
                new_state.thd = None
                new_state.snd = None
                new_state.snd = new_state.fst
                new_state.fst = None
                new_state.fst = token.batter
                result.outs += 1

        else:  # 2 outs - batter out ends inning, no runs score
            new_state.thd = None
            new_state.thd = new_state.snd
            new_state.snd = None
            new_state.snd = new_state.fst
            new_state.fst = None
            result.outs += 1

    result.bases_after = new_state
    
    return result






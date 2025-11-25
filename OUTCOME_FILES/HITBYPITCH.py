from UTILITIES.ENUMS import *

class HitByPitch:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 0

        bases = gamestate.bases
        r1 = bases[Base.FST] is not None
        r2 = bases[Base.SND] is not None
        r3 = bases[Base.THD] is not None

        # Process R3 → R2 → R1 (reverse order to avoid overwrites)
        # R3: Only forced if bases loaded
        if r3 and r2 and r1:
            # Bases loaded - R3 forced home
            gamestate.bases[Base.THD] = None
            runs += 1
        
        # R2: Only forced if R1 occupied
        if r2 and r1:
            # R2 forced to 3rd (R1 needs 2nd)
            gamestate.bases[Base.THD] = gamestate.bases[Base.SND]
            gamestate.bases[Base.SND] = None
        
        # R1: Always forced (batter needs 1st)
        if r1:
            gamestate.bases[Base.SND] = gamestate.bases[Base.FST]
            gamestate.bases[Base.FST] = None

        # Batter always advances to 1st on a walk
        gamestate.bases[Base.FST] = batter
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }

    


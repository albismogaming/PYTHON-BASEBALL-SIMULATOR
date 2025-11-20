from UTILITIES.ENUMS import *

class Strikeout:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 1

        # All runners hold on strikeout, batter out
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
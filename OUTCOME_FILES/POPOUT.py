from UTILITIES.ENUMS import *

class Popout:
    def execute(self, gamestate, batter, pitcher):
        hits = 0
        runs = 0
        outs = 1
        
        return {
            'hits': hits,
            'runs': runs,
            'outs': outs,
            'rbis': runs,
        }
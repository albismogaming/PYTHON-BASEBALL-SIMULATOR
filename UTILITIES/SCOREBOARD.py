from UTILITIES.ENUMS import InningHalf, Base
from UTILITIES.FUNCTIONS import *
from UTILITIES.COLOR_CODES import *
from tabulate import tabulate

class Scoreboard:
    @staticmethod
    def scoreboard(gamestate):
        net = rgb_colored(f"= MLB =", WHITE, DARK_GRAY)
        tob = rgb_colored(" ▲ ", YELLOW, DARK_GRAY) if gamestate.inninghalf == InningHalf.TOP else rgb_colored(" ▼ ", YELLOW, DARK_GRAY)
        inn = rgb_colored(f" {ordinal(gamestate.current_inning):4} ", YELLOW, DARK_GRAY)
        out = rgb_colored(f" {(gamestate.outs)} OUTS ", YELLOW, DARK_GRAY)
        bns = rgb_colored(f" {gamestate.balls} - {gamestate.strikes} ", YELLOW, DARK_GRAY)

        awt = rgb_colored(f" {gamestate.away_team.abbreviation:7}  ", WHITE, DODGER_BLUE)
        aws = rgb_colored(f" {(gamestate.stats['away_team']['score']):2} ", BLACK, WHITE)
        
        hmt = rgb_colored(f" {gamestate.home_team.abbreviation:7}  ", WHITE, NAVY_BLUE)
        hms = rgb_colored(f" {(gamestate.stats['home_team']['score']):2} ", BLACK, WHITE)
        
        div = rgb_colored(f"┃", WHITE)
        fst = rgb_colored("▄▄", GOLDEN_YELLOW) if gamestate.bases.fst else rgb_colored("▄▄", WHITE)
        snd = rgb_colored("▀▀", GOLDEN_YELLOW) if gamestate.bases.snd else rgb_colored("▀▀", WHITE)
        thd = rgb_colored("▄▄", GOLDEN_YELLOW) if gamestate.bases.thd else rgb_colored("▄▄", WHITE)

        scoreboard = f"""
{rgb_colored(f"┏━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┓", WHITE)}
{div}{net}{div}{awt}{aws}{div}{hmt}{hms}{div}{tob}{inn}{div}{out}{div}{bns}{div} {thd}{snd}{fst} {div}
{rgb_colored(f"┗━━━━━━━┻━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━┻━━━━━━━┻━━━━━━━━┛", WHITE)}"""
        print(scoreboard)

    @staticmethod
    def inning_start(gamestate, inning_half):
        message = f"""
{rgb_colored("\n" + "="*77, WHITE)}
{rgb_colored(f"{inning_half.name} OF {ordinal(gamestate.current_inning)} INNING || {gamestate.batting_team.abbreviation} BATTING", WHITE)}
{rgb_colored("="*77, WHITE)}"""
        print(message)

    @staticmethod
    def boxscore(gamestate):
        max_innings = max(len(gamestate.stats['away_team']['score_by_inning']), len(gamestate.stats['home_team']['score_by_inning']))

        # Append 'X' if the game ends and the home team does not bat in what would be their half of the inning
        if gamestate.current_inning >= 9 and gamestate.stats['home_team']['score'] > gamestate.stats['away_team']['score'] and gamestate.inninghalf == InningHalf.TOP:
            while len(gamestate.stats['home_team']['score_by_inning']) < gamestate.current_inning:  # Ensure there's space for 'X'
                gamestate.stats['home_team']['score_by_inning'].append(0)  # Pad innings if needed before appending 'X'
            gamestate.stats['home_team']['score_by_inning'][-1] = 'X'  # Replace the last 0 or append 'X'

        # Coloring and preparing headers
        headers = [rgb_colored("FINAL", YELLOW)] + \
                  [rgb_colored(f"{(i)}", YELLOW) for i in range(1, max_innings + 1)] + \
                  [rgb_colored("R", YELLOW), 
                   rgb_colored("H", YELLOW), 
                   rgb_colored("E", YELLOW)]

        away_row = [rgb_colored(f"{gamestate.away_team.abbreviation}", RED)] + \
                   [rgb_colored(str(score), WHITE) for score in gamestate.stats['away_team']['score_by_inning']] + \
                   [rgb_colored(str(gamestate.stats['away_team']['score']), RED), 
                    rgb_colored(str(gamestate.stats['away_team']['hits']), RED), 
                    rgb_colored(str(gamestate.stats['away_team']['errors']), RED)]

        home_row = [rgb_colored(f"{gamestate.home_team.abbreviation}", BLUE)] + \
                   [rgb_colored(str(score), WHITE) for score in gamestate.stats['home_team']['score_by_inning']] + \
                   [rgb_colored(str(gamestate.stats['home_team']['score']), BLUE), 
                    rgb_colored(str(gamestate.stats['home_team']['hits']), BLUE), 
                    rgb_colored(str(gamestate.stats['home_team']['errors']), BLUE)]

        print(tabulate([away_row, home_row], headers=headers, tablefmt="heavy_grid", numalign="center", stralign="center"))

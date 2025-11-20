import time
import re
import numpy as np
from termcolor import colored

@staticmethod
def rgb_colored(text, rgb, bg_rgb=None):
    """
    Apply RGB color to text, with an optional background color.

    :param text: The text to color.
    :param rgb: Tuple for the text color (r, g, b).
    :param bg_rgb: Optional tuple for the background color (r, g, b).
    :return: Formatted text with RGB color.
    """
    r, g, b = rgb
    if bg_rgb:
        br, bg, bb = bg_rgb
        return f"\033[1m\033[38;2;{r};{g};{b}m\033[48;2;{br};{bg};{bb}m{text}\033[0m"  # Bold with foreground and background
    else:
        return f"\033[1m\033[38;2;{r};{g};{b}m{text}\033[0m"  # Bold with foreground only

def ordinal(n):
    return "%d%s" % (n,"TSNRHTDD"[(n//10%10!=1)*(n%10<4)*n%10::4])

def strip_ansi(text):
    """Remove ANSI color codes from text."""
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def time_format(secs):
    mins = int(secs // 60)
    rem_secs = int(secs % 60)
    formatted = f'{mins:02d}:{rem_secs:02d}'
    return formatted

def print_delay(items, delay=0):
    for item in items:
        print(item, end='', flush=True)  # `flush=True` forces the output to be written immediately
        time.sleep(delay)  # Wait for 'delay' seconds before printing the next item
    print()  # Move to the next line after all items are printed


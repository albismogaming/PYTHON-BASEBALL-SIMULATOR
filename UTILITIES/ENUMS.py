from enum import Enum

class InningHalf(Enum):
    TOP = "TOP"
    BOT = "BOT"

class Base(Enum):
    BAT = "BAT"
    FST = "1ST"
    SND = "2ND"
    THD = "3RD"
    HME = "HME"

class Outcome(Enum):
    """All possible at-bat outcomes"""
    SO = "STRIKEOUT"
    BB = "BASE_ON_BALLS"
    HP = "HIT_BY_PITCH"
    IH = "INFIELD_HIT"
    SL = "SINGLE"
    DL = "DOUBLE"
    TL = "TRIPLE"
    HR = "HOMERUN"
    GO = "GROUNDOUT"
    FO = "FLYOUT"
    LO = "LINEOUT"
    PO = "POPOUT"

class HitTypes(Enum):
    GB = "GROUNDBALL"
    FB = "FLYBALL"
    LD = "LINEDRIVE"
    PU = "POPUP"

class PitchResult(Enum):
    """Pitch result codes for pitch sequences"""
    B = "B"    # Ball
    C = "C"    # Called strike
    S = "S"    # Swinging strike
    F = "F"    # Foul ball
    H = "H"    # Hit by pitch
    X = "X"    # Ball in play (contact made)

class Positions(Enum):
    """Defensive positions by number"""
    _SP = 1
    _RP = 2
    _1B = 3
    _2B = 4
    _3B = 5
    _SS = 6
    _LF = 7
    _CF = 8
    _RF = 9
    _DH = 0
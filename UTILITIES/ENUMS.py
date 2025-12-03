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

class EventType(Enum):
    PITCH = "PITCH"
    MICRO = "MICRO"
    MACRO = "MACRO"
    OTHER = "OTHER"

class Pitch(Enum):
    """Pitch result codes for pitch sequences"""
    NA = "NA"
    BL = "B"
    CS = "C"
    SW = "S"
    FL = "F"
    IP = "X"

class Micro(Enum):
    """All possible at-bat outcomes"""
    NA = "NA"
    WP = "WP"
    PB = "PB"
    BK = "BK"
    SB = "SB"
    P1 = "P1"

class Macro(Enum):
    NA = "NA"
    SO = "SO"
    BB = "BB"
    HP = "HP"
    IH = "IH"
    SL = "SL"
    DL = "DL"
    TL = "TL"
    HR = "HR"
    GO = "GO"
    DP = "DP"
    FC = "FC"
    FO = "FO"
    LO = "LO"
    PO = "PO"
    
class HitTypes(Enum):
    GB = "GB"
    FB = "FB"
    LD = "LD"
    PU = "PU"

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

class StatKey(Enum):
    """Player stat keys for outcome probability calculations"""
    BA = "BA"      # Batting average (BABIP)
    SO = "SO"      # Strikeouts
    BB = "BB"      # Walks
    HP = "HP"      # Hit by pitch
    HR = "HR"      # Home runs
    IH = "IH"      # Infield hits
    SL = "SL"      # Singles
    DL = "DL"      # Doubles
    TL = "TL"      # Triples
    GO = "GO"      # Ground outs
    FO = "FO"      # Fly outs
    LO = "LO"      # Line outs
    PO = "PO"      # Pop outs
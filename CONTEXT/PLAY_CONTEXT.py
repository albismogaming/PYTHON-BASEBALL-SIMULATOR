from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from UTILITIES.ENUMS import *
from CONTEXT.HIT_CONTEXT import HitInfo

@dataclass
class PlayContext:
    """
    Complete context for a play (at-bat outcome).
    Matches C# PlayContext structure.
    """
    # Required fields (must be provided at creation)
    batter: object                            # Batter PlayerContext
    pitcher: object                           # Pitcher PlayerContext
    description: str                          # "HOMERUN", "SINGLE", "GROUNDOUT", etc.
    outcome: Optional[Outcome] = None        # Outcome enum
    
    # Play identification
    at_bat_id: str = field(default_factory=lambda: str(uuid4()))  # Unique ID for this at-bat
    
    # Outcome token (if using token system)
    token: Optional[object] = None            # OutcomeToken object
    
    # Hit information - complete HitInfo object with all batted ball data
    hit_info: Optional[HitInfo] = None        # HitInfo object (hit_type, hit_sector, hit_location, hit_fielder)

    # Pitch Information
    pitch_sequence: Optional[str] = None
    pitches_thrown: int = 0

    # Play outcomes
    hits_hit: int = 0                         # Number of hits (0 or 1)
    runs_scored: int = 0                      # Total runs scored on this play
    outs_recorded: int = 0                    # Outs recorded on this play
    errors_made: int = 0                      # Errors committed on this play
    
    # Play status flags
    is_complete: bool = False                 # Is the play complete?
    at_bat_complete: bool = False             # Is the at-bat over?
    is_walk_off: bool = False                 # Did this play end the game?
    is_error: bool = False                    # Was there an error?
    is_ball_in_play: bool = False             # Was the ball put in play?
    is_extra_event: bool = False              # Is this an extra event (WP, PB, etc)?
    
    # Runner contexts - what happened to each runner
    on_bat: Optional[object] = None           # RunnerContext for batter
    on_fst: Optional[object] = None           # RunnerContext for runner on 1st
    on_snd: Optional[object] = None           # RunnerContext for runner on 2nd
    on_thd: Optional[object] = None           # RunnerContext for runner on 3rd
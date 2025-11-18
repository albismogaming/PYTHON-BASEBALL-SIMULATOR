from dataclasses import dataclass
from typing import Optional
from UTILITIES.ENUMS import Base

@dataclass
class RunnerContext:
    """
    Complete context for a runner's action during a play.
    Describes what happened to a specific runner.
    """
    runner: object                    # The player object
    start_base: Base                  # Where they started (can be Base.BAT)
    end_base: Optional[Base]          # Where they ended up (None if out/scored)
    out_base: Optional[Base]          # Where they were thrown out (if applicable)
    advanced: bool                    # Did they advance at least one base?
    held: bool                        # Did they stay at their base?
    scored: bool                      # Did they score?
    was_out: bool                     # Were they thrown out?
    description: str                  # Text description of what happened


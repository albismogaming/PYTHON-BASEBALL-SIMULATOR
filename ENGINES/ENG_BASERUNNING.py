from UTILITIES.ENUMS import *
from dataclasses import dataclass
from typing import Optional
from CONTEXT.RUNNER_CONTEXT import RunnerContext

class BaseRunnerEngine:
    """
    Stateless manager for base running operations.
    All methods are static and accept gamestate as a parameter.
    """

    @staticmethod
    def create_context(gamestate, from_base: Base, to_base: Optional[Base], 
                      adv: bool, scr: bool, hld: bool, is_out: bool, 
                      desc: str, runner=None) -> Optional[RunnerContext]:
        """
        Create a runner context for a base running action.
        Returns None if no runner exists at from_base (unless runner is provided).
        """
        # If runner not provided, get from gamestate
        if runner is None:
            if from_base == Base.BAT:
                return None  # Batter must be passed explicitly
            runner = gamestate.bases.get(from_base)
            if runner is None:
                return None  # No runner to create context for
        
        return RunnerContext(
            runner=runner,
            start_base=from_base,
            end_base=to_base,
            out_base=to_base if is_out else None,
            advanced=adv,
            held=hld,
            scored=scr,
            was_out=is_out,
            description=desc
        )

    @staticmethod
    def adv_batter(gamestate, to_base: Base, batter):
        """Advance the batter to a specified base."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=Base.BAT,
            to_base=to_base,
            adv=True,
            scr=False,
            hld=False,
            is_out=False,
            desc=f"BATTER ADVANCES TO {to_base.value}",
            runner=batter
        )
        
        # Update bases
        gamestate.bases[to_base] = batter
        return ctx  # Always returns RunnerContext since batter is provided
    
    @staticmethod
    def adv_runner(gamestate, from_base: Base, to_base: Base) -> Optional[RunnerContext]:
        """Advance a runner from one base to another."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=from_base,
            to_base=to_base,
            adv=True,
            scr=False,
            hld=False,
            is_out=False,
            desc=f"RUNNER ADVANCES FROM {from_base.value} -> {to_base.value}"
        )
        
        if ctx is None:
            return None
        
        # Update bases
        gamestate.bases[to_base] = gamestate.bases[from_base]
        gamestate.bases[from_base] = None
        return ctx

    @staticmethod
    def hld_runner(gamestate, from_base: Base) -> Optional[RunnerContext]:
        """Hold a runner on a base (no movement)."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=from_base,
            to_base=from_base,  # End where they started
            adv=False,
            scr=False,
            hld=True,
            is_out=False,
            desc=f"RUNNER HOLDS AT {from_base.value}"
        )
        
        # No base update needed - runner stays put
        return ctx

    @staticmethod
    def scr_runner(gamestate, from_base: Base) -> Optional[RunnerContext]:
        """Score a runner from a base."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=from_base,
            to_base=Base.HME,
            adv=True,
            scr=True,
            hld=False,
            is_out=False,
            desc=f"RUNNER SCORES FROM {from_base.value}"
        )
        
        if ctx is None:
            return None
        
        # Clear the base
        gamestate.bases[from_base] = None
        return ctx
    
    @staticmethod
    def scr_batter(gamestate, batter):
        """Score the batter directly (homerun)."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=Base.BAT,
            to_base=Base.HME,
            adv=True,
            scr=True,
            hld=False,
            is_out=False,
            desc=f"BATTER SCORES",
            runner=batter
        )
        
        # No base update needed - batter scoring directly
        return ctx  # Always returns RunnerContext since batter is provided

    @staticmethod
    def out_runner(gamestate, from_base: Base, to_base: Base) -> Optional[RunnerContext]:
        """Record an out for a runner attempting to advance."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=from_base,
            to_base=to_base,
            adv=False,
            scr=False,
            hld=False,
            is_out=True,
            desc=f"RUNNER OUT {from_base.value} -> {to_base.value}"
        )
        
        if ctx is None:
            return None
        
        # Clear the base
        gamestate.bases[from_base] = None
        return ctx
    
    @staticmethod
    def out_batter(gamestate, to_base: Base, batter):
        """Record the batter being thrown out."""
        ctx = BaseRunnerEngine.create_context(
            gamestate=gamestate,
            from_base=Base.BAT,
            to_base=to_base,
            adv=False,
            scr=False,
            hld=False,
            is_out=True,
            desc=f"BATTER OUT AT {to_base.value}",
            runner=batter
        )
        
        # No base update needed - batter is out
        return ctx  # Always returns RunnerContext since batter is provided
    
    @staticmethod
    def clear_bases(gamestate):
        """Clear all bases (e.g., for inning change)."""
        gamestate.bases = {Base.FST: None, Base.SND: None, Base.THD: None}
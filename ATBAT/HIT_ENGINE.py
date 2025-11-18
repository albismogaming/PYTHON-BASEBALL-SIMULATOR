from CONTEXT.HIT_CONTEXT import HitInfo
from UTILITIES.ENUMS import HitSectors, HitTypes, Positions, Outcome
from ATBAT.HIT_LOCATION import HitLocationGenerator
from ATBAT.HIT_TYPE import BattedBallTypeGenerator
from ATBAT.HIT_SPRAY import SprayDirectionGenerator
from ATBAT.HIT_DEPTH import HitDepthGenerator

class HitEngine:
    """
    Stateless orchestrator for generating complete hit information.
    Coordinates specialized generators:
    - BattedBallTypeGenerator: Determines GB/FB/LD/PU
    - SprayDirectionGenerator: Determines sector (LL, LF, LC, CF, RC, RF, RL)
    - HitDepthGenerator: Determines depth (SH, MD, DP, XD)
    - HitLocationGenerator: Determines fielder and Retrosheet code
    """
    
    @classmethod
    def generate_hit_info(cls, outcome, batter) -> HitInfo:
        """
        Generate complete hit information using specialized generators.
        
        Args:
            outcome: Outcome enum (e.g., Outcome.SL, Outcome.HR)
            batter: Batter Player object
        
        Returns:
            HitInfo object with hit_type, hit_sector, hit_depth, hit_fielder, retrosheet_code
        """
        # Convert outcome enum to string value
        outcome_value = outcome.value if hasattr(outcome, 'value') else str(outcome)
        
        # Get batter characteristics
        batter_handedness = batter.bats.upper()
        batter_profile = batter.bat_profile if hasattr(batter, 'bat_profile') and batter.bat_profile is not None else 1
        
        # Step 1: Generate batted ball type (GB, FB, LD, PU)
        hit_type = BattedBallTypeGenerator.determine_hit_type(outcome_value, batter_profile)
        
        # Step 2: Generate spray direction (LL, LF, LC, CF, RC, RF, RL)
        hit_sector = SprayDirectionGenerator.determine_spray_direction(
            outcome_value, 
            batter_handedness, 
            hit_type, 
            batter_profile
        )
        
        # Step 3: Generate hit depth (SH, MD, DP, XD) with sector modifier
        hit_depth = HitDepthGenerator.determine_hit_depth(
            outcome_value, 
            hit_type,
            hit_sector
        )
        
        # Step 4: Determine which fielder makes the play
        fielder_position_num = HitLocationGenerator.determine_fielder(
            hit_type, 
            hit_sector, 
            hit_depth.value  # Convert HitDepths enum to string
        )
        
        # Convert position number to Positions enum
        position_map = {
            1: Positions._SP,
            2: Positions._RP,
            3: Positions._1B,
            4: Positions._2B,
            5: Positions._3B,
            6: Positions._SS,
            7: Positions._LF,
            8: Positions._CF,
            9: Positions._RF
        }
        hit_fielder = position_map.get(fielder_position_num, Positions._CF)
        
        # Step 5: Generate Retrosheet location code for notation
        retrosheet_code = HitLocationGenerator.generate_retrosheet_location(
            hit_type, 
            hit_sector, 
            hit_depth.value,  # Convert HitDepths enum to string
            fielder_position_num
        )
        
        return HitInfo(
            hit_type=hit_type,
            hit_sector=hit_sector,
            hit_depth=hit_depth,
            hit_fielder=hit_fielder,
            retrosheet_code=retrosheet_code
        )
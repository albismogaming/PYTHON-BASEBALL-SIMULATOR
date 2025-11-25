from typing import List
from PLAYOFFS.PLAYOFF_CONFIG import PLAYOFF_FORMATS, ACTIVE_FORMAT
from PLAYOFFS.BRACKET_PLAYOFF import BracketPlayoff
from PLAYOFFS.POOL_PLAY_PLAYOFF import PoolPlayPlayoff


class PlayoffFactory:
    """Factory to create playoff simulators based on format."""
    
    @staticmethod
    def create_playoff(teams: List[str], format_name: str = ""):
        """ Create playoff simulator based on format. """
        format_name = format_name or ACTIVE_FORMAT
        
        if format_name not in PLAYOFF_FORMATS:
            raise ValueError(f"Unknown playoff format: {format_name}")
        
        config = PLAYOFF_FORMATS[format_name]
        playoff_type = config.get('type', 'standard')
        
        # Validate team count
        if len(teams) != config['num_teams']:
            raise ValueError(f"Format '{format_name}' requires {config['num_teams']} teams, got {len(teams)}")
        
        # Create appropriate playoff simulator
        if playoff_type == 'standard':
            return BracketPlayoff(teams, config)
        elif playoff_type == 'pool_play':
            return PoolPlayPlayoff(teams, config)
        else:
            raise ValueError(f"Unknown playoff type: {playoff_type}")
    
    @staticmethod
    def get_available_formats() -> dict:
        """Get all available playoff formats."""
        return PLAYOFF_FORMATS
    
    @staticmethod
    def get_format_info(format_name: str) -> dict:
        """Get information about a specific format."""
        if format_name not in PLAYOFF_FORMATS:
            raise ValueError(f"Unknown playoff format: {format_name}")
        return PLAYOFF_FORMATS[format_name]

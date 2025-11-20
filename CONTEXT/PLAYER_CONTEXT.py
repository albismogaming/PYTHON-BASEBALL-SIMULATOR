from dataclasses import dataclass, field as dataclass_field
from typing import Dict, Optional


@dataclass
class Player:
    """
    Player with stats needed for simulation.
    Holds raw rates extracted from CSV - OutcomeBuilder will use these for probability calculations.
    """
    # Identity
    player_id: int
    team_abbrev: str
    first_name: str
    last_name: str
    age: int
    position: str
    bats: str  # L, R, or B (both/switch)
    throws: str  # L or R
    
    # Raw stats (only used for precomputation, not during simulation)
    bat_stats_raw: Dict[str, float]  # SO, BB, HP, HR, IH, SL, DL, TL, BABIP, GBFB
    pit_stats_raw: Dict[str, float]  # SO, BB, HP, HR, IH, SL, DL, TL, BABIP, GBFB
    
    # Additional attributes
    bat_profile: Optional[int] = None  # Batter profile for hit type distribution
    average: Optional[float] = None
    clutch: Optional[float] = None
    speed: Optional[float] = None  # Batters only
    field: Optional[float] = None  # Batters only
    
    # Game stats (populated during game simulation)
    bat_stats: Dict[str, int] = dataclass_field(default_factory=dict)
    pit_stats: Dict[str, int] = dataclass_field(default_factory=dict)
    
    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.team_abbrev}) - {self.position}"
    
    @property
    def full_name(self):
        """Get player's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_switch_hitter(self):
        """Check if player is a switch hitter."""
        return self.bats == 'B'
    
    @staticmethod
    def from_csv_row(row: dict, team_abbrev: str) -> 'Player':
        """
        Create Player from CSV row dictionary.
        
        Args:
            row: Dictionary from pandas DataFrame row
            team_abbrev: Team abbreviation
            
        Returns:
            Player instance
        """
        # Extract all batter stats into flat dict
        bat_stats_raw = {
            'SO': row['b_SO'],
            'BB': row['b_BB'],
            'HP': row['b_HP'],
            'HR': row['b_HR'],
            'IH': row['b_IH'],
            'SL': row['b_SL'],
            'DL': row['b_DL'],
            'TL': row['b_TL'],
            'BABIP': row['b_BABIP'],
            'GBFB': row['b_GBFB']
        }
        
        # Extract all pitcher stats into flat dict
        pit_stats_raw = {
            'SO': row['p_SO'],
            'BB': row['p_BB'],
            'HP': row['p_HP'],
            'HR': row['p_HR'],
            'IH': row['p_IH'],
            'SL': row['p_SL'],
            'DL': row['p_DL'],
            'TL': row['p_TL'],
            'BABIP': row['p_BABIP'],
            'GBFB': row['p_GBFB']
        }
        
        return Player(
            player_id=row['player_id'],
            team_abbrev=team_abbrev,
            first_name=row['FIRST'],
            last_name=row['LAST'],
            age=row['AGE'],
            position=row['POS'],
            bats=row['B'],
            throws=row['T'],
            bat_stats_raw=bat_stats_raw,
            pit_stats_raw=pit_stats_raw,
            bat_profile=row['BAT_PROFILE'],
            average=row['AVG'],
            clutch=row['CLU'],
            speed=row.get('SPD'),
            field=row.get('FLD'),
        )
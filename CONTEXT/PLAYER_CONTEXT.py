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
    
    # Handedness
    bats: str  # L, R, or B (both/switch)
    throws: str  # L or R
    
    # Batter stats (raw rates for OutcomeBuilder)
    bat_base_stats: Dict[str, float]  # SO, BB, HP, HR rates
    bat_hit_stats: Dict[str, float]  # SL, DL, TL, IH rates
    
    # Pitcher stats (raw rates for OutcomeBuilder)
    pit_base_stats: Dict[str, float]  # SO, BB, HP, HR rates
    pit_hit_stats: Dict[str, float]  # SL, DL, TL, IH rates

    # Contact quality
    b_babip: float
    p_babip: float
    b_gbfb: float  # Ground ball to fly ball ratio
    p_gbfb: float  # Ground ball to fly ball ratio
    
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
        # Extract base outcome rates (for OutcomeBuilder)
        bat_base_stats = {
            'SO': row['b_SO'],
            'BB': row['b_BB'],
            'HP': row['b_HP'],
            'HR': row['b_HR']
        }
        
        # Extract hit type rates (for OutcomeBuilder)
        bat_hit_stats = {
            'IH': row['b_IH'],
            'SL': row['b_SL'],
            'DL': row['b_DL'],
            'TL': row['b_TL'],
        }
        
        pit_base_stats = {
            'SO': row['b_SO'],
            'BB': row['b_BB'],
            'HP': row['b_HP'],
            'HR': row['b_HR']
        }
        
        # Extract hit type rates (for OutcomeBuilder)
        pit_hit_stats = {
            'IH': row['b_IH'],
            'SL': row['b_SL'],
            'DL': row['b_DL'],
            'TL': row['b_TL'],
        }
        
        return Player(
            player_id=row['id'],
            team_abbrev=team_abbrev,
            first_name=row['FIRST'],
            last_name=row['LAST'],
            age=row['AGE'],
            position=row['POS'],
            bats=row['B'],
            throws=row['T'],
            bat_base_stats=bat_base_stats,
            bat_hit_stats=bat_hit_stats,
            pit_base_stats=pit_base_stats,
            pit_hit_stats=pit_hit_stats,
            b_babip=row['b_BABIP'],
            b_gbfb=row['b_GBFB'],
            p_babip=row['p_BABIP'],
            p_gbfb=row['p_GBFB'],
            bat_profile=row['BAT_PROFILE'],
            average=row['AVG'],
            clutch=row['CLU'],
            speed=row.get('SPD'),
            field=row.get('FLD'),
        )
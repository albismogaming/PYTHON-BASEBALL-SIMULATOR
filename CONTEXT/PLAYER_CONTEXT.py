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
    base_stats: Dict[str, float]  # SO, BB, HP, HR, BA (BABIP)
    hits_stats: Dict[str, float]   # IH, SL, DL, TL
    outs_stats: Dict[str, float]   # GO, FO, LO, PO
    
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
    
    @staticmethod
    def from_csv_row(row: dict, team_abbrev: str) -> 'Player':
        """ Create Player from CSV row dictionary. """
        # Extract base outcome stats (strikeout, walk, hit by pitch, home run, BABIP)
        base_stats = {
            'SO': row['SO'],
            'BB': row['BB'],
            'HP': row['HP'],
            'HR': row['HR'],
            'BA': row['BABIP']
        }
        
        # Extract hit type distribution (infield hit, single, double, triple)
        hits_stats = {
            'IH': row['IH'],
            'SL': row['SL'],
            'DL': row['DL'],
            'TL': row['TL']
        }
        
        # Extract out type distribution (ground out, fly out, line out, pop out)
        outs_stats = {
            'GO': row['GO'],
            'FO': row['FO'],
            'LO': row['LO'],
            'PO': row['PO']
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
            base_stats=base_stats,
            hits_stats=hits_stats,
            outs_stats=outs_stats,
            bat_profile=row['BAT_PROFILE'],
            average=row['AVG'],
            clutch=row['CLU'],
            speed=row.get('SPD'),
            field=row.get('FLD'),
        )
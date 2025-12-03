from dataclasses import dataclass, field as dataclass_field
from typing import Dict, Optional


@dataclass
class Player:
    """ Player with stats needed for simulation. """
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
    stats_vl: Dict[str, float]  # SO, BB, HP, HR, BA (BABIP)
    stats_vr: Dict[str, float]   # IH, SL, DL, TL
    
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
        stats_vl = {
            'BA': row['BAvl'],
            'SO': row['SOvl'],
            'BB': row['BBvl'],
            'HP': row['HP'],
            'HR': row['HRvl'],
            'IH': row['IHvl'],
            'SL': row['SLvl'],
            'DL': row['DLvl'],
            'TL': row['TLvl'],
            'GO': row['GOvl'],
            'FO': row['FOvl'],
            'LO': row['LOvl'],
            'PO': row['POvl']
        }

        stats_vr = {
            'BA': row['BAvr'],
            'SO': row['SOvr'],
            'BB': row['BBvr'],
            'HP': row['HP'],
            'HR': row['HRvr'],
            'IH': row['IHvr'],
            'SL': row['SLvr'],
            'DL': row['DLvr'],
            'TL': row['TLvr'],
            'GO': row['GOvr'],
            'FO': row['FOvr'],
            'LO': row['LOvr'],
            'PO': row['POvr']
        }
        
        return Player(
            player_id=row['PLAYER_ID'],
            team_abbrev=team_abbrev,
            first_name=row['FIRST'],
            last_name=row['LAST'],
            age=row['AGE'],
            position=row['POS'],
            bats=row['BAT'],
            throws=row['THR'],
            stats_vl=stats_vl,
            stats_vr=stats_vr,
            bat_profile=row['BAT_PROFILE'],
            average=row['AVG'],
            clutch=row['CLU'],
            speed=row.get('SPD'),
            field=row.get('FLD'),
        )
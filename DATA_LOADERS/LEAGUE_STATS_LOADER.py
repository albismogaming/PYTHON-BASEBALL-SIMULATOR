from CONTEXT.LEAGUE_CONTEXT import LeagueData
from typing import Optional
import pandas as pd

class LeagueLoader:
    """Static methods for loading league-average data and park factors."""
    
    # Class-level cache for league data
    _league_data: Optional[LeagueData] = None
    
    @classmethod
    def load_league_data(cls, csv_path: str, year: Optional[int] = 2025) -> LeagueData:
        """ Load league-average rates from CSV and cache for reuse. """
        df = pd.read_csv(csv_path)
        
        # If year specified, filter; otherwise take first/most recent row
        if year is not None:
            df = df[df['YEAR'] == year]
        
        if len(df) == 0:
            raise ValueError(f"No league data found for year {year}")
        
        row = df.iloc[0]
        
        # Load all factors into a single flat dictionary
        factors = {
            'BA': float(row['BABIP']),
            'SO': float(row['SO']),
            'BB': float(row['BB']),
            'HP': float(row['HP']),
            'HR': float(row['HR']),
            'IH': float(row['IH']),
            'SL': float(row['SL']),
            'DL': float(row['DL']),
            'TL': float(row['TL']),
            'GO': float(row['GO']),
            'FO': float(row['FO']),
            'LO': float(row['LO']),
            'PO': float(row['PO'])
        }

        cls._league_data = LeagueData(
            year=int(row['YEAR']),
            factors=factors
        )
        return cls._league_data
    
    @classmethod
    def get_league_factors(cls) -> Optional[dict]:
        """Get cached league factors, or None if not loaded."""
        return cls._league_data.factors if cls._league_data else None
    

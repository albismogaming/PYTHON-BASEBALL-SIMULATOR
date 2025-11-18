from CONTEXT.LEAGUE_CONTEXT import LeagueData
from typing import Optional
import pandas as pd

class LeagueLoader:
    """Static methods for loading league-average data and park factors."""
    
    @staticmethod
    def load_league_data(csv_path: str, year: Optional[int] = 2025) -> LeagueData:
        """
        Load league-average rates from CSV.
        
        Args:
            csv_path: Path to LEAGUE_FACTORS.csv
            year: Optional year to filter by (if CSV has multiple years)
            
        Returns:
            LeagueData object with league-average rates
        """
        df = pd.read_csv(csv_path)
        
        # If year specified, filter; otherwise take first/most recent row
        if year is not None:
            df = df[df['YEAR'] == year]
        
        if len(df) == 0:
            raise ValueError(f"No league data found for year {year}")
        
        row = df.iloc[0]
        
        base_factors = {
            'SO': float(row['STRIKEOUT']),
            'BB': float(row['WALK']),
            'HP': float(row['HITBYPITCH']),
            'HR': float(row['HOMERUN'])
        }

        hit_factors = {
            'IH': float(row['INFIELDS']),
            'SL': float(row['SINGLE']),
            'DL': float(row['DOUBLE']),
            'TL': float(row['TRIPLE']),
        }

        return LeagueData(
            year=int(row['YEAR']),
            babip_factor=float(row['BABIP']),
            base_factors=base_factors,
            hit_factors=hit_factors,
            gbfb_factor=float(row['GBFB'])
        )
    

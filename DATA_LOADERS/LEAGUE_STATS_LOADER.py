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
        
        # Load all factors into a single flat dictionary
        factors = {
            'SO': float(row['SO']),
            'BB': float(row['BB']),
            'HP': float(row['HP']),
            'HR': float(row['HR']),
            'IH': float(row['IH']),
            'SL': float(row['SL']),
            'DL': float(row['DL']),
            'TL': float(row['TL']),
            'BABIP': float(row['BABIP']),
            'GBFB': float(row['GBFB'])
        }

        return LeagueData(
            year=int(row['YEAR']),
            factors=factors
        )
    

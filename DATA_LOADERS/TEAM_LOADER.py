import pandas as pd
from CONTEXT.TEAM_CONTEXT import Team
from CONTEXT.PLAYER_CONTEXT import Player

class TeamLoader:
    """Static methods for loading teams with rosters and park factors."""
    
    @staticmethod
    def load_team_metadata(csv_path: str) -> dict:
        """
        Load all teams' basic info for selection.
        
        Args:
            csv_path: Path to TEAMS.csv (now includes stadium/park factors)
            
        Returns:
            Dictionary mapping team abbreviation to metadata dict
        """
        # Try multiple encodings to handle special characters
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(csv_path, encoding='latin-1')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_path, encoding='cp1252')
        
        return {row['team_abbrev']: row.to_dict() for _, row in df.iterrows()}
    
    @staticmethod
    def load_full_team(team_abbrev: str, 
                      roster_csv: str,
                      teams_csv: str) -> Team:
        """
        Load complete team (metadata + roster + park factors) for simulation.
        
        Args:
            team_abbrev: Team abbreviation (e.g., "NYY", "LAD")
            roster_csv: Path to team's roster CSV (e.g., "GAME_DATA/TEAMS/LAD/LAD_BAT.csv")
            teams_csv: Path to TEAMS.csv (includes park factors)
            
        Returns:
            Team object with complete roster and park factors loaded
        """
        # Load metadata + park factor data from single CSV
        metadata = TeamLoader.load_team_metadata(teams_csv)[team_abbrev]
        
        # Extract park factors from metadata row
        park_factors = {
            'SL': metadata.get('single_factor', 1.0),
            'DL': metadata.get('double_factor', 1.0),
            'TL': metadata.get('triple_factor', 1.0),
            'HR': metadata.get('homerun_factor', 1.0),
            'GBFB': metadata.get('gbfb_factor', 1.0)
        }
        
        stadium_name = metadata.get('stadium_name', f"{metadata['market']} Stadium")
        
        # Load roster (batters and pitchers in one file)
        try:
            roster_df = pd.read_csv(roster_csv, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                roster_df = pd.read_csv(roster_csv, encoding='latin-1')
            except UnicodeDecodeError:
                roster_df = pd.read_csv(roster_csv, encoding='cp1252')
        
        # Split by position - pitchers have 'P' in position
        batters_df = roster_df[~roster_df['POS'].str.contains('P', na=False)]
        pitchers_df = roster_df[roster_df['POS'].str.contains('P', na=False)]
        
        # Convert DataFrame rows to Player objects
        batters = [
            Player.from_csv_row(row.to_dict(), team_abbrev) 
            for _, row in batters_df.iterrows()
        ]
        
        pitchers = [
            Player.from_csv_row(row.to_dict(), team_abbrev) 
            for _, row in pitchers_df.iterrows()
        ]
        
        # Construct Team object
        return Team(
            name=metadata['team_name'],
            abbreviation=team_abbrev,
            market=metadata.get('market', team_abbrev),
            stadium_name=stadium_name,
            park_factors=park_factors,
            batters=batters,
            pitchers=pitchers,
            wins=metadata.get('wins', 0),
            losses=metadata.get('losses', 0)
        )
    
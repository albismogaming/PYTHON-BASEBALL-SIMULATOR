import pandas as pd
from typing import Dict, List, Tuple
from pathlib import Path
from CONTEXT.TEAM_CONTEXT import Team
from CONTEXT.PLAYER_CONTEXT import Player

class TeamLoader:
    """Static methods for loading teams with rosters and park factors."""
    
    # Global cache for all players (loaded once per session)
    _all_players_cache: Dict[str, Tuple[List[Player], List[Player]]] = {}
    _cache_initialized: bool = False
    
    @staticmethod
    def initialize_player_cache(all_teams_csv: str):
        """
        Load all players from ALL_TEAMS.csv once and cache by team.
        This should be called once at the start of a season simulation.
        
        Args:
            all_teams_csv: Path to ALL_TEAMS.csv with all players
        """
        if TeamLoader._cache_initialized:
            return  # Already loaded
        
        try:
            df = pd.read_csv(all_teams_csv, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(all_teams_csv, encoding='latin-1')
            except UnicodeDecodeError:
                df = pd.read_csv(all_teams_csv, encoding='cp1252')
        
        # Group players by team
        for team_abbrev in df['TM'].unique():
            team_df = df[df['TM'] == team_abbrev]
            
            batters = []
            pitchers = []
            
            for _, row in team_df.iterrows():
                player = Player.from_csv_row(row.to_dict(), team_abbrev)
                
                if player.position == 'SP' or player.position == 'RP':
                    pitchers.append(player)
                else:
                    batters.append(player)
            
            TeamLoader._all_players_cache[team_abbrev] = (batters, pitchers)
        
        TeamLoader._cache_initialized = True
    
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
        }
        
        stadium_name = metadata.get('stadium_name', f"{metadata['market']} Stadium")
        
        # Use cached players if available, otherwise load from individual file
        if TeamLoader._cache_initialized and team_abbrev in TeamLoader._all_players_cache:
            batters, pitchers = TeamLoader._all_players_cache[team_abbrev]
        else:
            # Fallback: Load roster from individual team file
            try:
                roster_df = pd.read_csv(roster_csv, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    roster_df = pd.read_csv(roster_csv, encoding='latin-1')
                except UnicodeDecodeError:
                    roster_df = pd.read_csv(roster_csv, encoding='cp1252')
            
            # Split by position - pitchers have 'SP' or 'RP' in position
            batters_df = roster_df[~roster_df['POS'].str.contains('SP|RP', na=False)]
            pitchers_df = roster_df[roster_df['POS'].str.contains('SP|RP', na=False)]
            
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
    
    @staticmethod
    def load_team_from_cache(team_abbrev: str, teams_csv: str) -> Team:
        """
        Load team using only the player cache (no individual CSV files).
        Requires initialize_player_cache() to have been called first.
        
        Args:
            team_abbrev: Team abbreviation (e.g., "BOS", "NYY")
            teams_csv: Path to TEAM_META.csv for metadata/park factors
            
        Returns:
            Team object with full roster from cache
            
        Raises:
            RuntimeError: If player cache has not been initialized
        """
        if not TeamLoader._cache_initialized:
            raise RuntimeError("Player cache not initialized. Call initialize_player_cache() first.")
        
        if team_abbrev not in TeamLoader._all_players_cache:
            raise KeyError(f"Team {team_abbrev} not found in player cache.")
        
        # Get players from cache
        batters, pitchers = TeamLoader._all_players_cache[team_abbrev]
        
        # Load metadata + park factors
        metadata = TeamLoader.load_team_metadata(teams_csv)[team_abbrev]
        
        park_factors = {
            'SL': metadata.get('single_factor', 1.0),
            'DL': metadata.get('double_factor', 1.0),
            'TL': metadata.get('triple_factor', 1.0),
            'HR': metadata.get('homerun_factor', 1.0),
        }
        
        stadium_name = metadata.get('stadium_name', f"{metadata['market']} Stadium")
        
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
    
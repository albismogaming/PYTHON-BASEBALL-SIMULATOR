from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from CONTEXT.PLAY_CONTEXT import PlayResult
from UTILITIES.ENUMS import Micro, Macro
from UTILITIES.STATS_CALCS import StatsCalculator


class StatsManager:
    """ Static manager for in-game statistics for batters and pitchers. """
    
    # Class-level dictionaries to store all stats
    batter_stats: Dict = {}  # Key: (team_abbrev, player_id), Value: stat dict
    pitcher_stats: Dict = {}  # Key: (team_abbrev, player_id), Value: stat dict
    _key_cache: Dict = {}  # Cache player keys to avoid repeated tuple creation
    
    # ==================== INITIALIZATION ====================
    
    @staticmethod
    def _get_player_key(player):
        """Get hashable key for a player (cached)."""
        player_id = id(player)
        if player_id not in StatsManager._key_cache:
            StatsManager._key_cache[player_id] = (player.team_abbrev, player.player_id)
        return StatsManager._key_cache[player_id]
    
    @staticmethod
    def _initialize_batter(batter):
        """
        Initialize stats for a batter if not already tracked.
        
        Args:
            batter: Player object (batter)
        """
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            StatsManager.batter_stats[key] = {
                'player': batter,
                'PA': 0,      # Plate appearances
                'AB': 0,      # At-bats
                'H': 0,       # Hits
                '1B': 0,      # Singles
                '2B': 0,      # Doubles
                '3B': 0,      # Triples
                'HR': 0,      # Home runs
                'R': 0,       # Runs scored
                'RBI': 0,     # Runs batted in
                'BB': 0,      # Walks
                'SO': 0,      # Strikeouts
                'HBP': 0,     # Hit by pitch
                'TB': 0,      # Total bases
                'SB': 0,      # Stolen bases
                'CS': 0,      # Caught stealing
            }
    
    @staticmethod
    def _initialize_pitcher(pitcher):
        """ Initialize stats for a pitcher if not already tracked. """
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            StatsManager.pitcher_stats[key] = {
                'player': pitcher,
                'IP': 0.0,       # Innings pitched (as outs/3)
                'PT': 0,         # Total pitches thrown
                'H': 0,          # Hits allowed
                'R': 0,          # Runs allowed
                'ER': 0,         # Earned runs
                'BB': 0,         # Walks issued
                'SO': 0,         # Strikeouts
                'HR': 0,         # Home runs allowed
                'BF': 0,         # Batters faced
                'Outs': 0,       # Outs recorded
            }
    
    # ==================== RECORD STATS ====================
    
    @staticmethod
    def record_at_bat(result: PlayResult):
        """ Record a complete at-bat with all relevant stats. """
        StatsManager._initialize_batter(result.batter)
        StatsManager._initialize_pitcher(result.pitcher)
        StatsManager._update_batter_stats(result)
        StatsManager._update_pitcher_stats(result)
    
    @staticmethod
    def _update_batter_stats(result: PlayResult):
        """Update batter statistics based on outcome."""
        key = StatsManager._get_player_key(result.batter)
        stats = StatsManager.batter_stats[key]
        
        # Every outcome is a plate appearance
        stats['PA'] += 1
        
        # Determine if it's an at-bat (excludes BB, HP, sacrifices)
        is_at_bat = result.type not in [Macro.BB, Macro.HP]
        
        if is_at_bat:
            stats['AB'] += 1
        
        if result.type in [Macro.SL, Macro.DL, Macro.TL, Macro.HR, Macro.IH]:
            stats['H'] += 1

        # Hits
        if result.type == Macro.SL or result.type == Macro.IH:
            stats['1B'] += 1
            stats['TB'] += 1
        elif result.type == Macro.DL:
            stats['2B'] += 1
            stats['TB'] += 2
        elif result.type == Macro.TL:
            stats['3B'] += 1
            stats['TB'] += 3
        elif result.type == Macro.HR:
            stats['HR'] += 1
            stats['TB'] += 4
        
        # Other outcomes
        if result.type == Macro.SO:
            stats['SO'] += 1
        elif result.type == Macro.BB:
            stats['BB'] += 1
        elif result.type == Macro.HP:
            stats['HBP'] += 1
        
        # Runs and RBI
        stats['R'] += result.runs
        stats['RBI'] += result.rbis
    
    @staticmethod
    def _update_pitcher_stats(result: PlayResult):
        """Update pitcher statistics based on outcome."""
        key = StatsManager._get_player_key(result.pitcher)
        stats = StatsManager.pitcher_stats[key]
        
        # Every at-bat is a batter faced
        stats['BF'] += 1
        
        # Hits allowed
        if result.type in [Macro.SL, Macro.DL, Macro.TL, Macro.HR, Macro.IH]:
            stats['H'] += 1
        
        # Home runs allowed
        if result.type == Macro.HR:
            stats['HR'] += 1
        
        # Walks
        if result.type == Macro.BB:
            stats['BB'] += 1
        
        # Strikeouts
        if result.type == Macro.SO:
            stats['SO'] += 1
        
        # Outs recorded (can be 0, 1, or 2)
        stats['Outs'] += result.outs
        stats['IP'] = stats['Outs'] / 3.0
    
    @staticmethod
    def record_pitch(pitcher, pitch_count: int = 1):
        """ Record pitches thrown by pitcher. """
        StatsManager._initialize_pitcher(pitcher)
        key = StatsManager._get_player_key(pitcher)
        stats = StatsManager.pitcher_stats[key]
        
        stats['PT'] += pitch_count

    @staticmethod
    def record_run_for_pitcher(pitcher, earned: bool = True):
        """
        Record a run allowed by pitcher.
        
        Args:
            pitcher: Pitcher Player object
            earned: Whether the run is earned (default True)
        """
        StatsManager._initialize_pitcher(pitcher)
        key = StatsManager._get_player_key(pitcher)
        stats = StatsManager.pitcher_stats[key]
        
        stats['R'] += 1
        if earned:
            stats['ER'] += 1
    
    @staticmethod
    def record_steal_attempt(runner, success: bool):
        """
        Record a stolen base attempt.
        
        Args:
            runner: Player object attempting to steal
            success: True if stolen base, False if caught stealing
        """
        StatsManager._initialize_batter(runner)
        key = StatsManager._get_player_key(runner)
        stats = StatsManager.batter_stats[key]
        
        if success:
            stats['SB'] += 1
        else:
            stats['CS'] += 1
    
    # ==================== RETRIEVAL ====================
    
    @staticmethod
    def get_batter_stats(batter) -> Dict:
        """Get all stats for a specific batter."""
        key = StatsManager._get_player_key(batter)
        if key not in StatsManager.batter_stats:
            return {}
        return StatsManager.batter_stats[key].copy()
    
    @staticmethod
    def get_pitcher_stats(pitcher) -> Dict:
        """Get all stats for a specific pitcher."""
        key = StatsManager._get_player_key(pitcher)
        if key not in StatsManager.pitcher_stats:
            return {}
        return StatsManager.pitcher_stats[key].copy()
    
    @staticmethod
    def get_all_batter_stats() -> List[Dict]:
        """Get stats for all batters as a list."""
        return list(StatsManager.batter_stats.values())
    
    @staticmethod
    def get_all_pitcher_stats() -> List[Dict]:
        """Get stats for all pitchers as a list."""
        return list(StatsManager.pitcher_stats.values())
    
    @staticmethod
    def get_team_batting_stats(team_abbrev: str) -> List[Dict]:
        """Get batting stats for all players on a team."""
        return [stats for stats in StatsManager.batter_stats.values() 
                if stats['player'].team_abbrev == team_abbrev]
    
    @staticmethod
    def get_team_pitching_stats(team_abbrev: str) -> List[Dict]:
        """Get pitching stats for all pitchers on a team."""
        return [stats for stats in StatsManager.pitcher_stats.values() 
                if stats['player'].team_abbrev == team_abbrev]
    
    # ==================== FORMATTING ====================
    
    @staticmethod
    def format_batting_stats(team_abbrev: Optional[str] = None) -> str:
        """ Format batting stats as a table. """
        if team_abbrev:
            stats_list = StatsManager.get_team_batting_stats(team_abbrev)
        else:
            stats_list = StatsManager.get_all_batter_stats()
        
        if not stats_list:
            return "No batting stats recorded."
        
        lines = []
        lines.append(f"{'PLAYER':<20} {'POS':<4} {'AB':>3} {'R':>3} {'H':>3} {'2B':>3} {'3B':>3} {'HR':>3} {'RBI':>3} {'BB':>3} {'SO':>3} {'AVG':>5}")
        lines.append("-" * 80)
        
        for stats in sorted(stats_list, key=lambda x: x.get('AB', 0), reverse=True):
            player = stats['player']
            avg = StatsCalculator.get_batting_average(stats)
            
            lines.append(
                f"{player.full_name:<20} {player.position:<4} "
                f"{stats['AB']:>3} {stats['R']:>3} {stats['H']:>3} "
                f"{stats['2B']:>3} {stats['3B']:>3} {stats['HR']:>3} "
                f"{stats['RBI']:>3} {stats['BB']:>3} {stats['SO']:>3} "
                f"{avg:>5.3f}"
            )
        
        return "\n".join(lines)
    
    @staticmethod
    def format_pitching_stats(team_abbrev: Optional[str] = None) -> str:
        """ Format pitching stats as a table. """
        if team_abbrev:
            stats_list = StatsManager.get_team_pitching_stats(team_abbrev)
        else:
            stats_list = StatsManager.get_all_pitcher_stats()
        
        if not stats_list:
            return "No pitching stats recorded."
        
        lines = []
        lines.append(f"{'PLAYER':<20} {'POS':<4} {'IP':>5} {'H':>3} {'R':>3} {'ER':>3} {'BB':>3} {'SO':>3} {'HR':>3} {'Pit':>4} {'ERA':>5}")
        lines.append("-" * 90)
        
        for stats in sorted(stats_list, key=lambda x: x.get('BF', 0), reverse=True):
            player = stats['player']
            ip_str = StatsCalculator.format_innings_pitched(stats)
            era = StatsCalculator.get_era(stats)
            
            lines.append(
                f"{player.full_name:<20} {player.position:<4} "
                f"{ip_str:>5} {stats['H']:>3} {stats['R']:>3} {stats['ER']:>3} "
                f"{stats['BB']:>3} {stats['SO']:>3} {stats['HR']:>3} "
                f"{stats['PT']:>4} {era:>5.2f}"
            )
        
        return "\n".join(lines)
    
    # ==================== RESET ====================
    
    @staticmethod
    def reset():
        """Clear all stats for a new game."""
        StatsManager.batter_stats.clear()
        StatsManager.pitcher_stats.clear()
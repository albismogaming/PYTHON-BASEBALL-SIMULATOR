from typing import Dict


class StatsCalculator:
    """Calculate derived baseball statistics from raw stat dictionaries."""
    
    # ==================== BATTING STATS ====================
    
    @staticmethod
    def get_batting_average(stats: Dict) -> float:
        """
        Calculate batting average (H / AB).
        
        Args:
            stats: Dictionary with 'H' (hits) and 'AB' (at-bats)
        
        Returns:
            Batting average (0.000 to 1.000)
        """
        ab = stats.get('AB', 0)
        if ab == 0:
            return 0.0
        return stats.get('H', 0) / ab
    
    @staticmethod
    def get_on_base_percentage(stats: Dict) -> float:
        """
        Calculate on-base percentage (H + BB + HBP) / (AB + BB + HBP).
        
        Args:
            stats: Dictionary with 'H', 'BB' (walks), 'HBP' (hit by pitch), 'AB'
        
        Returns:
            OBP (0.000 to 1.000+)
        """
        denominator = stats.get('AB', 0) + stats.get('BB', 0) + stats.get('HBP', 0)
        if denominator == 0:
            return 0.0
        numerator = stats.get('H', 0) + stats.get('BB', 0) + stats.get('HBP', 0)
        return numerator / denominator
    
    @staticmethod
    def get_slugging_percentage(stats: Dict) -> float:
        """
        Calculate slugging percentage (TB / AB).
        
        Args:
            stats: Dictionary with 'TB' (total bases) and 'AB' (at-bats)
        
        Returns:
            SLG (0.000 to 4.000+)
        """
        ab = stats.get('AB', 0)
        if ab == 0:
            return 0.0
        return stats.get('TB', 0) / ab
    
    @staticmethod
    def get_ops(stats: Dict) -> float:
        """
        Calculate OPS (On-base Plus Slugging).
        
        Args:
            stats: Dictionary with batting statistics
        
        Returns:
            OPS = OBP + SLG
        """
        return StatsCalculator.get_on_base_percentage(stats) + StatsCalculator.get_slugging_percentage(stats)
    
    @staticmethod
    def get_strikeout_rate(stats: Dict) -> float:
        """
        Calculate strikeout rate (SO / PA).
        
        Args:
            stats: Dictionary with 'SO' (strikeouts) and 'PA' (plate appearances)
        
        Returns:
            K/PA (0.000 to 1.000)
        """
        pa = stats.get('PA', 0)
        if pa == 0:
            return 0.0
        return stats.get('SO', 0) / pa
    
    @staticmethod
    def get_walk_rate(stats: Dict) -> float:
        """
        Calculate walk rate (BB / PA).
        
        Args:
            stats: Dictionary with 'BB' (walks) and 'PA' (plate appearances)
        
        Returns:
            BB/PA (0.000 to 1.000)
        """
        pa = stats.get('PA', 0)
        if pa == 0:
            return 0.0
        return stats.get('BB', 0) / pa
    
    @staticmethod
    def get_home_run_rate(stats: Dict) -> float:
        """
        Calculate home run rate (HR / AB).
        
        Args:
            stats: Dictionary with 'HR' (home runs) and 'AB' (at-bats)
        
        Returns:
            HR/AB (0.000 to 0.300+)
        """
        ab = stats.get('AB', 0)
        if ab == 0:
            return 0.0
        return stats.get('HR', 0) / ab
    
    # ==================== PITCHING STATS ====================
    
    @staticmethod
    def get_era(stats: Dict) -> float:
        """
        Calculate ERA (Earned Run Average).
        Formula: (ER * 9) / IP
        
        Args:
            stats: Dictionary with 'ER' (earned runs) and 'IP' (innings pitched as decimal)
        
        Returns:
            ERA (0.00 to 100.00+)
        """
        ip = stats.get('IP', 0)
        if ip == 0:
            return 0.0
        return (stats.get('ER', 0) * 9) / ip
    
    @staticmethod
    def get_whip(stats: Dict) -> float:
        """
        Calculate WHIP (Walks + Hits per Innings Pitched).
        Formula: (BB + H) / IP
        
        Args:
            stats: Dictionary with 'BB' (walks), 'H' (hits), 'IP' (innings pitched)
        
        Returns:
            WHIP (1.00 to 3.00+)
        """
        ip = stats.get('IP', 0)
        if ip == 0:
            return 0.0
        return (stats.get('BB', 0) + stats.get('H', 0)) / ip
    
    @staticmethod
    def get_strikeout_per_nine(stats: Dict) -> float:
        """
        Calculate strikeouts per 9 innings (K/9).
        Formula: (SO * 9) / IP
        
        Args:
            stats: Dictionary with 'SO' (strikeouts) and 'IP' (innings pitched)
        
        Returns:
            K/9 (0.00 to 15.00+)
        """
        ip = stats.get('IP', 0)
        if ip == 0:
            return 0.0
        return (stats.get('SO', 0) * 9) / ip
    
    @staticmethod
    def get_walk_per_nine(stats: Dict) -> float:
        """
        Calculate walks per 9 innings (BB/9).
        Formula: (BB * 9) / IP
        
        Args:
            stats: Dictionary with 'BB' (walks) and 'IP' (innings pitched)
        
        Returns:
            BB/9 (0.00 to 10.00+)
        """
        ip = stats.get('IP', 0)
        if ip == 0:
            return 0.0
        return (stats.get('BB', 0) * 9) / ip
    
    @staticmethod
    def get_strikeout_walk_ratio(stats: Dict) -> float:
        """
        Calculate strikeout to walk ratio (K/BB).
        
        Args:
            stats: Dictionary with 'SO' (strikeouts) and 'BB' (walks)
        
        Returns:
            K/BB ratio (0.00 to 10.00+)
        """
        bb = stats.get('BB', 0)
        if bb == 0:
            return 0.0
        return stats.get('SO', 0) / bb
    
    @staticmethod
    def format_innings_pitched(stats: Dict) -> str:
        """
        Format innings pitched as string (e.g., "5.2" for 5 2/3 innings).
        
        Args:
            stats: Dictionary with 'Outs' (total outs recorded)
        
        Returns:
            Formatted string like "5.2"
        """
        outs = stats.get('Outs', 0)
        full_innings = outs // 3
        remaining_outs = outs % 3
        return f"{full_innings}.{remaining_outs}"
    
    # ==================== UTILITY FORMATTING ====================
    
    @staticmethod
    def format_stat(value: float, decimals: int = 3) -> str:
        """
        Format a stat value with specified decimal places.
        
        Args:
            value: The numeric value to format
            decimals: Number of decimal places (default 3)
        
        Returns:
            Formatted string
        """
        return f"{value:.{decimals}f}"

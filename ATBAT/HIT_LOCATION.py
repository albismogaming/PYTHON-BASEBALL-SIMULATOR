import random
import numpy as np
from UTILITIES.ENUMS import HitTypes, HitSectors, Outcome


class HitLocationGenerator:
    """
    Stateless class for determining hit depth/location and generating Retrosheet-style location codes.
    Uses triangular distributions with outcome and hit-type specific parameters.
    
    Retrosheet location codes consist of:
    - Ball type prefix: G (Ground), L (Line), F (Fly), P (Pop)
    - Numeric field zone: Position number or combination (e.g., 7, 89, 56)
    - Depth suffix: S (Shallow), M (Medium), D (Deep), XD (Extra Deep), DF (Deep Fly), LDF (Line Drive Fly)
    """
    
    @classmethod
    def determine_fielder(cls, hit_type: HitTypes, hit_sector: HitSectors, hit_depth: str) -> int:
        """
        Determine which fielder makes the play based on hit characteristics.
        
        Args:
            hit_type: HitTypes enum (GB, FB, LD, PU)
            hit_sector: HitSectors enum (LL, LF, LC, CF, RC, RF, RL)
            hit_depth: 'SHALLOW', 'MEDIUM', or 'DEEP'
            
        Returns:
            int: Fielder position number (1-9)
        """
        # POPUPS - mostly infielders, some shallow outfielders
        if hit_type == HitTypes.PU:
            sector_fielders = {
                HitSectors.LL: [5, 6],      # 3B, SS
                HitSectors.LF: [5, 6, 7],   # 3B, SS, LF
                HitSectors.LC: [6, 7],      # SS, LF
                HitSectors.CF: [2, 8],      # C, CF
                HitSectors.RC: [4, 9],      # 2B, RF
                HitSectors.RF: [3, 4, 9],   # 1B, 2B, RF
                HitSectors.RL: [3, 4]       # 1B, 2B
            }
            return np.random.choice(sector_fielders.get(hit_sector, [2, 4, 6]))
        
        # GROUNDBALLS - infielders based on sector
        elif hit_type == HitTypes.GB:
            if hit_depth == 'SHALLOW':
                sector_fielders = {
                    HitSectors.LL: [5],     # 3B
                    HitSectors.LF: [5, 6],  # 3B, SS
                    HitSectors.LC: [6],     # SS
                    HitSectors.CF: [2, 6, 4], # C, SS, 2B
                    HitSectors.RC: [4],     # 2B
                    HitSectors.RF: [3, 4],  # 1B, 2B
                    HitSectors.RL: [3]      # 1B
                }
            else:  # MEDIUM/DEEP - outfielders might field it
                sector_fielders = {
                    HitSectors.LL: [5, 7],  # 3B, LF
                    HitSectors.LF: [6, 7],  # SS, LF
                    HitSectors.LC: [6, 7, 8], # SS, LF, CF
                    HitSectors.CF: [6, 4, 8], # SS, 2B, CF
                    HitSectors.RC: [4, 8, 9], # 2B, CF, RF
                    HitSectors.RF: [4, 9],  # 2B, RF
                    HitSectors.RL: [3, 9]   # 1B, RF
                }
            return np.random.choice(sector_fielders.get(hit_sector, [6]))
        
        # FLYBALLS - outfielders primarily, some infielders on shallow
        elif hit_type == HitTypes.FB:
            if hit_depth == 'SHALLOW':
                sector_fielders = {
                    HitSectors.LL: [5, 7],  # 3B, LF
                    HitSectors.LF: [7],     # LF
                    HitSectors.LC: [7, 8],  # LF, CF
                    HitSectors.CF: [8],     # CF
                    HitSectors.RC: [8, 9],  # CF, RF
                    HitSectors.RF: [9],     # RF
                    HitSectors.RL: [3, 9]   # 1B, RF
                }
            elif hit_depth == 'MEDIUM':
                sector_fielders = {
                    HitSectors.LL: [7],     # LF
                    HitSectors.LF: [7],     # LF
                    HitSectors.LC: [7, 8],  # LF, CF
                    HitSectors.CF: [8],     # CF
                    HitSectors.RC: [8, 9],  # CF, RF
                    HitSectors.RF: [9],     # RF
                    HitSectors.RL: [9]      # RF
                }
            else:  # DEEP
                sector_fielders = {
                    HitSectors.LL: [7],     # LF
                    HitSectors.LF: [7],     # LF
                    HitSectors.LC: [7, 8],  # LF, CF
                    HitSectors.CF: [8],     # CF
                    HitSectors.RC: [8, 9],  # CF, RF
                    HitSectors.RF: [9],     # RF
                    HitSectors.RL: [9]      # RF
                }
            return np.random.choice(sector_fielders.get(hit_sector, [8]))
        
        # LINEDRIVES - mix of infielders and outfielders
        elif hit_type == HitTypes.LD:
            if hit_depth == 'SHALLOW':
                sector_fielders = {
                    HitSectors.LL: [5, 7],  # 3B, LF
                    HitSectors.LF: [5, 6, 7], # 3B, SS, LF
                    HitSectors.LC: [6, 7, 8], # SS, LF, CF
                    HitSectors.CF: [1, 6, 4, 8], # P, SS, 2B, CF
                    HitSectors.RC: [4, 8, 9], # 2B, CF, RF
                    HitSectors.RF: [3, 4, 9], # 1B, 2B, RF
                    HitSectors.RL: [3, 9]   # 1B, RF
                }
            else:  # MEDIUM/DEEP
                sector_fielders = {
                    HitSectors.LL: [7],     # LF
                    HitSectors.LF: [7],     # LF
                    HitSectors.LC: [7, 8],  # LF, CF
                    HitSectors.CF: [8],     # CF
                    HitSectors.RC: [8, 9],  # CF, RF
                    HitSectors.RF: [9],     # RF
                    HitSectors.RL: [9]      # RF
                }
            return np.random.choice(sector_fielders.get(hit_sector, [8]))
        
        # Default to centerfielder if somehow no match
        return 8
        
    @classmethod
    def generate_retrosheet_location(cls, hit_type: HitTypes, hit_sector: HitSectors, 
                                     hit_depth: str, fielder_position: int) -> str:
        """
        Generate a Retrosheet-style location code based on hit characteristics.
        
        Args:
            hit_type: HitTypes enum (GB, FB, LD, PU)
            hit_sector: HitSectors enum (LL, LF, LC, CF, RC, RF, RL)
            hit_depth: 'SHALLOW', 'MEDIUM', or 'DEEP'
            fielder_position: Position number 1-9
            
        Returns:
            str: Retrosheet location code (e.g., '7LDF', 'G56', 'F89XD', 'P4')
        """
        
        # Get field zone code
        zone_code = cls._get_zone_code(hit_sector, hit_depth, fielder_position, hit_type)
        
        # Get depth suffix
        depth_suffix = cls._get_depth_suffix(hit_type, hit_depth, hit_sector)
        
        # Combine: type + zone + depth (e.g., F89D, G56, L7S, P4)
        return f"{zone_code}{depth_suffix}"
    
    
    @classmethod
    def _get_zone_code(cls, hit_sector: HitSectors, hit_depth: str, 
                       fielder_position: int, hit_type: HitTypes) -> str:
        """
        Get the numeric field zone code.
        
        Returns single position (e.g., '7') or combination zones (e.g., '78', '56', '89').
        """
        # For popups and shallow hits, usually single position
        if hit_type == HitTypes.PU or hit_depth == 'SHALLOW':
            return str(fielder_position)
        
        # For deep/medium hits in gaps, use combination codes
        gap_zones = {
            # Left-center gap
            (HitSectors.LC, 'MEDIUM'): ['78', '7', '8'],
            (HitSectors.LC, 'DEEP'): ['78', '7', '8'],
            
            # Right-center gap
            (HitSectors.RC, 'MEDIUM'): ['89', '8', '9'],
            (HitSectors.RC, 'DEEP'): ['89', '8', '9'],
            
            # Left field line
            (HitSectors.LL, 'MEDIUM'): ['7', '5'],
            (HitSectors.LL, 'DEEP'): ['7', '5'],
            
            # Right field line
            (HitSectors.RL, 'MEDIUM'): ['9', '3'],
            (HitSectors.RL, 'DEEP'): ['9', '3'],
            
            # Straight left
            (HitSectors.LF, 'MEDIUM'): ['7'],
            (HitSectors.LF, 'DEEP'): ['7'],
            
            # Straight center
            (HitSectors.CF, 'MEDIUM'): ['8'],
            (HitSectors.CF, 'DEEP'): ['8'],
            
            # Straight right
            (HitSectors.RF, 'MEDIUM'): ['9'],
            (HitSectors.RF, 'DEEP'): ['9'],
        }
        
        key = (hit_sector, hit_depth)
        zone_options = gap_zones.get(key, [str(fielder_position)])
        
        # Randomly select from options to add variety
        return random.choice(zone_options)
    
    @classmethod
    def _get_depth_suffix(cls, hit_type: HitTypes, hit_depth: str, hit_sector: HitSectors) -> str:
        """
        Get the depth suffix for Retrosheet notation.
        
        Returns suffixes like: S, M, D, XD, DF, LDF, etc.
        """
        # Popups rarely have depth suffixes (stay in infield)
        if hit_type == HitTypes.PU:
            return ''
        
        # Ground balls to infield
        if hit_type == HitTypes.GB and hit_depth == 'SHALLOW':
            return ''  # Most infield grounders don't need suffix
        
        # Ground balls to outfield
        if hit_type == HitTypes.GB:
            if hit_depth == 'MEDIUM':
                return 'M' if random.random() < 0.3 else ''
            else:  # DEEP
                return 'D' if random.random() < 0.5 else ''
        
        # Line drives
        if hit_type == HitTypes.LD:
            if hit_depth == 'SHALLOW':
                return 'S' if random.random() < 0.4 else ''
            elif hit_depth == 'MEDIUM':
                return random.choice(['', 'M', 'D']) if random.random() < 0.6 else ''
            else:  # DEEP
                return random.choice(['D', 'LD', 'LDF'])
        
        # Fly balls
        if hit_type == HitTypes.FB:
            if hit_depth == 'SHALLOW':
                return 'S'
            elif hit_depth == 'MEDIUM':
                return random.choice(['', 'M', 'D'])
            else:  # DEEP
                # Extra deep flyballs (potential homers/warning track)
                if random.random() < 0.3:
                    return 'XD'
                else:
                    return random.choice(['D', 'DF'])
        
        return ''

# ============================================================================
# PLAYOFF FORMAT CONFIGURATIONS
# ============================================================================

PLAYOFF_FORMATS = {
    # MLB-style: 6 teams, top 2 get byes, 3 rounds (Bo3 → Bo5 → Bo7)
    'MLB_STYLE': {
        'num_teams': 6,
        'num_byes': 2,
        'rounds': [
            {'name': 'Wild Card Round', 'wins_needed': 2, 'home_field_games': [1, 3]},        # Best-of-3
            {'name': 'Division Series', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},     # Best-of-5
            {'name': 'Championship Series', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}  # Best-of-7
        ]
    },
    
    # Classic: 4 teams, no byes, 2 rounds (Bo5 → Bo7)
    'CLASSIC_4': {
        'num_teams': 4,
        'num_byes': 0,
        'rounds': [
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
    # Single Elimination: 8 teams, 3 rounds (Bo1 → Bo1 → Bo1)
    'SINGLE_ELIM_8': {
        'num_teams': 8,
        'num_byes': 0,
        'rounds': [
            {'name': 'Quarterfinals', 'wins_needed': 1, 'home_field_games': [1]},             # Single game
            {'name': 'Semifinals', 'wins_needed': 1, 'home_field_games': [1]},                # Single game
            {'name': 'Finals', 'wins_needed': 1, 'home_field_games': [1]}                     # Single game
        ]
    },
    
    # March Madness Style: 8 teams, all best-of-5
    'TOURNAMENT_8': {
        'num_teams': 8,
        'num_byes': 0,
        'rounds': [
            {'name': 'Quarterfinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},       # Best-of-5
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
    # Quick Playoffs: 4 teams, all best-of-3
    'QUICK_4': {
        'num_teams': 4,
        'num_byes': 0,
        'rounds': [
            {'name': 'Semifinals', 'wins_needed': 2, 'home_field_games': [1, 3]},             # Best-of-3
            {'name': 'Finals', 'wins_needed': 2, 'home_field_games': [1, 3]}                  # Best-of-3
        ]
    },
    
    # Two-team Championship: Just a finals series
    'CHAMPIONSHIP': {
        'num_teams': 2,
        'num_byes': 0,
        'rounds': [
            {'name': 'Championship Series', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}  # Best-of-7
        ]
    },
    
    # Pool Play + Bracket: 8 teams in 2 pools of 4, top 2 per pool advance
    'POOL_PLAY_8': {
        'type': 'pool_play',
        'num_teams': 8,
        'num_pools': 2,  # Number of pools
        'pool_play': {
            'games_per_matchup': 3,  # Each team plays others in pool three times
            'advance_per_pool': 2     # Top 2 from each pool advance
        },
        'bracket_rounds': [
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
    # Pool Play + Bracket: 12 teams in 3 pools of 4, top 2 per pool + 2 wild cards advance
    'POOL_PLAY_12': {
        'type': 'pool_play',
        'num_teams': 12,
        'num_pools': 3,  # Number of pools
        'pool_play': {
            'games_per_matchup': 2,  # Each team plays others in pool twice
            'advance_per_pool': 2,    # Top 2 from each pool advance automatically
            'wild_cards': 2           # Additional wild card teams (best records among non-qualifiers)
        },
        'bracket_rounds': [
            {'name': 'Quarterfinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},       # Best-of-5
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
    # Pool Play + Bracket: 6 teams in 2 pools of 3, top team per pool + 2 wild cards advance
    'POOL_PLAY_6': {
        'type': 'pool_play',
        'num_teams': 6,
        'num_pools': 2,  # Number of pools
        'pool_play': {
            'games_per_matchup': 3,  # Each team plays others in pool 3 times
            'advance_per_pool': 1,    # Top 1 from each pool advances automatically
            'wild_cards': 2           # Additional wild card teams (2nd place finishers)
        },
        'bracket_rounds': [
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
    # Group Stage + Knockout: 8 teams in 2 groups of 4, top 2 per group advance
    'GROUP_STAGE_8': {
        'type': 'group_stage',
        'num_teams': 8,
        'groups': 2,  # Number of groups
        'group_stage': {
            'games_per_matchup': 2,  # Each team plays others in group twice
            'advance_per_group': 2    # Top 2 from each group advance
        },
        'knockout_rounds': [
            {'name': 'Semifinals', 'wins_needed': 3, 'home_field_games': [1, 2, 5]},          # Best-of-5
            {'name': 'Finals', 'wins_needed': 4, 'home_field_games': [1, 2, 6, 7]}            # Best-of-7
        ]
    },
    
}

# ============================================================================
# ACTIVE PLAYOFF FORMAT
# ============================================================================

# Change this to switch between playoff formats
ACTIVE_FORMAT = 'SWISS_8'

# Load active configuration
_active_config = PLAYOFF_FORMATS[ACTIVE_FORMAT]
ACTIVE_TYPE = _active_config.get('type', 'standard')  # standard, round_robin, ladder, group_stage, swiss, double_elimination

# Standard bracket attributes
NUM_PLAYOFF_TEAMS = _active_config['num_teams']
NUM_BYE_TEAMS = _active_config.get('num_byes', 0)
PLAYOFF_ROUNDS = _active_config.get('rounds', _active_config.get('bracket_rounds', []))
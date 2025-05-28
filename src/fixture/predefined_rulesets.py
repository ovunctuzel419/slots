import numpy as np

from app.ruleset import Ruleset, MatchLeftRule, ScatterRule, FixedConfigurationRule, AllSameRule
from fixture.predefined_slots import BLAZINGFRUITS, MEGAREELS

predefined_rulesets = {}  # noqa

predefined_rulesets[BLAZINGFRUITS.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # Cherry
        MatchLeftRule(symbol_index=0, payout=1, num_matches=2),
        MatchLeftRule(symbol_index=0, payout=4, num_matches=3),
        MatchLeftRule(symbol_index=0, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=0, payout=40, num_matches=5),
        # Lemon
        MatchLeftRule(symbol_index=1, payout=4, num_matches=3),
        MatchLeftRule(symbol_index=1, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=1, payout=40, num_matches=5),
        # Grape
        MatchLeftRule(symbol_index=2, payout=10, num_matches=3),
        MatchLeftRule(symbol_index=2, payout=40, num_matches=4),
        MatchLeftRule(symbol_index=2, payout=100, num_matches=5),
        # Orange
        MatchLeftRule(symbol_index=3, payout=4, num_matches=3),
        MatchLeftRule(symbol_index=3, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=3, payout=40, num_matches=5),
        # Watermelon
        MatchLeftRule(symbol_index=4, payout=10, num_matches=3),
        MatchLeftRule(symbol_index=4, payout=40, num_matches=4),
        MatchLeftRule(symbol_index=4, payout=100, num_matches=5),
        # Plum
        MatchLeftRule(symbol_index=5, payout=4, num_matches=3),
        MatchLeftRule(symbol_index=5, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=5, payout=40, num_matches=5),
        # Star
        ScatterRule(symbol_index=6, payout=2, num_matches=3),
        ScatterRule(symbol_index=6, payout=10, num_matches=4),
        ScatterRule(symbol_index=6, payout=50, num_matches=5),
        # Seven
        MatchLeftRule(symbol_index=7, payout=20, num_matches=3),
        MatchLeftRule(symbol_index=7, payout=200, num_matches=4),
        MatchLeftRule(symbol_index=7, payout=1000, num_matches=5),
    ]
)

predefined_rulesets[MEGAREELS.name] = Ruleset(
    lines=[[1, 1, 1],
           [0, 0, 0],
           [2, 2, 2],
           [0, 1, 2],
           [2, 1, 0]],
    rules=[
        # Special rules
        AllSameRule(symbol_index=1, payout=80),  # All lemon
        AllSameRule(symbol_index=2, payout=80),  # All Orange
        AllSameRule(symbol_index=3, payout=80),  # All Grape
        AllSameRule(symbol_index=4, payout=80),  # All Plum
        # Cherry
        MatchLeftRule(symbol_index=0, payout=1, num_matches=3),
        # Lemon
        MatchLeftRule(symbol_index=1, payout=8, num_matches=3),
        # Grape
        MatchLeftRule(symbol_index=2, payout=8, num_matches=3),
        # Orange
        MatchLeftRule(symbol_index=3, payout=8, num_matches=3),
        # Plum
        MatchLeftRule(symbol_index=4, payout=8, num_matches=3),
        # Bar
        MatchLeftRule(symbol_index=5, payout=12, num_matches=3),
        # Star
        MatchLeftRule(symbol_index=6, payout=40, num_matches=3),
        # Seven
        MatchLeftRule(symbol_index=7, payout=150, num_matches=3)
    ]
)

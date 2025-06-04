import numpy as np

from app.ruleset import Ruleset, MatchLeftRule, ScatterRule, FixedConfigurationRule, AllSameRule, \
    MatchAnyPositionWithWildBonusRule, MatchLeftOrRightWithWildColumnRule, ExistsInEveryReelRule
from fixture.predefined_slots import BLAZINGFRUITS, MEGAREELS, BELLS, MUMMY, MAJESTIC, FRUIT, CRYSTALTREASURE, \
    REELSDELUXE, ICEDFRUITS, REELS, GANGSTER, DRAGON, VULCAN, DISCO

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

predefined_rulesets[BELLS.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # Cherry
        MatchLeftRule(symbol_index=0, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=16, num_matches=5, wild_symbol=9),
        # Plum
        MatchLeftRule(symbol_index=1, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=5, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=24, num_matches=5, wild_symbol=9),
        # Lemon
        MatchLeftRule(symbol_index=2, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=16, num_matches=5, wild_symbol=9),
        # Orange
        MatchLeftRule(symbol_index=3, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=16, num_matches=5, wild_symbol=9),
        # Watermelon
        MatchLeftRule(symbol_index=4, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=200, num_matches=5, wild_symbol=9),
        # Grape
        MatchLeftRule(symbol_index=5, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=5, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=24, num_matches=5, wild_symbol=9),
        # SingleBar
        MatchLeftRule(symbol_index=6, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=200, num_matches=5, wild_symbol=9),
        # DoubleBar
        MatchLeftRule(symbol_index=7, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=30, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=300, num_matches=5, wild_symbol=9),
        # TripleBar
        MatchLeftRule(symbol_index=8, payout=2, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=20, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=200, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=1000, num_matches=5, wild_symbol=9),
        # Bell Scattergame - 10 free spins
        ScatterRule(symbol_index=9, payout=2, free_games_bonus=10, num_matches=3),
        ScatterRule(symbol_index=9, payout=20, free_games_bonus=10, num_matches=4),
        ScatterRule(symbol_index=9, payout=200, free_games_bonus=10, num_matches=5)
    ]
)

predefined_rulesets[MUMMY.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # 10
        MatchLeftRule(symbol_index=0, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=16, num_matches=5, wild_symbol=9),
        # J
        MatchLeftRule(symbol_index=1, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=16, num_matches=5, wild_symbol=9),
        # Q
        MatchLeftRule(symbol_index=2, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=16, num_matches=5, wild_symbol=9),
        # K
        MatchLeftRule(symbol_index=3, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=5, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=24, num_matches=5, wild_symbol=9),
        # A
        MatchLeftRule(symbol_index=4, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=5, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=24, num_matches=5, wild_symbol=9),
        # SphinxFace
        MatchLeftRule(symbol_index=5, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=30, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=300, num_matches=5, wild_symbol=9),
        # SphinxBody
        MatchLeftRule(symbol_index=6, payout=2, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=20, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=200, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=1000, num_matches=5, wild_symbol=9),
        # Tomb
        MatchLeftRule(symbol_index=7, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=200, num_matches=5, wild_symbol=9),
        # Scarab
        MatchLeftRule(symbol_index=8, payout=1, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=200, num_matches=5, wild_symbol=9),
        # Mummy Scattergame - 10 free spins
        ScatterRule(symbol_index=9, payout=2, free_games_bonus=10, num_matches=3),
        ScatterRule(symbol_index=9, payout=20, free_games_bonus=10, num_matches=4),
        ScatterRule(symbol_index=9, payout=200, free_games_bonus=10, num_matches=5)
    ]
)

predefined_rulesets[MAJESTIC.name] = Ruleset(
    lines=[[1, 1, 1],
           [0, 0, 0,],
           [2, 2, 2,],
           [0, 1, 2,],
           [2, 1, 0,]],
    rules=[
        # Stars
        MatchLeftRule(symbol_index=0, payout=8, num_matches=3),
        # SingleBar
        MatchLeftRule(symbol_index=1, payout=16, num_matches=3),
        # DoubleBar
        MatchLeftRule(symbol_index=2, payout=20, num_matches=3),
        # TripleBar
        MatchLeftRule(symbol_index=3, payout=40, num_matches=3),
        # Orange
        MatchLeftRule(symbol_index=4, payout=8, num_matches=3),
        # Lemon
        MatchLeftRule(symbol_index=5, payout=8, num_matches=3),
        # Cherry
        MatchLeftRule(symbol_index=6, payout=8, num_matches=3),
        # Sevens
        MatchLeftRule(symbol_index=7, payout=60, num_matches=3),
        # Bell
        MatchLeftRule(symbol_index=8, payout=16, num_matches=3),
    ]
)


predefined_rulesets[FRUIT.name] = Ruleset(  # Blazing Hot7
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2],

           [1, 2, 2, 2, 1],
           [1, 0, 0, 0, 1],
           [2, 2, 1, 0, 0],
           [0, 0, 1, 2, 2],
           [2, 1, 1, 1, 0],

           [0, 1, 1, 1, 2],
           [0, 0, 1, 0, 0],
           [2, 2, 1, 2, 2],
           [1, 0, 1, 2, 1],
           [1, 2, 1, 0, 1],

           [0, 1, 0, 1, 0],
           [2, 1, 2, 1, 2],
           [1, 1, 0, 1, 1],
           [1, 1, 2, 1, 1],
           [0, 1, 1, 1, 0]],
    rules=[
        # Cherry
        MatchLeftRule(symbol_index=0, payout=0.25, num_matches=2),
        MatchLeftRule(symbol_index=0, payout=1.25, num_matches=3),
        MatchLeftRule(symbol_index=0, payout=2.5, num_matches=4),
        MatchLeftRule(symbol_index=0, payout=9, num_matches=5),
        # Grape
        MatchLeftRule(symbol_index=1, payout=2.5, num_matches=3),
        MatchLeftRule(symbol_index=1, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=1, payout=25, num_matches=5),
        # Watermelon
        MatchLeftRule(symbol_index=2, payout=2.5, num_matches=3),
        MatchLeftRule(symbol_index=2, payout=10, num_matches=4),
        MatchLeftRule(symbol_index=2, payout=25, num_matches=5),
        # Lemon
        MatchLeftRule(symbol_index=3, payout=1.25, num_matches=3),
        MatchLeftRule(symbol_index=3, payout=2.5, num_matches=4),
        MatchLeftRule(symbol_index=3, payout=9, num_matches=5),
        # Orange
        MatchLeftRule(symbol_index=4, payout=1.25, num_matches=3),
        MatchLeftRule(symbol_index=4, payout=2.5, num_matches=4),
        MatchLeftRule(symbol_index=4, payout=9, num_matches=5),
        # Plum
        MatchLeftRule(symbol_index=5, payout=1.25, num_matches=3),
        MatchLeftRule(symbol_index=5, payout=2.5, num_matches=4),
        MatchLeftRule(symbol_index=5, payout=9, num_matches=5),
        # Star
        MatchLeftRule(symbol_index=6, payout=5, num_matches=3),
        MatchLeftRule(symbol_index=6, payout=20, num_matches=4),
        MatchLeftRule(symbol_index=6, payout=50, num_matches=5),
        # Seven
        MatchLeftRule(symbol_index=7, payout=5, num_matches=3),
        MatchLeftRule(symbol_index=7, payout=50, num_matches=4),
        MatchLeftRule(symbol_index=7, payout=250, num_matches=5),
    ]
)


predefined_rulesets[CRYSTALTREASURE.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # Key
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=4, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=20, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=100, num_matches=5, wild_symbol=7),
        # Amethyst
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=1, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=5, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=20, num_matches=5, wild_symbol=7),
        # Ruby
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=2, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=10, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=40, num_matches=5, wild_symbol=7),
        # Sapphire
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=2, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=10, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=40, num_matches=5, wild_symbol=7),
        # Emerald
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=1, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=5, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=20, num_matches=5, wild_symbol=7),
        # Crown
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=10, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=100, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=500, num_matches=5, wild_symbol=7),
        # GoldBar
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=4, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=20, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=100, num_matches=5, wild_symbol=7),
    ]
)

predefined_rulesets[REELS.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # Cherry
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=1, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=5, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=20, num_matches=5, wild_symbol=7),
        # Grape
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=4, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=20, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=100, num_matches=5, wild_symbol=7),
        # Watermelon
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=4, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=20, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=100, num_matches=5, wild_symbol=7),
        # Lemon
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=1, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=5, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=20, num_matches=5, wild_symbol=7),
        # Orange
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=2, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=10, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=40, num_matches=5, wild_symbol=7),
        # Plum
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=2, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=10, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=40, num_matches=5, wild_symbol=7),
        # Seven
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=10, num_matches=3, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=100, num_matches=4, wild_symbol=7),
        MatchAnyPositionWithWildBonusRule(symbol_index=6, payout=500, num_matches=5, wild_symbol=7),
    ]
)

predefined_rulesets[REELSDELUXE.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2]],
    rules=[
        # Cherry
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=1, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=5, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=0, payout=20, num_matches=5, wild_symbol=6),
        # Lemon
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=1, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=5, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=1, payout=20, num_matches=5, wild_symbol=6),
        # Grape
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=4, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=20, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=2, payout=100, num_matches=5, wild_symbol=6),
        # Orange
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=2, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=10, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=3, payout=40, num_matches=5, wild_symbol=6),
        # Watermelon
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=4, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=20, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=4, payout=100, num_matches=5, wild_symbol=6),
        # Plum
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=2, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=10, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=5, payout=40, num_matches=5, wild_symbol=6),
        # Seven
        MatchAnyPositionWithWildBonusRule(symbol_index=7, payout=10, num_matches=3, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=7, payout=100, num_matches=4, wild_symbol=6),
        MatchAnyPositionWithWildBonusRule(symbol_index=7, payout=500, num_matches=5, wild_symbol=6),
    ]
)

predefined_rulesets[ICEDFRUITS.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2],
           [0, 0, 1, 0, 0],
           [2, 2, 1, 2, 2],
           [1, 0, 0, 0, 1],
           [1, 2, 2, 2, 1],
           [1, 1, 0, 1, 1]],
    rules=[
        # Cherry
        MatchLeftOrRightWithWildColumnRule(symbol_index=0, payout=1, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=0, payout=2, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=0, payout=10, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Lemon
        MatchLeftOrRightWithWildColumnRule(symbol_index=1, payout=1, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=1, payout=2, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=1, payout=10, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Watermelon
        MatchLeftOrRightWithWildColumnRule(symbol_index=2, payout=2, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=2, payout=5, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=2, payout=20, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Orange
        MatchLeftOrRightWithWildColumnRule(symbol_index=3, payout=1, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=3, payout=3, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=3, payout=15, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Plum
        MatchLeftOrRightWithWildColumnRule(symbol_index=4, payout=1, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=4, payout=3, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=4, payout=15, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Grape
        MatchLeftOrRightWithWildColumnRule(symbol_index=5, payout=2, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=5, payout=5, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=5, payout=20, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Bell
        MatchLeftOrRightWithWildColumnRule(symbol_index=6, payout=5, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=6, payout=20, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=6, payout=50, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Seven
        MatchLeftOrRightWithWildColumnRule(symbol_index=7, payout=10, num_matches=3, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=7, payout=50, num_matches=4, wild_symbol=8, special_wild_symbol=9),
        MatchLeftOrRightWithWildColumnRule(symbol_index=7, payout=100, num_matches=5, wild_symbol=8, special_wild_symbol=9),
        # Wild free Game with at least one symbol
        ScatterRule(symbol_index=8, payout=0, free_games_bonus=1, num_matches=1),
    ]
)

predefined_rulesets[GANGSTER.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2],
           [1, 2, 2, 2, 1],
           [1, 0, 0, 0, 1],
           [2, 2, 1, 0, 0],
           [0, 0, 1, 2, 2],
           [2, 1, 1, 1, 0],
           [0, 1, 1, 1, 2],
           [0, 0, 2, 0, 0],
           [2, 2, 0, 2, 2],
           [1, 0, 1, 2, 1],
           [1, 2, 1, 0, 1],
           [0, 1, 0, 1, 0],
           [2, 1, 2, 1, 2],
           [1, 1, 0, 1, 1],
           [1, 1, 2, 1, 1],
           [0, 2, 1, 2, 0],
           [0, 2, 2, 2, 0],
           [1, 0, 2, 0, 1],
           [0, 2, 0, 2, 0],
           [1, 2, 0, 2, 1],
           [2, 0, 0, 0, 2],
           [2, 0, 1, 0, 2],
           [2, 0, 2, 0, 2]],
    rules=[
        # Dynamite
        MatchLeftRule(symbol_index=0, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=0, payout=1, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=0, payout=6, num_matches=5, wild_symbol=11),
        # Hat
        MatchLeftRule(symbol_index=1, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=1, payout=0.8, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=1, payout=4, num_matches=5, wild_symbol=11),
        # Money
        MatchLeftRule(symbol_index=2, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=2, payout=1, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=2, payout=6, num_matches=5, wild_symbol=11),
        # Kegs
        MatchLeftRule(symbol_index=3, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=3, payout=0.8, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=3, payout=4, num_matches=5, wild_symbol=11),
        # Car
        MatchLeftRule(symbol_index=4, payout=0.8, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=4, payout=4, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=4, payout=20, num_matches=5, wild_symbol=11),
        # TommyGun
        MatchLeftRule(symbol_index=5, payout=0.6, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=5, payout=2, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=5, payout=10, num_matches=5, wild_symbol=11),
        # Safe
        MatchLeftRule(symbol_index=6, payout=0.2, num_matches=2, wild_symbol=11),
        MatchLeftRule(symbol_index=6, payout=1, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=6, payout=4, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=6, payout=40, num_matches=5, wild_symbol=11),
        # Whiskey
        MatchLeftRule(symbol_index=7, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=7, payout=0.8, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=7, payout=4, num_matches=5, wild_symbol=11),
        # Ammo
        MatchLeftRule(symbol_index=8, payout=0.2, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=8, payout=0.8, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=8, payout=4, num_matches=5, wild_symbol=11),
        # Pistol
        MatchLeftRule(symbol_index=9, payout=0.2, free_games_bonus=0, multiplier_2x_bonus=0, num_matches=2, wild_symbol=11),
        MatchLeftRule(symbol_index=9, payout=0.4, free_games_bonus=8, multiplier_2x_bonus=8, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=9, payout=0.8, free_games_bonus=10, multiplier_2x_bonus=10, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=9, payout=2, free_games_bonus=15, multiplier_2x_bonus=15, num_matches=5, wild_symbol=11),
        # Moneybag
        MatchLeftRule(symbol_index=10, payout=0.6, num_matches=3, wild_symbol=11),
        MatchLeftRule(symbol_index=10, payout=2, num_matches=4, wild_symbol=11),
        MatchLeftRule(symbol_index=10, payout=10, num_matches=5, wild_symbol=11),
    ]
)


predefined_rulesets[DRAGON.name] = Ruleset(
    lines=[[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 2, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 0, 0, 1, 0],
           [0, 1, 0, 0, 0],
           [0, 0, 1, 1, 0],
           [0, 1, 1, 0, 0],
           [0, 0, 2, 0, 0],
           [0, 0, 2, 1, 0],
           [0, 1, 2, 0, 0],
           [1, 1, 1, 1, 1],
           [1, 1, 2, 1, 1],
           [1, 1, 0, 1, 1],
           [1, 2, 2, 2, 1],
           [1, 0, 0, 0, 1],
           [1, 2, 1, 2, 1],
           [1, 0, 1, 0, 1],
           [1, 1, 1, 2, 1],
           [1, 1, 1, 0, 1],
           [1, 2, 1, 1, 1],
           [1, 0, 1, 1, 1],
           [1, 2, 0, 2, 1],
           [1, 0, 2, 0, 1],
           [2, 2, 2, 2, 2],
           [2, 2, 3, 2, 2],
           [2, 2, 1, 2, 2],
           [2, 3, 3, 3, 2],
           [2, 1, 1, 1, 2],
           [2, 3, 2, 3, 2],
           [2, 1, 2, 1, 2],
           [2, 2, 2, 3, 2],
           [2, 2, 2, 1, 2],
           [2, 3, 2, 2, 2],
           [2, 1, 2, 2, 2],
           [2, 3, 1, 3, 2],
           [2, 1, 3, 1, 2],
           [3, 3, 3, 3, 3],
           [3, 3, 2, 3, 3],
           [3, 2, 2, 2, 3],
           [3, 2, 1, 2, 3],
           [3, 2, 3, 2, 3],
           [3, 3, 3, 2, 3],
           [3, 2, 3, 3, 3],
           [3, 3, 2, 2, 3],
           [3, 2, 2, 3, 3],
           [3, 3, 1, 3, 3],
           [3, 3, 1, 2, 3],
           [3, 2, 1, 3, 3]],
    rules=[
        # 9
        MatchLeftRule(symbol_index=0, payout=0.2, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=0, payout=0.4, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=0, payout=4, num_matches=5, wild_symbol=8),
        # 10
        MatchLeftRule(symbol_index=1, payout=0.2, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=1, payout=0.4, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=1, payout=4, num_matches=5, wild_symbol=8),
        # J
        MatchLeftRule(symbol_index=2, payout=0.2, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=2, payout=0.6, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=2, payout=4, num_matches=5, wild_symbol=8),
        # Q
        MatchLeftRule(symbol_index=3, payout=0.2, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=3, payout=0.6, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=3, payout=4, num_matches=5, wild_symbol=8),
        # K
        MatchLeftRule(symbol_index=4, payout=0.4, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=4, payout=1, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=4, payout=8, num_matches=5, wild_symbol=8),
        # A
        MatchLeftRule(symbol_index=5, payout=0.4, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=5, payout=1, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=5, payout=8, num_matches=5, wild_symbol=8),
        # Coin
        MatchLeftRule(symbol_index=6, payout=0.8, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=6, payout=2, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=6, payout=8, num_matches=5, wild_symbol=8),
        # Tiger
        MatchLeftRule(symbol_index=7, payout=0.4, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=7, payout=2, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=7, payout=8, num_matches=5, wild_symbol=8),
        # YinYang
        ScatterRule(symbol_index=9, payout=10, num_matches=3, free_games_bonus=10),
        # House
        MatchLeftRule(symbol_index=10, payout=0.2, num_matches=2, wild_symbol=8),
        MatchLeftRule(symbol_index=10, payout=0.8, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=10, payout=3, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=10, payout=10, num_matches=5, wild_symbol=8),
        # Fan
        MatchLeftRule(symbol_index=11, payout=0.2, num_matches=2, wild_symbol=8),
        MatchLeftRule(symbol_index=11, payout=0.8, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=11, payout=3, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=11, payout=10, num_matches=5, wild_symbol=8),
        # Dragon
        MatchLeftRule(symbol_index=12, payout=0.2, num_matches=2, wild_symbol=8),
        MatchLeftRule(symbol_index=12, payout=0.8, num_matches=3, wild_symbol=8),
        MatchLeftRule(symbol_index=12, payout=4, num_matches=4, wild_symbol=8),
        MatchLeftRule(symbol_index=12, payout=20, num_matches=5, wild_symbol=8),
    ]
)


predefined_rulesets[VULCAN.name] = Ruleset(
    lines=[[1, 1, 1, 1, 1],
           [0, 0, 0, 0, 0],
           [2, 2, 2, 2, 2],
           [0, 1, 2, 1, 0],
           [2, 1, 0, 1, 2],
           [1, 2, 2, 2, 1],
           [1, 0, 0, 0, 1],
           [2, 2, 1, 0, 0],
           [0, 0, 1, 2, 2],
           [2, 1, 1, 1, 0],
           [0, 1, 1, 1, 2],
           [0, 0, 2, 0, 0],
           [2, 2, 0, 2, 2],
           [1, 0, 1, 2, 1],
           [1, 2, 1, 0, 1],
           [0, 1, 0, 1, 0],
           [2, 1, 2, 1, 2],
           [1, 1, 0, 1, 1],
           [1, 1, 2, 1, 1],
           [0, 2, 1, 2, 0],
           [0, 2, 2, 2, 0],
           [1, 0, 2, 0, 1],
           [0, 2, 0, 2, 0],
           [1, 2, 0, 2, 1],
           [2, 0, 0, 0, 2],
           [2, 0, 1, 0, 2],
           [2, 0, 2, 0, 2]],
    rules=[
        # J
        MatchLeftRule(symbol_index=0, payout=0.2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=0, payout=0.8, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=0, payout=2, num_matches=5, wild_symbol=12),
        # Q
        MatchLeftRule(symbol_index=1, payout=0.2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=1, payout=0.8, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=1, payout=2, num_matches=5, wild_symbol=12),
        # K
        MatchLeftRule(symbol_index=2, payout=0.2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=2, payout=0.8, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=2, payout=2, num_matches=5, wild_symbol=12),
        # A
        MatchLeftRule(symbol_index=3, payout=0.2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=3, payout=0.8, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=3, payout=2, num_matches=5, wild_symbol=12),
        # TreasureMap
        ScatterRule(symbol_index=4, payout=0, free_games_bonus=10, num_matches=3),
        ScatterRule(symbol_index=4, payout=0, free_games_bonus=20, num_matches=4),
        ScatterRule(symbol_index=4, payout=0, free_games_bonus=40, num_matches=5),
        # Coconut
        MatchLeftRule(symbol_index=5, payout=0.4, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=5, payout=1.6, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=5, payout=4, num_matches=5, wild_symbol=12),
        # Pineapple
        MatchLeftRule(symbol_index=6, payout=0.8, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=6, payout=2, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=6, payout=5, num_matches=5, wild_symbol=12),
        # GoldenIdol
        MatchLeftRule(symbol_index=7, payout=2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=7, payout=6, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=7, payout=20, num_matches=5, wild_symbol=12),
        # StoneIdol
        MatchLeftRule(symbol_index=8, payout=1.6, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=8, payout=4, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=8, payout=12, num_matches=5, wild_symbol=12),
        # GreenIdol
        MatchLeftRule(symbol_index=9, payout=1.2, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=9, payout=3, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=9, payout=8, num_matches=5, wild_symbol=12),
        # Volcano
        ScatterRule(symbol_index=10, payout=0, mystery_multiplier_count=1, num_matches=1),
        # PalmTree
        MatchLeftRule(symbol_index=11, payout=0.8, num_matches=3, wild_symbol=12),
        MatchLeftRule(symbol_index=11, payout=2, num_matches=4, wild_symbol=12),
        MatchLeftRule(symbol_index=11, payout=5, num_matches=5, wild_symbol=12),
        # Wild
        MatchLeftRule(symbol_index=12, payout=0.2, num_matches=3),
        MatchLeftRule(symbol_index=12, payout=0.6, num_matches=4),
        MatchLeftRule(symbol_index=12, payout=2, num_matches=5),
    ]
)


predefined_rulesets[DISCO.name] = Ruleset(
    lines=[[0, 3, 2, 3, 0],
           [0, 3, 0, 3, 0],
           [1, 1, 1, 1, 1],
           [1, 1, 0, 1, 1],
           [1, 1, 2, 1, 1],
           [1, 1, 3, 1, 1],
           [1, 0, 0, 0, 1],
           [1, 2, 2, 2, 1],
           [1, 2, 3, 2, 1],
           [1, 3, 3, 3, 1],
           [1, 0, 1, 0, 1],
           [1, 2, 1, 2, 1],
           [1, 3, 1, 3, 1],
           [1, 3, 2, 3, 1],
           [1, 0, 1, 2, 1],
           [2, 2, 2, 2, 2],
           [2, 2, 3, 2, 2],
           [2, 2, 1, 2, 2],
           [2, 2, 0, 2, 2],
           [2, 3, 3, 3, 2],
           [0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 2, 0, 0],
           [0, 0, 3, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 2, 1, 0],
           [0, 2, 2, 2, 0],
           [0, 3, 3, 3, 0],
           [0, 1, 0, 1, 0],
           [0, 2, 1, 2, 0],
           [3, 3, 1, 3, 3],
           [3, 3, 0, 3, 3],
           [3, 2, 2, 2, 3],
           [3, 2, 1, 2, 3],
           [3, 1, 1, 1, 3],
           [3, 0, 0, 0, 3],
           [3, 2, 3, 2, 3],
           [3, 1, 3, 1, 3],
           [3, 0, 1, 0, 3],
           [3, 0, 3, 0, 3],
           [2, 1, 1, 1, 2],
           [2, 1, 0, 1, 2],
           [2, 0, 0, 0, 2],
           [2, 3, 2, 3, 2],
           [2, 1, 2, 1, 2],
           [2, 0, 2, 0, 2],
           [2, 0, 1, 0, 2],
           [2, 3, 2, 1, 2],
           [3, 3, 3, 3, 3],
           [3, 3, 2, 3, 3]],
    rules=[
        # 9
        MatchLeftRule(symbol_index=0, payout=0.2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=0.8, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=0, payout=4, num_matches=5, wild_symbol=9),
        # 10
        MatchLeftRule(symbol_index=1, payout=0.2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=1, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=1, payout=4, num_matches=5, wild_symbol=9),
        # J
        MatchLeftRule(symbol_index=2, payout=0.2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=1, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=2, payout=4, num_matches=5, wild_symbol=9),
        # Q
        MatchLeftRule(symbol_index=3, payout=0.2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=1, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=3, payout=4, num_matches=5, wild_symbol=9),
        # K
        MatchLeftRule(symbol_index=4, payout=0.2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=1, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=4, payout=4, num_matches=5, wild_symbol=9),
        # Clef
        MatchLeftRule(symbol_index=5, payout=0.6, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=3, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=5, payout=10, num_matches=5, wild_symbol=9),
        # DancerSingle
        MatchLeftRule(symbol_index=6, payout=1, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=4, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=6, payout=20, num_matches=5, wild_symbol=9),
        # DancerMultiple
        MatchLeftRule(symbol_index=7, payout=2, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=10, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=7, payout=30, num_matches=5, wild_symbol=9),
        # Equalizer
        MatchLeftRule(symbol_index=8, payout=0.4, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=1.6, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=8, payout=6, num_matches=5, wild_symbol=9),
        # Vinyl
        MatchLeftRule(symbol_index=9, payout=0.2, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=9, payout=4, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=9, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=9, payout=40, num_matches=5, wild_symbol=9),
        # Vinyl letters on a line trigger special bonus where these letters (non-vinyl) become wild for 5 games
        ExistsInEveryReelRule(symbol_index=-1, symbol_indices=[10, 11, 12], payout=0, free_games_bonus=5),
        # Halo (Hot Fun)
        MatchLeftRule(symbol_index=13, payout=0.2, num_matches=2, wild_symbol=9),
        MatchLeftRule(symbol_index=13, payout=4, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=13, payout=20, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=13, payout=40, num_matches=5, wild_symbol=9),
        # Disco Ball
        ScatterRule(symbol_index=14, payout=4, num_matches=3),
        ScatterRule(symbol_index=14, payout=40, num_matches=4),
        ScatterRule(symbol_index=14, payout=200, num_matches=5),
        # DJ (Turntable)
        MatchLeftRule(symbol_index=15, payout=0.4, num_matches=3, wild_symbol=9),
        MatchLeftRule(symbol_index=15, payout=2, num_matches=4, wild_symbol=9),
        MatchLeftRule(symbol_index=15, payout=8, num_matches=5, wild_symbol=9),
    ]
)

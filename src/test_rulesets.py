import unittest

import numpy as np

from fixture.predefined_rulesets import predefined_rulesets
from fixture.predefined_slots import MEGAREELS, MUMMY, MAJESTIC, BLAZINGHOT7, CRYSTALTREASURE, ICEDFRUITS, GANGSTER, \
    DRAGON, VULCAN, DISCO, BELLS


class TestMegaReels(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[MEGAREELS.name]
        self.bet = 100

    def test_all_same(self):
        icon_set = np.array([[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(8000, payout)

    def test_star_diagonal(self):
        icon_set = np.array([[6, 1, 2],
                             [4, 6, 3],
                             [2, 7, 6]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(4000, payout)

    def test_three_lines(self):
        icon_set = np.array([[5, 1, 5],
                             [5, 5, 5],
                             [5, 7, 5]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(3600, payout)

    def test_three_lines_different(self):
        icon_set = np.array([[5, 5, 5],
                             [5, 5, 5],
                             [0, 0, 0]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(2500, payout)


class TestMummy(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[MUMMY.name]
        self.bet = 50

    def test_triple_reward(self):
        icon_set = np.array([[5, 6, 0, 1, 1],
                             [0, 0, 9, 9, 3],
                             [9, 3, 4, 3, 2]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(500, payout)


class TestMajestic(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[MAJESTIC.name]
        self.bet = 50

    def test_cherry_row(self):
        icon_set = np.array([[8, 6, 5],
                             [8, 6, 5],
                             [6, 6, 6]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(400, payout)

    def test_many_oranges(self):
        icon_set = np.array([[4, 4, 3],
                             [4, 4, 4],
                             [4, 4, 4]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(1200, payout)


class TestBlazingHot7(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[BLAZINGHOT7.name]
        self.bet = 100

    def test_many_cherries(self):
        icon_set = np.array([[0, 0, 1, 3, 6],
                             [0, 0, 1, 3, 1],
                             [0, 0, 1, 3, 1]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(500, payout)

    def test_many_oranges(self):
        icon_set = np.array([[4, 4, 1, 0, 0],
                             [4, 4, 4, 2, 1],
                             [1, 1, 4, 2, 1]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(1000, payout)


class TestCrystalTreasure(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[CRYSTALTREASURE.name]
        self.bet = 100

    def test_sapphires(self):
        icon_set = np.array([[3, 4, 6, 3, 3],
                             [3, 6, 3, 3, 3],
                             [2, 6, 3, 3, 3]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(600, payout)

    def test_sapphires_even_more(self):
        icon_set = np.array([[4, 3, 3, 6, 3],
                             [4, 3, 3, 3, 3],
                             [4, 3, 3, 3, 1]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(2400, payout)

    def test_3x_multiplier(self):
        icon_set = np.array([[1, 6, 4, 9, 3],
                             [6, 5, 1, 9, 1],
                             [6, 5, 7, 9, 1]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(300, payout)  # 100 x 3 since 9 is 3x multiplier


class TestIcedFruits(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[ICEDFRUITS.name]
        self.bet = 50

    def test_many_plums(self):
        icon_set = np.array([[4, 4, 6, 2, 3],
                             [4, 4, 6, 0, 3],
                             [4, 4, 4, 0, 2]])

        payout = self.ruleset.calculate_payout(icon_set).payout * self.bet
        self.assertEqual(150, payout)

    def test_many_plums(self):
        icon_set = np.array([[0, 0, 6, 4, 1],
                             [0, 0, 4, 4, 1],
                             [4, 5, 4, 8, 7]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(0, payout.payout * self.bet)
        self.assertEqual(1, payout.free_games)

    def test_column_replacement(self):
        icon_set = np.array([[4, 2, 1, 6, 6],
                             [4, 2, 1, 6, 6],
                             [4, 8, 8, 4, 1]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(6500, payout.payout * self.bet)
        self.assertEqual(1, payout.free_games)

    def test_column_replacement_2(self):
        icon_set = np.array([[0, 5, 2, 0, 2],
                             [3, 5, 2, 0, 0],
                             [3, 5, 0, 4, 0]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(0, payout.payout * self.bet)

        icon_set[0, 3] = 9  # Replaced with a 'special wild'
        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(300, payout.payout * self.bet)


class TestGangster(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[GANGSTER.name]
        self.bet = 100

    def test_many_lines_match(self):
        icon_set = np.array([[6, 11, 7, 3, 7],
                             [7, 2, 7, 8, 3],
                             [5, 7, 7, 5, 4]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(180, payout)

    def test_many_lines_match_with_free_games(self):
        icon_set = np.array([[2, 9, 0, 9, 11],
                             [0, 3, 11, 8, 2],
                             [9, 11, 1, 6, 5]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(420, int(round(payout.payout * self.bet)))
        self.assertEqual(25, payout.free_games)
        self.assertEqual(25, payout.multiplier_2x)


class TestDragon(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[DRAGON.name]
        self.bet = 50

    def test_many_wild_match(self):
        icon_set = np.array([[12, 1, 10, 3, 8],
                             [12, 8, 4, 7, 8],
                             [3, 8, 7, 4, 8],
                             [9, 8, 1, 6, 8]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(150, payout)

    def test_many_wild_match_2(self):
        icon_set = np.array([[6, 6, 9, 6, 4],
                             [5, 1, 2, 2, 0],
                             [10, 8, 8, 7, 7],
                             [0, 5, 1, 1, 2]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(320, payout)

    def test_many_wild_match_3(self):
        icon_set = np.array([[10, 6, 0, 3, 2],
                             [5, 1, 9, 7, 7],
                             [2, 8, 2, 4, 3],
                             [0, 5, 8, 0, 11]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(70, payout)


class TestVulcan(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[VULCAN.name]
        self.bet = 50

    def test_wild_and_nonwild_match(self):
        icon_set = np.array([[12, 5, 9, 11, 3],
                             [1, 3, 3, 0, 6],
                             [3, 9, 0, 6, 5]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(80, payout)

    def test_three_matches(self):
        icon_set = np.array([[1, 6, 5, 9, 1],
                             [5, 9, 3, 9, 9],
                             [12, 5, 9, 6, 5]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(190, payout)

    def test_free_game_bonus(self):
        icon_set = np.array([[3, 11, 2, 7, 7],
                             [4, 1, 11, 5, 4],
                             [2, 6, 0, 4, 5]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(0, int(round(payout.payout * self.bet)))
        self.assertEqual(10, payout.free_games)


class TestBells(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[BELLS.name]
        self.bet = 100

    def test_expanding_columns(self):
        icon_set = np.array([[1, 0, 15, 2, 7],
                             [6, 6, 6, 15, 3],
                             [4, 3, 2, 1, 15]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(1100, payout)  # 600 (base) + 500 (expanding)


class TestDisco(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[DISCO.name]
        self.bet = 50

    def test_wild_disco_ball(self):
        icon_set = np.array([[14, 1, 1, 2, 0],
                             [1, 12, 8, 7, 5],
                             [8, 6, 5, 5, 15],
                             [1, 1, 15, 5, 10]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(30, payout)

    def test_many_halos(self):
        icon_set = np.array([[13, 13, 1, 0, 13],
                             [11, 13, 12, 6, 13],
                             [1, 13, 5, 8, 0],
                             [8, 13, 8, 0, 11]])

        payout = int(round(self.ruleset.calculate_payout(icon_set).payout * self.bet))
        self.assertEqual(120, payout)

    def test_scattergame_reward(self):
        icon_set = np.array([[15, 0, 13, 10, 0],
                             [10, 12, 13, 8, 5],
                             [15, 0, 13, 15, 15],
                             [5, 8, 10, 8, 10]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(0, int(round(payout.payout * self.bet)))
        self.assertEqual(5, payout.free_games)

    def test_big_bonus(self):
        icon_set = np.array([[7, 5, 0, 3, 1],
                             [0, 5, 9, 9, 7],
                             [6, 1, 7, 9, 0],
                             [8, 9, 6, 9, 5]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(820, int(round(payout.payout * self.bet)))

    def test_vinyls(self):
        icon_set = np.array([[9, 8, 8, 5, 15],
                             [14, 1, 1, 15, 9],
                             [5, 8, 5, 0, 6],
                             [1, 0, 7, 6, 1]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(40, int(round(payout.payout * self.bet)))

    def test_many_halo(self):
        icon_set = np.array([[1, 9, 13, 9, 6],
                             [9, 13, 13, 2, 9],
                             [13, 13, 13, 9, 0],
                             [13, 13, 13, 5, 7]])

        payout = self.ruleset.calculate_payout(icon_set)
        self.assertEqual(28800, int(round(payout.payout * self.bet)))


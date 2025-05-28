import unittest

import numpy as np

from app.payout import PayoutEstimator
from fixture.predefined_rulesets import predefined_rulesets
from fixture.predefined_slots import MEGAREELS


class TestMegaReels(unittest.TestCase):
    def setUp(self):
        self.ruleset = predefined_rulesets[MEGAREELS.name]
        self.bet = 100

    def test_all_same(self):
        icon_set = np.array([[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]])

        payout = self.ruleset.calculate_payout(icon_set) * self.bet
        self.assertEqual(8000, payout)

    def test_star_diagonal(self):
        icon_set = np.array([[6, 1, 2],
                             [4, 6, 3],
                             [2, 7, 6]])

        payout = self.ruleset.calculate_payout(icon_set) * self.bet
        self.assertEqual(4000, payout)

    def test_three_lines(self):
        icon_set = np.array([[5, 1, 5],
                             [5, 5, 5],
                             [5, 7, 5]])

        payout = self.ruleset.calculate_payout(icon_set) * self.bet
        self.assertEqual(3600, payout)

    def test_three_lines_different(self):
        icon_set = np.array([[5, 5, 5],
                             [5, 5, 5],
                             [0, 0, 0]])

        payout = self.ruleset.calculate_payout(icon_set) * self.bet
        self.assertEqual(2500, payout)

from attrs import define

from app.payout import PayoutEstimator
from utils.constants import MAX_REELS_IN_GAME


@define
class Strategy:
    max_loss: int
    gains: int
    position_to_stop: int


@define
class OptimalStrategyFinder:
    payout_estimator: PayoutEstimator

    def calculate(self, start_index: int, end_index: int, bet: int) -> Strategy:
        position_to_stop = start_index
        best_payout = 0
        budget = bet
        budget_for_best_payout = bet
        for i in range(start_index, end_index):
            index = i % MAX_REELS_IN_GAME
            estimate_so_far = self.payout_estimator.estimate(index, 1, bet)
            if estimate_so_far.payout > best_payout:
                best_payout = estimate_so_far.payout
                position_to_stop = index
                budget_for_best_payout = budget
            if estimate_so_far.payout < budget:
                budget = estimate_so_far.payout

        return Strategy(budget_for_best_payout, best_payout, position_to_stop)


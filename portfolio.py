import numpy as np


class Portfolio:

    def __init__(self, cash, market_size):
        # (T,N) matrices where t in [0,T] is the day and n in [0,N] is the asset.
        self.weights = np.zeros((1, market_size))
        self.weights[0][0] = 1
        self.quantities = np.zeros((1, market_size))
        self.quantities[0][0] = cash

        # (T,m) index to compute sharpe ratio in the reward function
        self.sharpe_cache = None

    def update_transaction(self, target, prices):
        # append a new row to the weights and quantities as close as the target as possible,
        # adjusted by the transaction cost.

        # Compute total value of assets
        total_budget = np.sum(self.quantities[-1][:]*prices)

        # Compute weights drift, delta and transaction cost
        drifted_weights = self.quantities[-1][:]*prices/total_budget
        delta_weights = target-drifted_weights

        # Compute amount of money worth of each stock this delta allows
        assets_budget = delta_weights*total_budget

        # Round quantities to the floor integer according to allocated money
        delta_quantities = np.floor(assets_budget/prices)

        # adjust quantities accordingly, transaction costs will be here
        new_quantities = self.quantities+delta_quantities
        self.quantities = np.append(self.quantities, new_quantities, axis=0)

        # sum unalocated money
        unalocated_money = total_budget-np.sum(new_quantities*prices)
        self.quantities[-1][0] = self.quantities[-1][0] + unalocated_money

        # Compute new real weights
        assets_values = self.quantities[-1][:]*prices
        new_weights = assets_values/np.sum(assets_values)
        self.weights = np.append(self.weights, new_weights, axis=0)

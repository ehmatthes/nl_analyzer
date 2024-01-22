import pandas as pd
import numpy as np

from data import ghost_resources as gr

class Pricer:
    def __init__(self, config):
        self.config = config

        self._initialize_data()
        self._fill_platform_data()

    # def get_costs_substack(self):
    #     """Calculate cost for every increment of 10 users.

    #     Returns:
    #         list: [int, int, ...]
    #     """
    #     return [int(0.1*rev) for rev in self.df["revenues"]]


    # def get_percentages_substack(self):
    #     """Sustack has a flat 0.10 across all levels."""
    #     return [0.1 for _ in range(0, self.config.max_subs, 10)]

    def get_costs_ghostpro(self):
        """Calculate cost for every increment of 10 users.

        Returns:
            list: [int, int, ...]
        """
        costs = []
        price_tiers = gr.get_price_tiers()
        price_tiers.reverse()
        for num_users in range(0, self.config.max_subs, 10):
            yearly_cost = -1
            for threshold, cost in price_tiers:
                # threshold, cost = price_tier
                # print(index, threshold, cost)
                # sys.exit()
                if num_users >= threshold:
                    yearly_cost = cost
                    break

            costs.append(yearly_cost)
        return costs

    def get_percentages_ghostpro(self):
        """Return list of percentages of cost/rev."""
        costs = self.get_costs_ghostpro()
        return [cost / rev if rev > 0 else None for cost, rev in zip(costs, self.df["revenues"])]

    # --- Helper methods ---

    def _initialize_data(self):
        """Build the dataframe that will be used throughout class."""
        user_levels = pd.Series([num_users for num_users in range(0, self.config.max_subs, 10)])

        revenues = pd.Series([
            num_users * self.config.paid_ratio * self.config.avg_revenue
            for num_users in user_levels
        ])

        self.df = pd.DataFrame({
            "user_levels": user_levels,
            "revenues": revenues,
            "costs_ss": np.nan,
            "percent_rev_ss": np.nan,
            "costs_gp": np.nan,
            "percent_rev_gp": np.nan,
            })

    def _fill_platform_data(self):
        """Fill only platform data that's currently being used."""
        if self.config.show_ss:
            self._fill_data_ss()
        if self.config.show_gp:
            self._fill_data_gp()

    def _fill_data_ss(self):
        """Fill Substack data."""
        self.df["costs_ss"] = pd.Series([int(0.1*rev) for rev in self.df["revenues"]])
        self.df["percent_rev_ss"] = pd.Series([0.1 for _ in self.df["user_levels"]])


    def _fill_data_gp(self):
        """Fill Ghost Pro data."""
        pass


# Simple profiling tool.
if __name__ == "__main__":
    pricer = Pricer()
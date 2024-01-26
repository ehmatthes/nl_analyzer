import pandas as pd
import numpy as np

from config import Config
from data import ghost_resources as gr


class Pricer:
    def __init__(self, config):
        self.config = config

        self._initialize_data()
        self._fill_platform_data()

    # --- Helper methods ---

    def _initialize_data(self):
        """Build the dataframe that will be used throughout class."""
        user_levels = pd.Series(
            [num_users for num_users in range(0, self.config.max_subs, 10)]
        )

        revenues = pd.Series(
            [
                num_users * self.config.paid_ratio * self.config.avg_revenue
                for num_users in user_levels
            ]
        )

        self.df = pd.DataFrame(
            {
                "user_levels": user_levels,
                "revenues": revenues,
                # Substack
                "costs_ss": np.nan,
                "percent_rev_ss": np.nan,
                "profits_ss": np.nan,
                # Ghost pro
                "costs_gp": np.nan,
                "percent_rev_gp": np.nan,
                "profits_gp": np.nan,
                # beehiiv
                "costs_bh": np.nan,
                "percent_rev_bh": np.nan,
                "profits_bh": np.nan,
                # Buttondown
                "costs_bd": np.nan,
                "percent_rev_bd": np.nan,
                "profits_bd": np.nan,
            }
        )

    def _fill_platform_data(self):
        """Fill only platform data that's currently being used."""
        if self.config.show_ss:
            self._fill_data_ss()
        if self.config.show_gp:
            self._fill_data_gp()
        if self.config.show_bh:
            self._fill_data_bh()
        if self.config.show_bd:
            self._fill_data_bd()

    def _fill_data_ss(self):
        """Fill Substack data."""
        self.df["costs_ss"] = pd.Series([int(0.1 * rev) for rev in self.df["revenues"]])
        self.df["percent_rev_ss"] = pd.Series([0.1 for _ in self.df["user_levels"]])

        self.df["profits_ss"] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df["costs_ss"])]
        )

    def _fill_data_gp(self):
        """Fill Ghost Pro data."""
        self._fill_costs_gp()
        self.df["percent_rev_gp"] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df["costs_gp"], self.df["revenues"])
            ]
        )

        self.df["profits_gp"] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df["costs_gp"])]
        )

    def _fill_data_bh(self):
        """Fill beehiiv data."""
        self._fill_costs_bh()
        self.df["percent_rev_bh"] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df["costs_bh"], self.df["revenues"])
            ]
        )

        self.df["profits_bh"] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df["costs_bh"])]
        )

    def _fill_data_bd(self):
        """Fill Buttondown data."""
        self._fill_costs_bd()
        self.df["percent_rev_bd"] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df["costs_bd"], self.df["revenues"])
            ]
        )

        self.df["profits_bd"] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df["costs_bd"])]
        )

    def _fill_costs_gp(self):
        """Fill costs column for Ghost Pro."""
        costs = []
        price_tiers = gr.get_price_tiers()
        price_tiers.reverse()
        for num_users in self.df["user_levels"]:
            yearly_cost = -1
            for threshold, cost in price_tiers:
                if num_users >= threshold:
                    yearly_cost = cost
                    break

            costs.append(yearly_cost)

        self.df["costs_gp"] = pd.Series(costs)

    def _fill_costs_bh(self):
        """Fill costs column for beehiiv."""
        costs = []
        for num_users in self.df["user_levels"]:
            if num_users <= 2500:
                costs.append(0)
            elif num_users <= 10_000:
                costs.append(42 * 12)
            elif num_users <= 100_000:
                costs.append(84 * 12)
        self.df["costs_bh"] = pd.Series(costs)

    def _fill_costs_bd(self):
        """Fill costs column for Buttondown.

        Annual plan gets two months free, so cost is 10*monthly rate.
        """
        costs = []
        for num_users in self.df["user_levels"]:
            if num_users <= 100:
                costs.append(0)
            elif num_users <= 1_000:
                costs.append(90)
            elif num_users <= 5_000:
                costs.append(290)
            elif num_users <= 10_000:
                costs.append(790)
            elif num_users <= 20_000:
                costs.append(1390)
            else:
                cost = self._get_cost_bd_high(num_users)
                costs.append(cost)
        self.df["costs_bd"] = pd.Series(costs)

    @staticmethod
    def _get_cost_bd_high(num_users):
        """Calculate enterprise tier costs for Buttondown (>20k subscribers)."""
        # Go through batches of subscribers, until none left.
        thousands = int(round(num_users, -3) / 1000)

        # --- Base tier of 20k users, $139/month
        # Subtract 20k users, and add base cost.
        thousands -= 20
        monthly_cost = 139

        # --- Tier 1: 20k-40k users, $5/month per 1,000 users.
        # Subtract 20k, and look at whether that's positive or negative.
        # If negative, find the batch size for this tier.
        thousands -= 20
        if thousands <= 0:
            # Find out the batch of users in this tier.
            batch = 20 + thousands
            monthly_cost += 5 * batch
            return monthly_cost * 10

        # This tier is full; add full tier cost
        monthly_cost += 5 * 20

        # --- Tier 2: 40k-60k users, $4/month per 1,000 users.
        thousands -= 20
        if thousands <= 0:
            batch = 20 + thousands
            monthly_cost += 4 * batch
            return monthly_cost * 10

        # This tier is full; add full tier cost
        monthly_cost += 4 * 20

        # --- Tier 3: 60k-80k users, $3/month per 1,000 users.
        thousands -= 20
        if thousands <= 0:
            batch = 20 + thousands
            monthly_cost += 3 * batch
            return monthly_cost * 10

        # This tier is full; add full tier cost
        monthly_cost += 3 * 20

        # --- Tier 4: 80k-100k users, $2/month per 1,000 users.
        thousands -= 20
        if thousands <= 0:
            batch = 20 + thousands
            monthly_cost += 2 * batch
            return monthly_cost * 10

        # This tier is full; add full tier cost
        monthly_cost += 2 * 20

        return monthly_cost


# Simple profiling tool.
if __name__ == "__main__":
    config = Config()
    pricer = Pricer(config)

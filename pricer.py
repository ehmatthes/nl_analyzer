import pandas as pd
import numpy as np

from nl_config import NLConfig
from data import ghost_resources as gr
from utils import pricer_utils


class Pricer:
    def __init__(self, nl_config):
        self.nl_config = nl_config

        self._initialize_df()
        self._fill_data()

    # --- Helper methods ---

    def _initialize_df(self):
        """Build the dataframe that will be used throughout class."""
        step_size = int(self.nl_config.max_subs / self.nl_config.num_points)
        if step_size == 0:
            step_size = 1

        # The columns user_levels and revenues are used by all platforms.
        user_levels = pd.Series(
            [num_users for num_users in range(0, self.nl_config.max_subs, step_size)]
        )
        revenues = pd.Series(
            [
                num_users * self.nl_config.paid_ratio * self.nl_config.avg_revenue
                for num_users in user_levels
            ]
        )

        df_data = {
            "user_levels": user_levels,
            "revenues": revenues,
        }

        # Add a group of columns for each platform that's visible.
        # For example, if Ghost Pro is visible:
        # df[("gp", "costs")] will return the series of costs for Ghost.
        for platform in self.nl_config.visible_platforms:
            df_data.update(
                {
                    (platform.code, "costs"): np.nan,
                    (platform.code, "percent_rev"): np.nan,
                    (platform.code, "profits"): np.nan,
                }
            )

        self.df = pd.DataFrame(df_data)

    def _fill_data(self):
        """Fill only platform data that's currently being used."""
        # Call each platform's _fill_costs_{platform_code}() method.
        for platform in self.nl_config.visible_platforms:
            fn_name = getattr(self, f"_fill_costs_{platform.code}")
            fn_name()

            self._fill_percent_rev_data(platform)
            self._fill_profit_data(platform)

    def _fill_costs_ss(self):
        """Fill Substack data."""
        self.df[("ss", "costs")] = pd.Series(
            [int(0.1 * rev) for rev in self.df["revenues"]]
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

        self.df[("gp", "costs")] = pd.Series(costs)

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
                cost = pricer_utils._get_cost_bd_high(num_users)
                costs.append(cost)
        self.df[("bd", "costs")] = pd.Series(costs)

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
        self.df[("bh", "costs")] = pd.Series(costs)

    def _fill_costs_ck(self):
        """Fill costs column for ConvertKit.

        Annual plan gets two months free, so cost is 10*monthly rate.
        """
        costs = []
        for num_users in self.df["user_levels"]:
            if num_users <= 1_000:
                costs.append(0)
            elif num_users <= 3_000:
                costs.append(490)
            elif num_users <= 5_000:
                costs.append(790)
            elif num_users <= 8_000:
                costs.append(990)
            elif num_users <= 10_000:
                costs.append(1190)
            elif num_users <= 15_000:
                costs.append(1490)
            elif num_users <= 20_000:
                costs.append(1790)
            elif num_users <= 25_000:
                costs.append(1990)
            else:
                # Above 25k users, it's $1990 plus $600 for every 10k users.
                above_25k = num_users - 25_000
                multiplier = (above_25k // 10_000) + 1
                cost = 1990 + multiplier * 600
                costs.append(cost)

        self.df[("ck", "costs")] = pd.Series(costs)


    def _fill_percent_rev_data(self, platform):
        """Fill the platform's percent of revenue column."""
        if platform.code == "ss":
            self.df[("ss", "percent_rev")] = pd.Series(
                [0.1 for _ in self.df["user_levels"]]
            )
        else:
            self.df[(platform.code, "percent_rev")] = pd.Series(
                [
                    cost / rev if rev > 0 else np.nan
                    for cost, rev in zip(self.df[(platform.code, "costs")], self.df["revenues"])
                ]
            )

    def _fill_profit_data(self, platform):
        """Fill the platform's profit column."""
        self.df[(platform.code, "profits")] = pd.Series(
            [
                rev - cost
                for rev, cost in zip(self.df["revenues"], self.df[(platform.code, "costs")])
            ]
        )
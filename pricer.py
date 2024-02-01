import pandas as pd
import numpy as np

from nl_config import NLConfig
from data import ghost_resources as gr


class Pricer:
    def __init__(self, nl_config):
        self.nl_config = nl_config

        self._initialize_data()
        self._fill_platform_data()

    # --- Helper methods ---

    def _initialize_data(self):
        """Build the dataframe that will be used throughout class."""
        # Fig size is 6.4x4, so 6.4" * 200dpi -> 1280 pixels per chart.
        # Use of int makes this fairly approximate, but aiming for order of magnitude.
        step_size = int(self.nl_config.max_subs / 1280)
        if step_size == 0:
            step_size = 1

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
        # if self.nl_config.ss_config.show:
        #     df_data.update(
        #         {
        #             "costs_ss": np.nan,
        #             "percent_rev_ss": np.nan,
        #             "profits_ss": np.nan,
        #         }
        #     )
        # if self.nl_config.gp_config.show:
        #     df_data.update(
        #         {
        #             "costs_gp": np.nan,
        #             "percent_rev_gp": np.nan,
        #             "profits_gp": np.nan,
        #         }
        #     )
        # if self.nl_config.bh_config.show:
        #     df_data.update(
        #         {
        #             "costs_bh": np.nan,
        #             "percent_rev_bh": np.nan,
        #             "profits_bh": np.nan,
        #         }
        #     )
        # if self.nl_config.bd_config.show:
        #     df_data.update(
        #         {
        #             "costs_bd": np.nan,
        #             "percent_rev_bd": np.nan,
        #             "profits_bd": np.nan,
        #         }
        #     )
        # if self.nl_config.ck_config.show:
        #     df_data.update(
        #         {
        #             "costs_ck": np.nan,
        #             "percent_rev_ck": np.nan,
        #             "profits_ck": np.nan,
        #         }
        #     )

        # DEV: This could be made as a loop using the dict lookup for configs.
        if self.nl_config.gp_config.show:
            df_data.update(
                {
                    ("gp", "costs"): np.nan,
                    ("gp", "percent_rev"): np.nan,
                    ("gp", "profits"): np.nan,
                }
            )
        if self.nl_config.bd_config.show:
            df_data.update(
                {
                    ("bd", "costs"): np.nan,
                    ("bd", "percent_rev"): np.nan,
                    ("bd", "profits"): np.nan,
                }
            )
        if self.nl_config.bh_config.show:
            df_data.update(
                {
                    ("bh", "costs"): np.nan,
                    ("bh", "percent_rev"): np.nan,
                    ("bh", "profits"): np.nan,
                }
            )
        if self.nl_config.ss_config.show:
            df_data.update(
                {
                    ("ss", "costs"): np.nan,
                    ("ss", "percent_rev"): np.nan,
                    ("ss", "profits"): np.nan,
                }
            )
        if self.nl_config.ck_config.show:
            df_data.update(
                {
                    ("ck", "costs"): np.nan,
                    ("ck", "percent_rev"): np.nan,
                    ("ck", "profits"): np.nan,
                }
            )

        self.df = pd.DataFrame(df_data)

    def _fill_platform_data(self):
        """Fill only platform data that's currently being used."""
        if self.nl_config.ss_config.show:
            self._fill_data_ss()
        if self.nl_config.gp_config.show:
            self._fill_data_gp()
        if self.nl_config.bh_config.show:
            self._fill_data_bh()
        if self.nl_config.bd_config.show:
            self._fill_data_bd()
        if self.nl_config.ck_config.show:
            self._fill_data_ck()

    def _fill_data_ss(self):
        """Fill Substack data."""
        self.df[("ss", "costs")] = pd.Series([int(0.1 * rev) for rev in self.df["revenues"]])
        self.df[("ss", "percent_rev")] = pd.Series([0.1 for _ in self.df["user_levels"]])

        self.df[("ss", "profits")] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df[("ss", "costs")])]
        )

    def _fill_data_gp(self):
        """Fill Ghost Pro data."""
        self._fill_costs_gp()
        self.df[("gp", "percent_rev")] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df[("gp", "costs")], self.df["revenues"])
            ]
        )

        self.df[("gp", "profits")] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df[("gp", "costs")])]
        )


    def _fill_data_bh(self):
        """Fill beehiiv data."""
        self._fill_costs_bh()
        self.df[("bh", "percent_rev")] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df[("bh", "costs")], self.df["revenues"])
            ]
        )

        self.df[("bh", "profits")] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df[("bh", "costs")])]
        )


    def _fill_data_bd(self):
        """Fill Buttondown data."""
        self._fill_costs_bd()
        self.df[("bd", "percent_rev")] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df[("bd", "costs")], self.df["revenues"])
            ]
        )

        self.df[("bd", "profits")] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df[("bd", "costs")])]
        )


    def _fill_data_ck(self):
        """Fill ConvertKit data."""
        self._fill_costs_ck()
        self.df[("ck", "percent_rev")] = pd.Series(
            [
                cost / rev if rev > 0 else np.nan
                for cost, rev in zip(self.df[("ck", "costs")], self.df["revenues"])
            ]
        )

        self.df[("ck", "profits")] = pd.Series(
            [rev - cost for rev, cost in zip(self.df["revenues"], self.df[("ck", "costs")])]
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
        self.df[("bd", "costs")] = pd.Series(costs)

    def _fill_costs_ck(self):
        """Fill costs column for ConvertKit.

        Annual plan gets two months free, so cost is 10*monthly rate.
        """
        costs = []
        for num_users in self.df["user_levels"]:
            # Note: This works out to $600/10k users above 25k users.
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
            elif num_users <= 35_000:
                costs.append(2590)
            elif num_users <= 45_000:
                costs.append(3190)
            elif num_users <= 55_000:
                costs.append(3790)
            elif num_users <= 65_000:
                costs.append(4390)
            elif num_users <= 75_000:
                costs.append(4990)
            elif num_users <= 85_000:
                costs.append(5590)
            elif num_users <= 95_000:
                costs.append(6190)
            elif num_users <= 105_000:
                costs.append(6_790)
        self.df[("ck", "costs")] = pd.Series(costs)

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
    nl_config = NLConfig()
    pricer = Pricer(nl_config)

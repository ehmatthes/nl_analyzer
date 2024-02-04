import pandas as pd
import numpy as np

from nl_config import NLConfig
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
        for platform in self.nl_config.visible_platforms:
            # Call each platorm's get_costs_{platform_code}() function.
            fn_name = getattr(pricer_utils, f"get_costs_{platform.code}")
            self.df[(platform.code, "costs")] = fn_name(self.df)

            self._fill_percent_rev_data(platform)
            self._fill_profit_data(platform)

    def _fill_percent_rev_data(self, platform):
        """Fill the platform's percent of revenue column."""
        # Substack is 0.1 for all user levels, but it's not worth a conditional block
        # for that. This returns 0.1 for Substack costs anyways.
        costs = self.df[(platform.code, "costs")]
        revenues = self.df["revenues"]
        self.df[(platform.code, "percent_rev")] = np.where(
            revenues > 0, costs / revenues, np.nan
        )

    def _fill_profit_data(self, platform):
        """Fill the platform's profit column."""
        self.df[(platform.code, "profits")] = (
            self.df["revenues"] - self.df[(platform.code, "costs")]
        )


if __name__ == "__main__":
    # This block allows this file to be run directly, for profiling purposes.
    nl_config = NLConfig()
    for platform in nl_config.platforms:
        platform.show = True
    pricer = Pricer(nl_config)

    from charts import cost_chart

    chart = cost_chart.get_plot(nl_config, pricer.df)

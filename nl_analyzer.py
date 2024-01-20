"""Compare annual costs of various newsletter platforms.

DEV notes:
- Add micro-adjustment sliders for each setting?
- Reformat paid ratio slider as an actual percentage.
- Make it work for Substack and Ghost, then share with group.
- Make a repo.
"""

import streamlit as st
import matplotlib.pyplot as plt


class Pricer:
    def __init__(self, max_subs=10_000, paid_ratio=0.02):
        self.max_subs = max_subs
        self.paid_ratio = paid_ratio

        # Average annual revenue per paid user. Must take into consideration discounts.
        self.avg_revenue = 40

    def get_costs_substack(self):
        """Calculate cost for every increment of 100 users.

        Returns:
            list: [int, int, ...]
        """
        costs = []
        for num_users in range(0, self.max_subs, 100):
            revenue = num_users * self.paid_ratio * self.avg_revenue
            cost = int(0.1 * revenue)
            costs.append(cost)
        return costs

    def get_revenues_substack(self):
        """Calculate revenue for increments of 100 users."""
        revenues = []
        for num_users in range(0, self.max_subs, 100):
            revenue = num_users * self.paid_ratio * self.avg_revenue
            revenues.append(revenue)
        return revenues

    def get_costs_ghostpro(self):
        """Calculate cost for every increment of 100 users.

        Returns:
            list: [int, int, ...]
        """
        # Use cheapest available plan. These are monthly costs, billed annually. This
        # reflects how pricing is presented on ghost.org.
        price_tiers = [
            (500, 9),
            (3000, 15),
            (5000, 40),
            (8000, 65),
            (10000, 82),
            (15000, 99),
            (20000, 124),
            (25000, 149)
        ]

        costs = []
        for num_users in range(0, self.max_subs, 100):
            # Set default cost here.
            monthly_cost = 1000
            for limit, cost in price_tiers:
                if num_users <= limit:
                    monthly_cost = cost
                    break

            cost = 12 * monthly_cost
            costs.append(cost)
        return costs


# Get attributes.
max_subs = st.slider("Number of subscribers", value=10_000, max_value=100_000, step=100)
paid_ratio = st.slider("Paid subscriber ratio", value=0.02, max_value=1.0, step=0.001, format="%.3f")

pricer = Pricer(max_subs=max_subs, paid_ratio=paid_ratio)
ss_costs = pricer.get_costs_substack()
ss_revenues = pricer.get_revenues_substack()
gp_costs = pricer.get_costs_ghostpro()

# Make chart.
x_values = range(0, max_subs, 100)
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
ax.plot(x_values, ss_costs)
ax.plot(x_values, gp_costs)

ax.set_title("Annual costs of hosting a newsletter")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Annual cost")

fig

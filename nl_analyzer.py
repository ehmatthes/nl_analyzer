"""Compare annual costs of various newsletter platforms."""

import sys

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
        # Use cheapest available plan. These are annual plans.
        # Data from: https://ghost.org/js/pricing.min.js
        price_tiers = [
            (0, 108),
            (1000, 180),
            (3000, 480),
            (5000, 780),
            (8000, 984),
            (10000, 1188),
            (15000, 1488),
            (20000, 1788),
            (25000, 1980),
            (35000, 2580),
            (45000, 3180),
            (55000, 3780),
            (65000, 4380),
            (75000, 4980),
            (85000, 5580),
            (95000, 6180),
            (105000, 6780),
            (115000, 7380),
            (125000, 7980),
            (135000, 8580),
            (145000, 9180),
            (155000, 9780),
            (165000, 10380),
            (175000, 10980),
            (185000, 11580),
            (195000, 12180),
            (205000, 12780),
            (215000, 13380),
            (225000, 13980),
            (235000, 14580),
            (245000, 15180),
            (265000, 16380),
            (285000, 17580),
            (305000, 18780),
            (325000, 19980),
            (345000, 21180),
            (365000, 22380),
            (385000, 22980),
        ]

        costs = []
        price_tiers.reverse()
        for num_users in range(0, self.max_subs, 100):
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


# Get attributes.
max_subs = st.slider("Number of subscribers", value=10_000, max_value=100_000, step=100)
paid_ratio = st.slider(
    "Paid subscriber ratio", value=0.02, max_value=1.0, step=0.001, format="%.3f"
)

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

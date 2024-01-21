"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import matplotlib.pyplot as plt


class Pricer:
    def __init__(self, max_subs=10_000, paid_ratio=0.02, avg_revenue=50):
        self.max_subs = max_subs
        self.paid_ratio = paid_ratio

        # Average annual revenue per paid user. Must take into consideration discounts.
        self.avg_revenue = avg_revenue

    def get_costs_substack(self):
        """Calculate cost for every increment of 10 users.

        Returns:
            list: [int, int, ...]
        """
        costs = []
        for num_users in range(0, self.max_subs, 10):
            revenue = num_users * self.paid_ratio * self.avg_revenue
            cost = int(0.1 * revenue)
            costs.append(cost)
        return costs

    def get_revenues_substack(self):
        """Calculate revenue for increments of 10 users."""
        revenues = []
        for num_users in range(0, self.max_subs, 10):
            revenue = num_users * self.paid_ratio * self.avg_revenue
            revenues.append(revenue)
        return revenues

    def get_percentages_substack(self):
        """Sustack has a flat 0.10 across all levels."""
        return [0.1 for _ in range(0, self.max_subs, 10)]


    def get_costs_ghostpro(self):
        """Calculate cost for every increment of 10 users.

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
        for num_users in range(0, self.max_subs, 10):
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
        revenues = self.get_revenues_substack()
        costs = self.get_costs_ghostpro()
        return [cost/rev if rev > 0 else None for cost, rev in zip(costs, revenues)]


# Get attributes.
max_subs_macro = st.slider(
    "Number of subscribers", value=10_000, max_value=100_000, step=10
)
max_subs_micro = st.slider(
    "Number of subscribers (fine tuning)", value=0, max_value=1_000, step=10
)
max_subs = max_subs_macro + max_subs_micro

# Build sidebar.
st.sidebar.write("**Platforms:**")
show_ss = st.sidebar.checkbox("Substack", value=True)
show_gp = st.sidebar.checkbox("Ghost Pro", value=True)
st.sidebar.write("---")

paid_ratio = st.sidebar.slider(
    "Paid subscriber ratio", value=0.02, max_value=1.0, step=0.001, format="%.3f"
)

avg_revenue = st.sidebar.slider(
    "Average annual revenue per paid user", value=50, max_value=500, step=1
)

st.sidebar.write("---")

st.sidebar.write(f"**Max subscribers:** {max_subs:,}")
st.sidebar.write(f"**Paid ratio:** {paid_ratio*100:.1f}%")
st.sidebar.write(f"**Average revenue/ paid user:** ${avg_revenue:.2f}")

"---"

pricer = Pricer(max_subs=max_subs, paid_ratio=paid_ratio, avg_revenue=avg_revenue)
ss_costs = pricer.get_costs_substack()
ss_revenues = pricer.get_revenues_substack()
gp_costs = pricer.get_costs_ghostpro()

# Make cost chart.
x_values = range(0, max_subs, 10)
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()

# Define horizontal placement of all line labels.
label_pos_x = x_values[-1] + 0.01 * max_subs

# Add Substack data.
if show_ss:
    ax.plot(x_values, ss_costs)
    label_pos_y = ss_costs[-1] - 0.005 * ax.get_ylim()[1]
    ax.annotate("Substack", (label_pos_x, label_pos_y))

# Add Ghost data.
if show_gp:
    ax.plot(x_values, gp_costs)
    label_pos_y = gp_costs[-1] - 0.01 * ax.get_ylim()[1]
    ax.annotate("Ghost Pro", (label_pos_x, label_pos_y))

ax.set_title("Annual cost of hosting a newsletter")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Annual cost")

fig

"---"

# Make percentage chart.
fig, ax = plt.subplots()
if show_ss:
    ss_percentages = pricer.get_percentages_substack()
    ax.plot(x_values, ss_percentages)
    label_pos_y = ss_percentages[-1] - 0.005 * ax.get_ylim()[1]
    ax.annotate("Substack", (label_pos_x, label_pos_y))

if show_gp:
    gp_percentages = pricer.get_percentages_ghostpro()
    ax.plot(x_values, gp_percentages)
    label_pos_y = gp_percentages[-1] - 0.01 * ax.get_ylim()[1]
    ax.annotate("Ghost Pro", (label_pos_x, label_pos_y))

# ax.set_ylim([0,1])
ax.axis([0, 1.05*max_subs, 0, 0.2])
y_vals = ax.get_yticks()
ax.set_yticklabels(['{:,.1%}'.format(y_val) for y_val in y_vals])

ax.set_title("Annual cost as percent of revenue")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Percent of revenue")

fig
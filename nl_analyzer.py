import streamlit as st
import matplotlib.pyplot as plt


class Pricer:
    def __init__(self, max_subs=10_000):
        self.max_subs = max_subs
        self.paid_ratio = 0.02

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


# Get attributes.
max_subs = st.slider("Number of subscribers", value=10_000, max_value=100_000, step=100)

pricer = Pricer(max_subs=max_subs)
ss_costs = pricer.get_costs_substack()

# Make chart.
x_values = range(0, max_subs, 100)
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
ax.plot(x_values, ss_costs)

ax.set_title("Annual costs")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Annual cost")

fig

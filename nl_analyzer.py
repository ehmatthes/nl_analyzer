import streamlit as st


class Pricer:

    def __init__(self):
        self.max_subs = 10_000
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



if __name__ == "__main__":
    pricer = Pricer()
    ss_costs = pricer.get_costs_substack()
    print(ss_costs)

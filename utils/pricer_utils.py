"""Utility functions for the Pricer class."""

import pandas as pd

from utils import ghost_resources as gr


def get_costs_ss(df):
    """Get costs for substack."""
    return pd.Series([int(0.1 * rev) for rev in df["revenues"]])

def get_costs_gp(df):
    """Get costs for Ghost Pro."""
    costs = []
    price_tiers = gr.get_price_tiers()
    price_tiers.reverse()
    for num_users in df["user_levels"]:
        yearly_cost = -1
        for threshold, cost in price_tiers:
            if num_users >= threshold:
                yearly_cost = cost
                break

        costs.append(yearly_cost)

    return pd.Series(costs)

def get_costs_bd(df):
    """Get costs for Buttondown."""
    costs = []
    for num_users in df["user_levels"]:
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
            cost = pricer_utils.get_cost_bd_high(num_users)
            costs.append(cost)

    return pd.Series(costs)

def get_cost_bd_high(num_users):
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

def get_costs_bh(df):
    """Return costs for beehiiv."""
    costs = []
    for num_users in self.df["user_levels"]:
        if num_users <= 2500:
            costs.append(0)
        elif num_users <= 10_000:
            costs.append(42 * 12)
        elif num_users <= 100_000:
            costs.append(84 * 12)

    return pd.Series(costs)

def get_costs_ck(df):
    """Return costs for ConvertKit."""
    costs = []
    for num_users in df["user_levels"]:
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

    return pd.Series(costs)
"""Utility functions for the Pricer class."""

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
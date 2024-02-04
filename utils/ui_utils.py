"""Utility functions for the overall UI."""


def max_subs_options():
    """Return options for max_subs select_slider."""
    # Open end of each range is included by start of next range.
    options = list(range(0, 300, 50))
    options += list(range(300, 1_000, 100))
    options += list(range(1_000, 10_000, 1_000))
    options += list(range(10_000, 25_000, 2_500))
    options += list(range(25_000, 50_000, 5_000))
    options += list(range(50_000, 100_001, 10_000))

    return options


def format_max_subs(num):
    return f"{int(num):,}"


def paid_ratio_options():
    """Return options for paid_ratio select_slider."""
    # Define ranges as integers, then divide to get fractional percents.
    options = list(range(0, 500, 25))
    options += list(range(500, 1_000, 50))
    options += list(range(1_000, 2_500, 100))
    options += list(range(2_500, 10_001, 500))
    options = [option / 10_000 for option in options]

    return options


def format_paid_ratio(num):
    return f"{num*100:.2f}%"

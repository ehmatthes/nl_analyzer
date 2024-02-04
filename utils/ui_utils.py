"""Utility functions for the overall UI."""

def get_max_subs_options():
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
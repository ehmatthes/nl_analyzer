"""Configuration for the overall project.

These are the settings that affect the overall calculuations, and which platforms are
included in the analysis.
"""
from dataclasses import dataclass

@dataclass
class Config:
    """Class for keeping track of overall project settings."""
    show_ss: bool = True
    show_gp: bool = True

    max_subs: int = 10_000
    paid_ratio: float = 0.02
    avg_revenue: int = 50
"""Configuration for the overall project.

These are the settings that affect the overall calculuations, and which platforms are
included in the analysis.
"""
from dataclasses import dataclass

@dataclass
class Config:
    """Class for keeping track of overall project settings."""
    show_ss: bool
    show_gp: bool

    max_subs: int
    paid_ratio: float
    avg_revenue: int
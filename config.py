"""Configuration for the overall project.

These are the settings that affect the overall calculuations, and which platforms are
included in the analysis.
"""
from dataclasses import dataclass


@dataclass
class Config:
    """Class for keeping track of overall project settings."""

    # Input widget settings.
    show_ss: bool = True
    show_gp: bool = True
    show_bh: bool = True

    max_subs: int = 10_000
    paid_ratio: float = 0.02
    avg_revenue: int = 50

    # Plot settings, that can't be covered in a Matplotlib stylesheet.
    ss_color: str = "#DC6931"
    gp_color: str = "black"
    bh_color: str = "#3A43C8"

    aspect_ratio: float = 2.0

    # font sizes
    fs_brand_label: int = 10

    # Spacing
    title_x = -0.1
    title_pad = 20

"""Configuration for the overall project.

These are the settings that affect the overall calculuations, and which platforms are
included in the analysis.

Note: Named NLConfig and nl_config to avoid collision with Streamlit's config.toml.
"""
from dataclasses import dataclass


@dataclass
class NLConfig:
    """Class for keeping track of overall project settings."""

    platform_codes = [
        ("gp", "Gost Pro"),
        ("bd", "Buttondown"),
        ("bh", "beehiiv"),
        ("ss", "Substack"),
        ("ck", "ConvertKit"),
    ]

    # Input widget settings.
    show_gp: bool = True
    show_bd: bool = False
    show_bh: bool = False
    show_ss: bool = True
    show_ck: bool = False

    show_exp_features: bool = False

    max_subs: int = 10_000
    paid_ratio: float = 0.02
    avg_revenue: int = 50

    # Plot settings, that can't be covered in a Matplotlib stylesheet.
    gp_color: str = "black"
    bd_color: str = "#006aff"
    bh_color: str = "#ee87d8"
    ss_color: str = "#DC6931"
    ck_color: str = "#34946d"

    aspect_ratio: float = 2.0

    # font sizes
    fs_brand_label: int = 10

    # Spacing
    title_x = -0.1
    title_pad = 20

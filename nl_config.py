"""Configuration for the overall project.

These are the settings that affect the overall calculuations, and which platforms are
included in the analysis.

Note: Named NLConfig and nl_config to avoid collision with Streamlit's config.toml.
"""
from dataclasses import dataclass


@dataclass
class PlatformConfig:
    code: str
    name: str
    color: str

    show: bool = False


@dataclass
class NLConfig:
    """Class for keeping track of overall project settings."""

    # Platform config.
    gp_config = PlatformConfig(code="gp", name="Ghost Pro", color="black")
    bd_config = PlatformConfig(code="bd", name="Buttondown", color="#006aff")
    bh_config = PlatformConfig(code="bh", name="beehiiv", color="#ee87d8")
    ss_config = PlatformConfig(code="ss", name="Substack", color="#DC6931")
    ck_config = PlatformConfig(code="ck", name="ConvertKit", color="#34946d")

    platforms = [gp_config, bd_config, bh_config, ss_config, ck_config]

    # General config.
    show_exp_features: bool = False

    max_subs: int = 10_000
    paid_ratio: float = 0.02
    avg_revenue: int = 50

    aspect_ratio: float = 2.0

    # Fig size is 6.4x4, so 6.4" * 200dpi -> 1280 pixels per chart.
    # Use of int makes this fairly approximate, but aiming for order of magnitude.
    # That uses too much data, so actually using a fraction of 1280.
    num_points = 256

    # font sizes
    fs_brand_label: int = 10

    # Spacing
    title_x = -0.1
    title_pad = 20

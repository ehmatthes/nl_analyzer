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
    show: bool
    color: str

@dataclass
class NLConfig:
    """Class for keeping track of overall project settings."""

    # platforms = {
    #     "gp": PlatformConfig(name="Ghost Pro", show=True, color="black"),
    #     "bd": PlatformConfig(name="Buttondown", show=False, color="#006aff"),
    #     "bh": PlatformConfig(name="beehiiv", show=False, color="#ee87d8"),
    #     "ss": PlatformConfig(name="Substack", show=True, color="#DC6931"),
    #     "ck": PlatformConfig(name="ConvertKit", show=False, color="#34946d"),
    # }

    gp_config = PlatformConfig(code="gp", name="Ghost Pro", show=True, color="black")
    bd_config = PlatformConfig(code="bd", name="Buttondown", show=False, color="#006aff")
    bh_config = PlatformConfig(code="bh", name="beehiiv", show=False, color="#ee87d8")
    ss_config = PlatformConfig(code="ss", name="Substack", show=True, color="#DC6931")
    ck_config = PlatformConfig(code="ck", name="ConvertKit", show=False, color="#34946d")

    # gp_config: PlatformConfig
    # bd_config: PlatformConfig
    # bh_config: PlatformConfig
    # ss_config: PlatformConfig
    # ck_config: PlatformConfig

    platforms = [gp_config, bd_config, bh_config, ss_config, ck_config]
    # platforms: []

    # platform_codes = [
    #     ("gp", "Gost Pro"),
    #     ("bd", "Buttondown"),
    #     ("bh", "beehiiv"),
    #     ("ss", "Substack"),
    #     ("ck", "ConvertKit"),
    # ]

    # # Input widget settings.
    # show_gp: bool = True
    # show_bd: bool = False
    # show_bh: bool = False
    # show_ss: bool = True
    # show_ck: bool = False

    show_exp_features: bool = False

    max_subs: int = 10_000
    paid_ratio: float = 0.02
    avg_revenue: int = 50

    # # Plot settings, that can't be covered in a Matplotlib stylesheet.
    # gp_color: str = "black"
    # bd_color: str = "#006aff"
    # bh_color: str = "#ee87d8"
    # ss_color: str = "#DC6931"
    # ck_color: str = "#34946d"

    aspect_ratio: float = 2.0

    # font sizes
    fs_brand_label: int = 10

    # Spacing
    title_x = -0.1
    title_pad = 20

    # def __post_init__(self):
    #     self.gp_config = PlatformConfig(code="gp", name="Ghost Pro", show=True, color="black")
    #     self.bd_config = PlatformConfig(code="bd", name="Buttondown", show=False, color="#006aff")
    #     self.bh_config = PlatformConfig(code="bh", name="beehiiv", show=False, color="#ee87d8")
    #     self.ss_config = PlatformConfig(code="ss", name="Substack", show=True, color="#DC6931")
    #     self.ck_config = PlatformConfig(code="ck", name="ConvertKit", show=False, color="#34946d")

        # self.platforms = [gp_config, bd_config, bh_config, ss_config, ck_config]

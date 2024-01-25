from matplotlib import pyplot as plt

from pathlib import Path


def get_plot(config, df):
    ss_costs = df["costs_ss"]
    gp_costs = df["costs_gp"]
    x_values = df["user_levels"]

    # path = Path("charts/nlc_style.mplstyle")
    # assert path.exists()
    # assert not path.exists()

    # plt.style.use(["seaborn-v0_8", "charts/nlc_style.mplstyle"])
    plt.style.use(["seaborn-v0_8-whitegrid", "charts/nlc_style.mplstyle"])
    fig, ax = plt.subplots()

    # Define horizontal placement of all line labels.
    label_pos_x = x_values.iloc[-1] + 0.01 * config.max_subs

    # Add Substack data.
    if config.show_ss:
        ax.plot(x_values, ss_costs, color=config.ss_color)
        label_pos_y = ss_costs.iloc[-1] - 0.005 * ax.get_ylim()[1]
        ax.annotate(
            "Substack",
            (label_pos_x, label_pos_y),
            color=config.ss_color,
            fontsize=config.fs_brand_label,
        )

    # Add Ghost data.
    if config.show_gp:
        ax.plot(x_values, gp_costs, color=config.gp_color)
        label_pos_y = gp_costs.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "Ghost Pro",
            (label_pos_x, label_pos_y),
            color=config.gp_color,
            fontsize=config.fs_brand_label,
        )

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    ax.set_title("Annual cost of hosting a newsletter", pad=20)
    ax.title.set_position([0.0, 1.0])
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Annual cost")

    return fig

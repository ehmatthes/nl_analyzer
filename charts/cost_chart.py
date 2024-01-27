from matplotlib import pyplot as plt
import matplotlib as mpl


def get_plot(config, df):
    ss_costs = df["costs_ss"]
    gp_costs = df["costs_gp"]
    bh_costs = df["costs_bh"]
    bd_costs = df["costs_bd"]
    x_values = df["user_levels"]

    plt.style.use(["seaborn-v0_8-whitegrid", "charts/nlc_style.mplstyle"])
    fig, ax = plt.subplots()

    # Set aspect ratio.
    width = fig.get_size_inches()[0]
    height = width / config.aspect_ratio
    fig.set_size_inches(width, height)

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

    # Add beehiiv data.
    if config.show_bh:
        ax.plot(x_values, bh_costs, color=config.bh_color)
        label_pos_y = bh_costs.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "beehiiv",
            (label_pos_x, label_pos_y),
            color=config.bh_color,
            fontsize=config.fs_brand_label,
        )

    # Add Buttondown data.
    if config.show_bd:
        ax.plot(x_values, bd_costs, color=config.bd_color)
        label_pos_y = bd_costs.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "Buttondown",
            (label_pos_x, label_pos_y),
            color=config.bd_color,
            fontsize=config.fs_brand_label,
        )

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))

    ax.set_title("Annual cost of hosting a newsletter", pad=config.title_pad, x=-0.1)
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Annual cost")

    return fig
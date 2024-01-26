from matplotlib import pyplot as plt
import matplotlib as mpl


def get_plot(config, df):
    ss_profits = df["profits_ss"]
    gp_profits = df["profits_gp"]
    bh_profits = df["profits_bh"]
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
        ax.plot(x_values, ss_profits, color=config.ss_color)
        label_pos_y = ss_profits.iloc[-1] - 0.005 * ax.get_ylim()[1]
        ax.annotate(
            "Substack",
            (label_pos_x, label_pos_y),
            color=config.ss_color,
            fontsize=config.fs_brand_label,
        )

    # Add Ghost data.
    if config.show_gp:
        ax.plot(x_values, gp_profits, color=config.gp_color)
        label_pos_y = gp_profits.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "Ghost Pro",
            (label_pos_x, label_pos_y),
            color=config.gp_color,
            fontsize=config.fs_brand_label,
        )

    # Add beehiiv data.
    if config.show_bh:
        ax.plot(x_values, bh_profits, color=config.bh_color)
        label_pos_y = bh_profits.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "beehiiv",
            (label_pos_x, label_pos_y),
            color=config.bh_color,
            fontsize=config.fs_brand_label,
        )

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))

    ax.set_title("Annual profit of hosting a newsletter", pad=config.title_pad, x=-0.1)
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Annual profit")

    return fig

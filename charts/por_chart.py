from matplotlib import pyplot as plt
import matplotlib as mpl


def get_chart(config, df):
    x_values = df["user_levels"]

    # Define horizontal placement of all line labels.
    label_pos_x = x_values.iloc[-1] + 0.01 * config.max_subs

    # Won't have data if there's no revenue.
    nonzero_revenue = bool(sum(df["revenues"]))

    plt.style.use(["seaborn-v0_8-whitegrid", "charts/nlc_style.mplstyle"])
    fig, ax = plt.subplots()

    # Set aspect ratio.
    width = fig.get_size_inches()[0]
    height = width / config.aspect_ratio
    fig.set_size_inches(width, height)

    if config.show_ss and nonzero_revenue:
        ss_percentages = df["percent_rev_ss"]
        ax.plot(x_values, ss_percentages, color=config.ss_color)
        label_pos_y = ss_percentages.iloc[-1] - 0.02 * ax.get_ylim()[1]
        ax.annotate(
            "Substack",
            (label_pos_x, label_pos_y),
            color=config.ss_color,
            fontsize=config.fs_brand_label,
        )

    if config.show_gp and nonzero_revenue:
        gp_percentages = df["percent_rev_gp"]
        ax.plot(x_values, gp_percentages, color=config.gp_color)
        label_pos_y = gp_percentages.iloc[-1] - 0.0002 * ax.get_ylim()[1]
        ax.annotate(
            "Ghost Pro",
            (label_pos_x, label_pos_y),
            color=config.gp_color,
            fontsize=config.fs_brand_label,
        )

    # Limit of y-axis needs to be at least 15%, but shouldn't over-emphasize high values
    # for only the lowest subscriber levels. Use percentage 1/10 of the way through the set
    # of values, so most of each platform's line is visible.
    if nonzero_revenue:
        try:
            y_max = max(0.15, gp_percentages[int(0.1 * len(gp_percentages))])
        except NameError:
            # Temp fix for when Ghost Pro is not selected.
            y_max = 0.2
        ax.axis([0, 1.05 * config.max_subs, 0, y_max])
        y_vals = ax.get_yticks()
        ax.set_yticklabels(["{:,.1%}".format(y_val) for y_val in y_vals])
    else:
        x_pos = ax.get_xlim()[1] * 0.1
        y_pos = ax.get_ylim()[1] / 2
        ax.annotate("No revenue generated.", (x_pos, y_pos), fontsize=16)

    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))

    ax.set_title("Annual cost as percent of revenue", pad=config.title_pad, x=-0.1)
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Percent of revenue")

    return fig

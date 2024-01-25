from matplotlib import pyplot as plt


def get_plot(config, df):
    ss_costs = df["costs_ss"]
    gp_costs = df["costs_gp"]
    x_values = df["user_levels"]

    plt.style.use("seaborn-v0_8")
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
            fontsize=config.label_font_size,
        )

    # Add Ghost data.
    if config.show_gp:
        ax.plot(x_values, gp_costs, color=config.gp_color)
        label_pos_y = gp_costs.iloc[-1] - 0.01 * ax.get_ylim()[1]
        ax.annotate(
            "Ghost Pro",
            (label_pos_x, label_pos_y),
            color=config.gp_color,
            fontsize=config.label_font_size,
        )

    ax.set_title("Annual cost of hosting a newsletter")
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Annual cost")

    return fig

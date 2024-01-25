from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np


def get_plot(config, df):
    """Compare profits of two platforms.

    Note: Will need logic to bail gracefully if more than two platforms selected.
    """
    df = df.copy()

    ss_profits = df["profits_ss"]
    gp_profits = df["profits_gp"]
    x_values = df["user_levels"]
    diffs = pd.Series(
        [p_gp - p_ss for p_gp, p_ss in zip(df["profits_gp"], df["profits_ss"])]
    )
    pos_diffs = diffs.where(diffs > 0, other=np.nan)
    neg_diffs = diffs.where(diffs < 0, other=np.nan)
    zero_diffs = diffs.where(diffs == 0, other=np.nan)

    plt.style.use(["seaborn-v0_8-whitegrid", "charts/nlc_style.mplstyle"])
    fig, ax = plt.subplots()

    # Set aspect ratio.
    width = fig.get_size_inches()[0]
    height = width / config.aspect_ratio
    fig.set_size_inches(width, height)

    # Define horizontal placement of all line labels.
    label_pos_x = x_values.iloc[-1] + 0.01 * config.max_subs


    # df.cum_profit.where(df.cum_profit.ge(0), np.nan).plot(color='green')
    # df.cum_profit.where(df.cum_profit.lt(0), np.nan).plot(color='red')

    # df["better"] = df["diffs"].where()


    ax.plot(x_values, pos_diffs, color="lightgreen")
    ax.fill_between(x_values, pos_diffs, where=pos_diffs > 0, interpolate=True, color="lightgreen", alpha=0.3)
    ax.plot(x_values, neg_diffs, color="salmon")
    ax.fill_between(x_values, neg_diffs, where=neg_diffs < 0, interpolate=True, color="salmon", alpha=0.3)
    ax.plot(x_values, zero_diffs, color="black")

    # # Add Substack data.
    # if config.show_ss:
    #     ax.plot(x_values, ss_profits, color=config.ss_color)
    #     label_pos_y = ss_profits.iloc[-1] - 0.005 * ax.get_ylim()[1]
    #     ax.annotate(
    #         "Substack",
    #         (label_pos_x, label_pos_y),
    #         color=config.ss_color,
    #         fontsize=config.fs_brand_label,
    #     )

    # # Add Ghost data.
    # if config.show_gp:
    #     ax.plot(x_values, gp_profits, color=config.gp_color)
    #     label_pos_y = gp_profits.iloc[-1] - 0.01 * ax.get_ylim()[1]
    #     ax.annotate(
    #         "Ghost Pro",
    #         (label_pos_x, label_pos_y),
    #         color=config.gp_color,
    #         fontsize=config.fs_brand_label,
    #     )

    # ax.set_xlim(left=0)
    # ax.set_ylim(bottom=0)
    # ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    # ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))

    ax.set_title("Ghost Pro profit vs Substack profit", pad=config.title_pad, x=-0.1)
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Difference in profit")

    return fig

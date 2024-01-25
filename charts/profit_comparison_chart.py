from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def get_plot(config, df):
    """Compare profits of two platforms.

    Note: Will need logic to bail gracefully if more than two platforms selected.
    """
    # Calculate the comparisons.
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

    ax.plot(x_values, pos_diffs, color="lightgreen")
    ax.fill_between(x_values, pos_diffs, where=pos_diffs > 0, interpolate=True, color="lightgreen", alpha=0.3)

    ax.plot(x_values, neg_diffs, color="salmon")
    ax.fill_between(x_values, neg_diffs, where=neg_diffs < 0, interpolate=True, color="salmon", alpha=0.3)

    ax.plot(x_values, zero_diffs, color="black")

    ax.set_title("Ghost Pro profit vs Substack profit", pad=config.title_pad, x=-0.1)
    ax.set_xlabel("Number of subscribers")
    ax.set_ylabel("Difference in profit")

    return fig

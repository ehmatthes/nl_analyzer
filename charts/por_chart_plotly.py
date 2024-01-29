import plotly.graph_objects as go
import pandas as pd

import streamlit as st


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""
    title = "Annual cost as percent of revenue"
    labels = {"x": "Number of subscribers", "y": "Percent of revenue"}

    # Won't have data if there's no revenue.
    nonzero_revenue = bool(sum(df["revenues"]))

    # Define each trace. Include names for hover data.
    trace_gp = go.Scatter(
        x=df["user_levels"],
        y=df["percent_rev_gp"],
        mode="lines",
        name="Ghost Pro",
        line=dict(color=nl_config.gp_color),
    )
    trace_bd = go.Scatter(
        x=df["user_levels"],
        y=df["percent_rev_bd"],
        mode="lines",
        name="Buttondown",
        line=dict(color=nl_config.bd_color),
    )
    trace_bh = go.Scatter(
        x=df["user_levels"],
        y=df["percent_rev_bh"],
        mode="lines",
        name="beehiiv",
        line=dict(color=nl_config.bh_color),
    )
    trace_ss = go.Scatter(
        x=df["user_levels"],
        y=df["percent_rev_ss"],
        mode="lines",
        name="Substack",
        line=dict(color=nl_config.ss_color),
    )

    # Create the figure and add the traces
    fig = go.Figure()

    if nl_config.show_gp and nonzero_revenue:
        fig.add_trace(trace_gp)
    if nl_config.show_bd and nonzero_revenue:
        fig.add_trace(trace_bd)
    if nl_config.show_bh and nonzero_revenue:
        fig.add_trace(trace_bh)
    if nl_config.show_ss and nonzero_revenue:
        fig.add_trace(trace_ss)

    # Label lines.
    for col, name, color in [
        ("percent_rev_gp", "Ghost Pro", nl_config.ss_color),
        ("percent_rev_bd", "Buttondown", nl_config.bd_color),
        ("percent_rev_bh", "beehiiv", nl_config.bh_color),
        ("percent_rev_ss", "Substack", nl_config.ss_color),
    ]:
        fig.add_annotation(
            x=df["user_levels"].iloc[-1],
            y=df[col].iloc[-1],
            text=name,
            showarrow=False,
            xanchor="left",
            xshift=5,
            font=dict(color=color)
        )

    # Limit of y-axis needs to be at least 15%, but shouldn't over-emphasize high values
    # for only the lowest subscriber levels. Use percentage 1/10 of the way through the set
    # of values, so most of each platform's line is visible.
    if nonzero_revenue:
        try:
            y_max = max(0.15, df["percent_rev_gp"][int(0.1 * df["user_levels"].size)])
        except NameError:
            # Temp fix for when Ghost Pro is not selected.
            y_max = 0.15
    else:
        # x_pos = ax.get_xlim()[1] * 0.1
        # y_pos = ax.get_ylim()[1] / 2
        # ax.annotate("No revenue generated.", (x_pos, y_pos), fontsize=16)
        # x_pos = fig.layout.xaxis.range[1] * 0.1
        # y_pos = fig.layout.yaxis.range[1] * 0.5
        # print(x_pos, y_pos)
        # return fig
        y_max = 0.15


    # Update layout with title and axis labels
    fig.update_layout(
        title=title,
        xaxis_title=labels["x"],
        xaxis=dict(
            tickformat=",",
            showgrid=True,
            range=[0, df["user_levels"].iloc[-1]]
        ),
        yaxis_title=labels["y"],
        # yaxis=dict(tickprefix="$", tickformat=","),
        yaxis=dict(
            range=[0, y_max],
        ),
        # xaxis=dict(
        #     range=[0, df["user_levels"].size]
        # ),
        showlegend=False,
    )

    # if nonzero_revenue:
    #     fig.update_layout(
    #         yaxis=dict(
    #             range=[0, y_max],
    #         ),
    #     )

    if not nonzero_revenue:
        fig.add_annotation(
            x=fig.layout.xaxis.range[1] * 0.1,
            y=fig.layout.yaxis.range[1] * 0.5,
            text="No revenue generated.",
            xanchor="left",
            showarrow=False,
            font=dict(
                size=20,
            )
        )

    # my_xlim = fig.layout.xaxis.range
    # print(my_xlim)

    return fig

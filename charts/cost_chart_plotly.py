import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import streamlit as st


def get_plot(nl_config, df):
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost ($)"}

    # fig = px.line(
    #     x=df["user_levels"],
    #     y=df["costs_ss"],
    #     title=title,
    #     labels=labels,
    #     # color=nl_config.ss_color,
    # )
    ss_color = pd.Series(["purple" for _ in df["user_levels"]])

    fig = px.line(
        df,
        x="user_levels",
        y="costs_ss",
        title=title,
        labels=labels,
    )

    # fig.add_trace(go.Line(
    #     x=df["user_levels"],
    #     y=df["costs_gp"],
    # ))

    fig.update_traces(line_color=nl_config.ss_color)

    return fig

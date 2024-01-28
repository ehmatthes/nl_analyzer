import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import streamlit as st


def get_plot(nl_config, df):
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost ($)"}

    ss_color = pd.Series(["purple" for _ in df["user_levels"]])

    fig = px.line(
        df,
        x="user_levels",
        y="costs_ss",
        title=title,
        labels=labels,
    )

    fig.add_trace(
        go.Scatter(
            x=df["user_levels"],
            y=df["costs_gp"],
            mode="lines",
            name="Costs GP",
            line=dict(color=nl_config.gp_color),
        )
    )


    return fig

    fig.update_traces(line_color=nl_config.ss_color)
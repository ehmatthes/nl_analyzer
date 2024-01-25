"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import altair as alt

from pricer import Pricer
from config import Config


# Build sidebar.
config = Config()

# Platforms to include.
st.sidebar.write("**Platforms:**")
config.show_ss = st.sidebar.checkbox("Substack", value=True)
config.show_gp = st.sidebar.checkbox("Ghost Pro", value=True)
st.sidebar.write("---")

# Max number of subscribers.
max_subs_macro = st.sidebar.slider(
    "Number of subscribers", value=10_000, max_value=100_000, step=1_000
)
max_subs_micro = st.sidebar.slider(
    "Number of subscribers (fine tuning)", value=0, max_value=1_000, step=10
)
config.max_subs = max_subs_macro + max_subs_micro

# Paid subscriber ratio.
paid_ratio_macro = st.sidebar.slider(
    "Paid subscriber ratio", value=0.02, max_value=1.0, step=0.001, format="%.3f"
)

paid_ratio_micro = st.sidebar.slider(
    "Paid subscriber ratio (fine tuning)",
    value=0.0,
    max_value=0.1,
    step=0.001,
    format="%.3f",
)
config.paid_ratio = paid_ratio_macro + paid_ratio_micro

# Average annual revenue per paid user.
config.avg_revenue = st.sidebar.slider(
    "Average annual revenue per paid user", value=50, max_value=500, step=1
)

st.sidebar.write("---")

# Summarize settings.
st.sidebar.write(f"**Max subscribers:** {config.max_subs:,}")
st.sidebar.write(f"**Paid ratio:** {config.paid_ratio*100:.1f}%")
st.sidebar.write(f"**Average revenue/ paid user:** ${config.avg_revenue:.2f}")

pricer = Pricer(config)
ss_costs = pricer.df["costs_ss"]
gp_costs = pricer.df["costs_gp"]

# --- Charts ---

ss_color = "#DC6931"
gp_color = "black"

# --- Cost chart ---
base_chart = alt.Chart(pricer.df).encode(
    x=alt.X("user_levels", title="Number of subscribers")
)

cost_chart = alt.layer(
    base_chart.mark_line(color=ss_color).encode(
        y=alt.Y("costs_ss", title="Annual cost")
    ),
    base_chart.mark_line(color=gp_color).encode(y="costs_gp"),
)
cost_chart.title = "Annual cost of hosting a newsletter"

ss_annotation = (
    alt.Chart(pricer.df)
    .mark_text(
        align="left",
        baseline="middle",
        fontSize=14,
    )
    .encode(
        x=alt.X("user_levels:Q", aggregate="max"),
        y=alt.Y("costs_ss:Q", aggregate="max"),
        text=alt.value("- Substack"),
    )
)

gp_annotation = (
    alt.Chart(pricer.df)
    .mark_text(
        align="left",
        baseline="middle",
        fontSize=14,
    )
    .encode(
        x=alt.X("user_levels:Q", aggregate="max"),
        y=alt.Y("costs_gp:Q", aggregate="max"),
        text=alt.value("- Ghost Pro"),
    )
)

final_chart = alt.layer(cost_chart, ss_annotation, gp_annotation)

st.altair_chart(final_chart, use_container_width=True)


"---"

# --- Percent of revenue chart
nonzero_revenue = bool(sum(pricer.df["revenues"]))
df_por = pricer.df.copy()

if nonzero_revenue:
    try:
        y_max = max(0.15, gp_percentages[int(0.1 * len(gp_percentages))])
    except NameError:
        # Temp fix for when Ghost Pro is not selected.
        y_max = 0.2
else:
    y_max = 0


df_por["percent_rev_ss"] = (
    df_por["percent_rev_ss"].clip(upper=y_max).where(df_por["percent_rev_ss"] <= y_max)
)
df_por["percent_rev_gp"] = (
    df_por["percent_rev_gp"].clip(upper=y_max).where(df_por["percent_rev_gp"] <= y_max)
)

base_chart = alt.Chart(df_por).encode(
    x=alt.X("user_levels", title="Number of subscribers")
)

por_chart = alt.layer(
    base_chart.mark_line(color=ss_color).encode(
        # y=alt.Y('percent_rev_ss', title="Percent of revenue", scale=alt.Scale(domain=[0, y_max]))),
        # y=alt.Y('percent_rev_ss', title="Percent of revenue")), # works
        y=alt.Y(
            "percent_rev_ss",
            title="Percent of revenue",
            scale=alt.Scale(domain=[0, y_max]),
        )
    ),
    base_chart.mark_line(color=gp_color).encode(y="percent_rev_gp"),
)
por_chart.title = "Annual cost as percent of revenue"

ss_annotation = (
    alt.Chart(df_por)
    .mark_text(
        align="left",
        baseline="middle",
        fontSize=14,
    )
    .encode(
        x=alt.X("user_levels:Q", aggregate="max"),
        y=alt.Y(
            "percent_rev_ss:Q", aggregate="max", scale=alt.Scale(domain=[0, y_max])
        ),
        text=alt.value("- Substack"),
    )
)

gp_annotation = (
    alt.Chart(df_por)
    .mark_text(
        align="left",
        baseline="middle",
        fontSize=14,
    )
    .encode(
        x=alt.X("user_levels:Q", aggregate="max"),
        y=alt.Y(
            "percent_rev_gp:Q", aggregate="max", scale=alt.Scale(domain=[0, y_max])
        ),
        text=alt.value("- Ghost Pro"),
    )
)

empty_annotation = (
    alt.Chart(df_por)
    .mark_text(
        align="left",
        baseline="middle",
        fontSize=16,
        dx=10,
        dy=100,
    )
    .encode(
        x=alt.X(value=0),
        y=alt.Y(value=0),
        text=alt.value("No revenue generated"),
    )
)

if nonzero_revenue:
    final_por_chart = alt.layer(por_chart, ss_annotation, gp_annotation)
else:
    final_por_chart = alt.layer(por_chart, empty_annotation)

st.altair_chart(final_por_chart, use_container_width=True)

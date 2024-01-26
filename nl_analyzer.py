"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import matplotlib.pyplot as plt

from pricer import Pricer
from config import Config

from charts import cost_chart, por_chart, profit_chart, profit_comparison_chart


# --- Sidebar ---

config = Config()

st.sidebar.write("---")

# Max number of subscribers.
max_subs_macro = st.sidebar.slider(
    "Number of subscribers", value=10_000, max_value=100_000, step=1_000
)
max_subs_micro = st.sidebar.slider(
    "Number of subscribers (fine tuning)", value=0, max_value=1_000, step=10
)
config.max_subs = max_subs_macro + max_subs_micro


st.sidebar.write("---")

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

st.sidebar.write("---")

# Average annual revenue per paid user.
config.avg_revenue = st.sidebar.slider(
    "Average annual revenue per paid user", value=50, max_value=500, step=1
)

st.sidebar.write("---")

config.show_exp_features = st.sidebar.checkbox(
    "Show experimental features", value=False
)

# --- Main section ---

# --- Summary of settings

st.write("#### Settings in use:")
st.write(
    f"Up to **{config.max_subs:,}** subscribers, with a paid ratio of **{config.paid_ratio*100:.1f}%**, and an average annual revenue of **${config.avg_revenue:.2f}** per paid subscriber."
)

# Platforms to include.
cols = st.columns(4)
with cols[0]:
    config.show_ss = st.checkbox("Substack", value=True)
with cols[1]:
    config.show_gp = st.checkbox("Ghost Pro", value=True)
with cols[2]:
    config.show_bh = st.checkbox("beehiiv", value=True)
with cols[3]:
    config.show_bd = st.checkbox("Buttondown", value=True)

st.write("---")

# --- Charts ---

if config.max_subs == 0:
    st.write("Number of subscribers must be more than 0.")
    st.stop()

pricer = Pricer(config)

# Get chart, and then resize it based on streamlit's work.
cost_fig = cost_chart.get_plot(config, pricer.df)
st.pyplot(cost_fig)


"---"

# Percent of revenue chart.
por_fig = por_chart.get_chart(config, pricer.df)
st.pyplot(por_fig)

"---"

# Profit chart.
profit_fig = profit_chart.get_plot(config, pricer.df)
st.pyplot(profit_fig)

# Profit comparison chart.
if config.show_exp_features:
    pc_fig = profit_comparison_chart.get_plot(config, pricer.df)
    st.pyplot(pc_fig)

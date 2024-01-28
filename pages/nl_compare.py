"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import matplotlib.pyplot as plt

from pricer import Pricer
from config import Config

from charts import cost_chart, por_chart, profit_chart, profit_comparison_chart


# Suppress matplotlib warning about ticks.
import warnings

warnings.filterwarnings("ignore", message=".*set_ticklabels().*")

# Streamlit config
st.set_page_config(layout="wide")

# --- Sidebar ---

config = Config()
st.sidebar.title("Settings")

st.sidebar.write("---")

# Max number of subscribers.
st.sidebar.write("*How many subscribers will you need to support?*")
max_subs_macro = st.sidebar.slider(
    "Number of subscribers",
    value=10_000,
    max_value=100_000,
    step=1_000,
    label_visibility="collapsed",
)
max_subs_micro = st.sidebar.slider(
    "(fine adjustment)", value=0, max_value=1_000, step=10
)
config.max_subs = max_subs_macro + max_subs_micro


st.sidebar.write("---")

# Paid subscriber ratio.
st.sidebar.write("*What percent of your subscribers have a paid subscription?*")
paid_ratio_macro = st.sidebar.slider(
    "Ratio of paid subscribers",
    value=2.0,
    max_value=100.0,
    step=0.1,
    format="%.1f%%",
    label_visibility="collapsed",
)

paid_ratio_micro = st.sidebar.slider(
    "(fine adjustment)",
    value=0.0,
    max_value=10.0,
    step=0.1,
    format="%.1f%%",
)
config.paid_ratio = round((paid_ratio_macro + paid_ratio_micro) / 100.0, 3)

st.sidebar.write("---")

# Average annual revenue per paid user.
st.sidebar.write("*What is your average annual revenue per paid subscriber?*")
config.avg_revenue = st.sidebar.slider(
    "Avergae annual revenue per paid subscriber",
    value=50,
    max_value=500,
    step=1,
    label_visibility="collapsed",
    format="$%d",
)

st.sidebar.write("---")

config.show_exp_features = st.sidebar.checkbox(
    "Show experimental features", value=False
)

# --- Main section ---

if st.button("Home"):
    st.switch_page("nl_analyzer.py")

# --- Summary of settings
st.write("#### Settings in use:")
st.write(
    f"Up to **{config.max_subs:,}** subscribers, with a paid ratio of **{config.paid_ratio*100}%**, and an average annual revenue of **${config.avg_revenue:.2f}** per paid subscriber."
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

# --- Charts ---

if config.max_subs == 0:
    st.error("Number of subscribers must be more than 0.")
    st.stop()

pricer = Pricer(config)

# Cost chart
cost_fig = cost_chart.get_plot(config, pricer.df)
with st.expander("Annual cost", expanded=True):
    st.pyplot(cost_fig)


# Percent of revenue chart
por_fig = por_chart.get_chart(config, pricer.df)
with st.expander("Annual cost as percent of revenue", expanded=True):
    st.pyplot(por_fig)


# Profit chart
profit_fig = profit_chart.get_plot(config, pricer.df)
with st.expander("Annual profit", expanded=True):
    st.pyplot(profit_fig)

# Profit comparison chart.
if config.show_exp_features:
    pc_fig = profit_comparison_chart.get_plot(config, pricer.df)
    st.pyplot(pc_fig)

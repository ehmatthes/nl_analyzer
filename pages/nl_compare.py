"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import matplotlib.pyplot as plt

from pricer import Pricer
from nl_config import NLConfig

from charts import cost_chart, por_chart, profit_chart, profit_comparison_chart


# Suppress matplotlib warning about ticks.
import warnings

warnings.filterwarnings("ignore", message=".*set_ticklabels().*")

# Streamlit config
st.set_page_config(layout="wide")

# --- Sidebar ---

nl_config = NLConfig()
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
help_micro_subs = """
To focus on a smaller number of subscribers, move the main slider to zero and then adjust this slider. The app will combine the values from each slider.
"""
max_subs_micro = st.sidebar.slider(
    "(fine adjustment)", value=0, max_value=1_000, step=10, help=help_micro_subs
)
nl_config.max_subs = max_subs_macro + max_subs_micro


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
help_micro_pr = """
To focus on a smaller percentage, move the main slider to zero and then adjust this slider. The app will combine the values from each slider.
"""
paid_ratio_micro = st.sidebar.slider(
    "(fine adjustment)",
    value=0.0,
    max_value=10.0,
    step=0.1,
    format="%.1f%%",
    help=help_micro_pr,
)
nl_config.paid_ratio = round((paid_ratio_macro + paid_ratio_micro) / 100.0, 3)

st.sidebar.write("---")

# Average annual revenue per paid user.
st.sidebar.write("*What is your average annual revenue per paid subscriber?*")
help_rev_paid = """
Remember to take into account discounts, and differences between monthly and annual plans.
"""
nl_config.avg_revenue = st.sidebar.slider(
    "Avergae annual revenue per paid subscriber",
    value=50,
    max_value=500,
    step=1,
    label_visibility="collapsed",
    format="$%d",
    help=help_rev_paid,
)

st.sidebar.write("---")

nl_config.show_exp_features = st.sidebar.checkbox(
    "Show experimental features", value=False
)

# --- Main section ---

if st.button("Home", type="primary"):
    st.switch_page("nl_analyzer.py")

# --- Summary of settings
st.write("#### Settings in use:")
st.write(
    f"Up to **{nl_config.max_subs:,}** subscribers, with a paid ratio of **{nl_config.paid_ratio*100}%**, and an average annual revenue of **${nl_config.avg_revenue:.2f}** per paid subscriber."
)

# Platforms to include.
help_ss = """
Remember that Substack is not free if you have paid subscribers. It might *seem* free because you never pay them directly, but they keep 10% of the revenue you generate.
"""
cols = st.columns(4)
with cols[0]:
    nl_config.show_gp = st.checkbox("Ghost Pro", value=True)
with cols[1]:
    nl_config.show_bd = st.checkbox("Buttondown", value=True)
with cols[2]:
    nl_config.show_bh = st.checkbox("beehiiv", value=True)
with cols[3]:
    nl_config.show_ss = st.checkbox("Substack", value=True, help=help_ss)


# --- Charts ---

if nl_config.max_subs == 0:
    st.error("Number of subscribers must be more than 0.")
    st.stop()

pricer = Pricer(nl_config)

# Cost chart
cost_fig = cost_chart.get_plot(nl_config, pricer.df)
with st.expander("Annual cost", expanded=True):
    st.pyplot(cost_fig)


# Percent of revenue chart
por_fig = por_chart.get_chart(nl_config, pricer.df)
with st.expander("Annual cost as percent of revenue", expanded=True):
    st.pyplot(por_fig)


# Profit chart
msg_profit = """
"Profit" here refers to your overall revenue, minus the platform's fees and/or percentage. This does not include payment processing fees, and any other costs associated with hosting.
"""
profit_fig = profit_chart.get_plot(nl_config, pricer.df)
with st.expander("Annual profit*", expanded=True):
    st.pyplot(profit_fig)
    st.info(msg_profit)

# Profit comparison chart.
if nl_config.show_exp_features:
    pc_fig = profit_comparison_chart.get_plot(nl_config, pricer.df)
    with st.expander("Profit comparison", expanded=True):
        st.pyplot(pc_fig)

st.write("---")

msg_data_src = """
##### Data sources

- Ghost Pro [pricing page](https://ghost.org/pricing/)
- Buttondown [pricing page](https://buttondown.email/pricing)
- beehiiv [pricing page](https://www.beehiiv.com/pricing)
- Substack [pricing page](https://substack.com/going-paid)
"""
st.info(msg_data_src)

st.write("---")

if st.button("Home", type="primary", key="home_2"):
    st.switch_page("nl_analyzer.py")
"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st

from pricer import Pricer
from nl_config import NLConfig

from charts import cost_chart, por_chart, profit_chart
from utils import ui_utils


# Streamlit config
st.set_page_config(layout="wide")

# --- Sidebar ---

nl_config = NLConfig()
st.sidebar.title("Settings")

st.sidebar.write("---")

# Max number of subscribers.
st.sidebar.write("*How many subscribers will you need to support?*")
nl_config.max_subs = int(
    st.sidebar.select_slider(
        "Number of subscribers",
        options=ui_utils.max_subs_options(),
        value=10_000,
        format_func=ui_utils.format_max_subs,
        label_visibility="collapsed",
    )
)

# Paid subscriber ratio.
st.sidebar.write("*What percent of your subscribers have a paid subscription?*")
nl_config.paid_ratio = st.sidebar.select_slider(
    "Ratio of paid subscribers",
    options=ui_utils.paid_ratio_options(),
    value=0.025,
    format_func=ui_utils.format_paid_ratio,
    label_visibility="collapsed",
)

# Average annual revenue per paid user.
st.sidebar.write("*What's your average annual revenue per paid subscriber?**")
nl_config.avg_revenue = st.sidebar.select_slider(
    "Avergae annual revenue per paid subscriber",
    options=ui_utils.avg_revenue_options(),
    value=50,
    format_func=ui_utils.format_avg_revenue,
    label_visibility="collapsed",
)

st.sidebar.write("---")

st.sidebar.write(
    "**Remember to take into account discounts, and differences between monthly and annual plans.*"
)

nl_config.show_exp_features = st.sidebar.toggle(
    "Show experimental features", value=False
)

# --- Main section ---

if st.button("Home", type="primary"):
    st.switch_page("nl_analyzer.py")

# --- Summary of settings
st.write("#### Settings in use:")
st.write(
    f"Up to **{nl_config.max_subs:,}** subscribers, with a paid ratio of **{round(nl_config.paid_ratio*100, 2)}%**, and an average annual revenue of **${nl_config.avg_revenue:.2f}** per paid subscriber."
)

# Platforms to include.
help_ss = """
Remember that Substack is not free if you have paid subscribers. It might *seem* free because you never pay them directly, but they keep 10% of the revenue you generate.
"""
cols = st.columns(3)
with cols[0]:
    nl_config.gp_config.show = st.toggle("Ghost Pro", value=True)
with cols[1]:
    nl_config.bd_config.show = st.toggle("Buttondown", value=False)
with cols[2]:
    nl_config.bh_config.show = st.toggle("beehiiv", value=False)

cols = st.columns(3)
with cols[0]:
    nl_config.ss_config.show = st.toggle("Substack", value=True, help=help_ss)
with cols[1]:
    nl_config.ck_config.show = st.toggle("ConvertKit", value=False)


# --- Charts ---

if nl_config.max_subs == 0:
    st.error("Number of subscribers must be greater than 0.")
    st.stop()

pricer = Pricer(nl_config)

# Cost chart.
cost_fig = cost_chart.get_plot(nl_config, pricer.df)
with st.expander("Annual cost", expanded=True):
    st.plotly_chart(cost_fig)


# Percent of revenue chart.
msg_por = """
For lower revenue amounts, the cost as a percent of revenue can be extremely high. The height of the chart is calculated in a way that tries to avoid over-emphasizing these outlier values.
"""
por_fig = por_chart.get_plot(nl_config, pricer.df)
with st.expander("Annual cost as percent of revenue", expanded=True):
    st.plotly_chart(por_fig)
    st.info(msg_por)

# Profit chart.
msg_profit = """
"Profit" here refers to your overall revenue, minus the platform's fees and/or percentage. This does not include payment processing fees, and any other costs associated with hosting.
"""
profit_fig = profit_chart.get_plot(nl_config, pricer.df)
with st.expander("Annual profit*", expanded=True):
    st.plotly_chart(profit_fig)
    st.info(msg_profit)


st.write("---")

msg_data_src = """
##### Data sources

- Ghost Pro [pricing page](https://ghost.org/pricing/)
- Buttondown [pricing page](https://buttondown.email/pricing)
- beehiiv [pricing page](https://www.beehiiv.com/pricing)
- Substack [pricing page](https://substack.com/going-paid)
- ConvertKit [pricing page](https://convertkit.com/pricing)
"""
st.info(msg_data_src)

st.write("---")

if st.button("Home", type="primary", key="home_2"):
    st.switch_page("nl_analyzer.py")

if nl_config.show_exp_features:
    st.write("---")
    st.write("##### Metrics")

    df_size_kb = round(pricer.df.memory_usage(deep=True).sum() / 1_000, 0)
    st.write(f"Dataframe size (df): {df_size_kb}kB")

"""Compare annual costs of various newsletter platforms."""

import sys

import streamlit as st
import matplotlib.pyplot as plt

from pricer import Pricer


# Build sidebar.
config = {}

# Platforms to include.
st.sidebar.write("**Platforms:**")
config["show_ss"] = st.sidebar.checkbox("Substack", value=True)
config["show_gp"] = st.sidebar.checkbox("Ghost Pro", value=True)
st.sidebar.write("---")

# Max number of subscribers.
max_subs_macro = st.sidebar.slider(
    "Number of subscribers", value=10_000, max_value=100_000, step=1_000
)
max_subs_micro = st.sidebar.slider(
    "Number of subscribers (fine tuning)", value=0, max_value=1_000, step=10
)
config["max_subs"] = max_subs_macro + max_subs_micro

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
config["paid_ratio"] = paid_ratio_macro + paid_ratio_micro

# Average annual revenue per paid user.
config["avg_revenue"] = st.sidebar.slider(
    "Average annual revenue per paid user", value=50, max_value=500, step=1
)

st.sidebar.write("---")

# Summarize settings.
st.sidebar.write(f"**Max subscribers:** {config['max_subs']:,}")
st.sidebar.write(f"**Paid ratio:** {config['paid_ratio']*100:.1f}%")
st.sidebar.write(f"**Average revenue/ paid user:** ${config['avg_revenue']:.2f}")


pricer = Pricer(config)
ss_costs = pricer.get_costs_substack()
gp_costs = pricer.get_costs_ghostpro()

# Make cost chart.
x_values = range(0, pricer.max_subs, 10)
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()

# Define horizontal placement of all line labels.
label_pos_x = x_values[-1] + 0.01 * pricer.max_subs

# Add Substack data.
if config["show_ss"]:
    ax.plot(x_values, ss_costs)
    label_pos_y = ss_costs[-1] - 0.005 * ax.get_ylim()[1]
    ax.annotate("Substack", (label_pos_x, label_pos_y))

# Add Ghost data.
if config["show_gp"]:
    ax.plot(x_values, gp_costs)
    label_pos_y = gp_costs[-1] - 0.01 * ax.get_ylim()[1]
    ax.annotate("Ghost Pro", (label_pos_x, label_pos_y))

ax.set_title("Annual cost of hosting a newsletter")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Annual cost")

fig

"---"

# Make percentage chart.
fig, ax = plt.subplots()

fill_plot = bool(sum(pricer.df["revenues"]))

if config["show_ss"] and fill_plot:
    ss_percentages = pricer.get_percentages_substack()
    ax.plot(x_values, ss_percentages)
    label_pos_y = ss_percentages[-1] - 0.02 * ax.get_ylim()[1]
    ax.annotate("Substack", (label_pos_x, label_pos_y))

if config["show_gp"] and fill_plot:
    gp_percentages = pricer.get_percentages_ghostpro()
    ax.plot(x_values, gp_percentages)
    label_pos_y = gp_percentages[-1] - 0.0002 * ax.get_ylim()[1]
    ax.annotate("Ghost Pro", (label_pos_x, label_pos_y))

# Limit of y-axis needs to be at least 15%, but shouldn't over-emphasize high values
# for only the lowest subscriber levels. Use percentage 1/10 of the way through the set
# of values, so most of each platform's line is visible.
if fill_plot:
    try:
        y_max = max(0.15, gp_percentages[int(0.1 * len(gp_percentages))])
    except NameError:
        # Temp fix for when Ghost Pro is not selected.
        y_max = 0.2
    ax.axis([0, 1.05 * pricer.max_subs, 0, y_max])
    y_vals = ax.get_yticks()
    ax.set_yticklabels(["{:,.1%}".format(y_val) for y_val in y_vals])
else:
    x_pos = ax.get_xlim()[1] * 0.1
    y_pos = ax.get_ylim()[1] / 2
    ax.annotate("No revenue generated.", (x_pos, y_pos), fontsize=16)

ax.set_title("Annual cost as percent of revenue")
ax.set_xlabel("Number of subscribers")
ax.set_ylabel("Percent of revenue")

fig

import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""

    # Won't have data if there's no revenue.
    nonzero_revenue = bool(sum(df["revenues"]))

    fig = go.Figure()

    # Add and label trace for each visible platform.
    for platform in nl_config.platforms:
        if not platform.show:
            continue

        # Add trace.
        trace = go.Scatter(
            x=df["user_levels"],
            y=df[(platform.code, "percent_rev")],
            mode="lines",
            name=platform.name,
            line=dict(color=platform.color),
        )
        fig.add_trace(trace)

        # Label trace.
        fig.add_annotation(
            x=df["user_levels"].iloc[-1],
            # y=df[col].iloc[-1],
            y=df[(platform.code, "percent_rev")].iloc[-1],
            text=platform.name,
            showarrow=False,
            xanchor="left",
            xshift=5,
            font=dict(color=platform.color),
        )

    # Limit of y-axis needs to be at least 15%, but shouldn't over-emphasize high values
    # for only the lowest subscriber levels. Use percentage 1/10 of the way through the set
    # of values, so most of each platform's line is visible.
    if nonzero_revenue:
        try:
            y_max = max(0.15, df[("gp", "percent_rev")][int(0.1 * df["user_levels"].size)])
        except NameError:
            # Temp fix for when Ghost Pro is not selected.
            y_max = 0.15
    else:
        y_max = 0.15

    # Update layout with title and axis labels
    title = "Annual cost as percent of revenue"
    labels = {"x": "Number of subscribers", "y": "Percent of revenue"}
    fig.update_layout(
        title=title,
        xaxis_title=labels["x"],
        xaxis=dict(
            tickformat=",",
            showgrid=True,
        ),
        yaxis_title=labels["y"],
        yaxis=dict(
            range=[0, y_max],
            tickformat=".0%",
        ),
        showlegend=False,
    )

    if not nonzero_revenue:
        # Empty chart. Set consistent bounds, then show appropriate message.
        fig.update_layout(
            xaxis=dict(
                range=[0, df["user_levels"].iloc[-1]],
            ),
        )

        fig.add_annotation(
            x=fig.layout.xaxis.range[1] * 0.1,
            y=fig.layout.yaxis.range[1] * 0.5,
            text="No revenue generated.",
            xanchor="left",
            showarrow=False,
            font=dict(
                size=20,
            ),
        )

    return fig

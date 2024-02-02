import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""

    # Won't have data if there's no revenue.
    nonzero_revenue = bool(sum(df["revenues"]))

    fig = go.Figure()

    # Add and label trace for each visible platform.
    for platform in nl_config.visible_platforms:
        # Add trace.
        trace = go.Scatter(
            x=df["user_levels"],
            y=df[(platform.code, "profits")],
            mode="lines",
            name=platform.name,
            line=dict(color=platform.color),
        )
        fig.add_trace(trace)

        # Label trace.
        fig.add_annotation(
            x=df["user_levels"].iloc[-1],
            y=df[(platform.code, "profits")].iloc[-1],
            text=platform.name,
            showarrow=False,
            xanchor="left",
            xshift=5,
            font=dict(color=platform.color),
        )

    # Update layout with title and axis labels
    title = "Annual profit"
    labels = {"x": "Number of subscribers", "y": "Annual profit"}
    fig.update_layout(
        title=title,
        xaxis_title=labels["x"],
        xaxis=dict(
            tickformat=",",
            showgrid=True,
        ),
        yaxis_title=labels["y"],
        yaxis=dict(tickprefix="$", tickformat=","),
        showlegend=False,
    )

    if not nonzero_revenue:
        # Empty chart. Set consistent bounds, then show appropriate message.
        fig.update_layout(
            xaxis=dict(
                range=[0, df["user_levels"].iloc[-1]],
            ),
            yaxis=dict(
                range=[0, 1_000],
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

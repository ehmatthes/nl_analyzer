import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart."""
    fig = go.Figure()

    # Add and label trace for each visible platform.
    for platform in nl_config.platforms:
        if not platform.show:
            continue

        # Add trace.
        fig.add_trace(
            go.Scatter(
                x=df["user_levels"],
                y = df[(platform.code, "costs")],
                mode="lines",
                name=platform.name,
                line=dict(color=platform.color),
            )
        )

        # Label trace.
        fig.add_annotation(
            x=df["user_levels"].iloc[-1],
            y=df[(platform.code, "costs")].iloc[-1],
            text=platform.name,
            showarrow=False,
            xanchor="left",
            xshift=5,
            font=dict(color=platform.color),
        )

    # Update layout.
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost"}

    fig.update_layout(
        title=title,
        xaxis_title=labels["x"],
        xaxis=dict(tickformat=",", showgrid=True),
        yaxis_title=labels["y"],
        yaxis=dict(tickprefix="$", tickformat=","),
        showlegend=False,
    )

    return fig

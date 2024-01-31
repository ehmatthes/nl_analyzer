import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart."""
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost"}

    fig = go.Figure()

    # Add trace for each visible platform.
    for pf, name in nl_config.platform_codes:
        if not getattr(nl_config, f"show_{pf}"):
            continue

        color = getattr(nl_config, f"{pf}_color")
        fig.add_trace(
            go.Scatter(
                x=df["user_levels"],
                y=df[f"costs_{pf}"],
                mode="lines",
                name=name,
                line=dict(color=color),
            )
        )

    # Label lines.
    for code, name in nl_config.platform_codes:
        if not getattr(nl_config, f"show_{code}"):
            continue
        color = getattr(nl_config, f"{code}_color")
        fig.add_annotation(
            x=df["user_levels"].iloc[-1],
            y=df[f"costs_{code}"].iloc[-1],
            text=name,
            showarrow=False,
            xanchor="left",
            xshift=5,
            font=dict(color=color),
        )

    # Update layout with title and axis labels
    fig.update_layout(
        title=title,
        xaxis_title=labels["x"],
        xaxis=dict(tickformat=",", showgrid=True),
        yaxis_title=labels["y"],
        yaxis=dict(tickprefix="$", tickformat=","),
        showlegend=False,
    )

    return fig

import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""
    title = "Annual profit"
    labels = {"x": "Number of subscribers", "y": "Annual profit"}

    # Won't have data if there's no revenue.
    nonzero_revenue = bool(sum(df["revenues"]))

    # Define each trace. Include names for hover data.
    trace_gp = go.Scatter(
        x=df["user_levels"],
        y=df["profits_gp"],
        mode="lines",
        name="Ghost Pro",
        line=dict(color=nl_config.gp_color),
    )
    trace_bd = go.Scatter(
        x=df["user_levels"],
        y=df["profits_bd"],
        mode="lines",
        name="Buttondown",
        line=dict(color=nl_config.bd_color),
    )
    trace_bh = go.Scatter(
        x=df["user_levels"],
        y=df["profits_bh"],
        mode="lines",
        name="beehiiv",
        line=dict(color=nl_config.bh_color),
    )
    trace_ss = go.Scatter(
        x=df["user_levels"],
        y=df["profits_ss"],
        mode="lines",
        name="Substack",
        line=dict(color=nl_config.ss_color),
    )
    trace_ck = go.Scatter(
        x=df["user_levels"],
        y=df["profits_ck"],
        mode="lines",
        name="ConvertKit",
        line=dict(color=nl_config.ck_color),
    )

    # Create the figure and add the traces
    fig = go.Figure()

    if nl_config.show_gp and nonzero_revenue:
        fig.add_trace(trace_gp)
    if nl_config.show_bd and nonzero_revenue:
        fig.add_trace(trace_bd)
    if nl_config.show_bh and nonzero_revenue:
        fig.add_trace(trace_bh)
    if nl_config.show_ss and nonzero_revenue:
        fig.add_trace(trace_ss)

    # Label lines.
    for col, name, color, show in [
        ("profits_gp", "Ghost Pro", nl_config.gp_color, nl_config.show_gp),
        ("profits_bd", "Buttondown", nl_config.bd_color, nl_config.show_bd),
        ("profits_bh", "beehiiv", nl_config.bh_color, nl_config.show_bh),
        ("profits_ss", "Substack", nl_config.ss_color, nl_config.show_ss),
        ("profits_ck", "ConvertKit", nl_config.ck_color, nl_config.show_ck),
    ]:
        if show:
            fig.add_annotation(
                x=df["user_levels"].iloc[-1],
                y=df[col].iloc[-1],
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

import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost"}

    platform_codes = [("gp", "Gost Pro"), ("bd", "Buttondown"), ("bh", "beehiiv"), ("ss", "Substack"), ("ck", "ConvertKit")]

    fig = go.Figure()
    for pf, name in platform_codes:
        # Don't create trace if we're not showing that platform.
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
    for col, name, color, show in [
        ("costs_gp", "Ghost Pro", nl_config.gp_color, nl_config.show_gp),
        ("costs_bd", "Buttondown", nl_config.bd_color, nl_config.show_bd),
        ("costs_bh", "beehiiv", nl_config.bh_color, nl_config.show_bh),
        ("costs_ss", "Substack", nl_config.ss_color, nl_config.show_ss),
        ("costs_ck", "ConvertKit", nl_config.ck_color, nl_config.show_ck),
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


    # for pf, name in [
    #     ("gp")
    # ]




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

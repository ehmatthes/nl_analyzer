import plotly.graph_objects as go


def get_plot(nl_config, df):
    """Generate the cost chart, using Plotly."""
    title = "Annual cost of hosting a newsletter"
    labels = {"x": "Number of subscribers", "y": "Annual cost"}

    # # Define each trace. Include names for hover data.
    # trace_gp = go.Scatter(
    #     x=df["user_levels"],
    #     y=df["costs_gp"],
    #     mode="lines",
    #     name="Ghost Pro",
    #     line=dict(color=nl_config.gp_color),
    # )
    # trace_bd = go.Scatter(
    #     x=df["user_levels"],
    #     y=df["costs_bd"],
    #     mode="lines",
    #     name="Buttondown",
    #     line=dict(color=nl_config.bd_color),
    # )
    # trace_bh = go.Scatter(
    #     x=df["user_levels"],
    #     y=df["costs_bh"],
    #     mode="lines",
    #     name="beehiiv",
    #     line=dict(color=nl_config.bh_color),
    # )
    # trace_ss = go.Scatter(
    #     x=df["user_levels"],
    #     y=df["costs_ss"],
    #     mode="lines",
    #     name="Substack",
    #     line=dict(color=nl_config.ss_color),
    # )
    # trace_ck = go.Scatter(
    #     x=df["user_levels"],
    #     y=df["costs_ck"],
    #     mode="lines",
    #     name="ConvertKit",
    #     line=dict(color=nl_config.ck_color),
    # )

    fig = go.Figure()
    for pf, name in [("gp", "Gost Pro"), ("bd", "Buttondown"), ("bh", "beehiiv"), ("ss", "Substack"), ("ck", "ConvertKit")]:
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




    # Create the figure and add the traces
    # fig = go.Figure()
    # if nl_config.show_gp:
    #     fig.add_trace(trace_gp)
    # if nl_config.show_bd:
    #     fig.add_trace(trace_bd)
    # if nl_config.show_bh:
    #     fig.add_trace(trace_bh)
    # if nl_config.show_ss:
    #     fig.add_trace(trace_ss)
    # if nl_config.show_ck:
    #     fig.add_trace(trace_ck)

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

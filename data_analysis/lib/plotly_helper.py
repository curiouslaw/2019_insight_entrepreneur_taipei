import plotly.graph_objects as go


def add_chart_title(fig: go.Figure, title: str, elevate_line: int = 1, **kwargs) -> None:
    fig.update_layout(
        dict(
            margin={'t': 40 + (elevate_line * 30)},
        )
    )

    y_line = 0.98 + (elevate_line * 0.04)
    y_annotation = y_line

    fig.add_annotation(
        text=title,
        font={'size': 12},
        yanchor='bottom',
        xref='paper', x=0.5, yref='paper', y=y_annotation,
        showarrow=False,
        **kwargs
    )

    fig.add_shape(
        type='line',
        xref='paper', x0=0, x1=1,
        yref='paper', y0=y_line, y1=y_line,
        line=dict(
            width=1
        )
    )


def add_chart_annotation(fig: go.Figure, text: str) -> None:
    fig.add_annotation(text=text,
        xanchor='left', yanchor='bottom',
        xref='paper', x=0, yref='paper', y=1,
        font=dict(
            color='grey',
            size=8
        ),
        showarrow=False
    )

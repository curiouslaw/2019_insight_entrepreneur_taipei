import plotly.graph_objects as go


def add_chart_title(fig: go.Figure, title: str, elevate_line: int = 1,
    title_margin: int = 40, font_size: int = 12, **kwargs) -> None:

    y_line = 0.98 + (elevate_line * 0.04)
    y_annotation = y_line

    fig.add_annotation(
        text=title,
        font={'size': font_size},
        align='left',
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

    if title_margin:
        fig.update_layout(
            dict(
                margin={'t': title_margin + (elevate_line * 30)},
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


def add_chart_bottom_annotation(fig: go.Figure, text: str,
    y_position: float = 0, x_position: float = 0) -> None:

    fig.add_annotation(text=text,
        xanchor='left', yanchor='top',
        xref='paper', x=x_position, yref='paper', y=-y_position,
        font=dict(
            color='grey',
            size=8
        ),
        showarrow=False
    )


def set_layout_size(fig: go.Figure, width: int, height: int,
    hsplit: int = 1, vsplit: int = 1) -> None:
    fig.update_layout(
        dict(
            autosize=False,
            width=width / hsplit,
            height=height / vsplit,
        )
    )

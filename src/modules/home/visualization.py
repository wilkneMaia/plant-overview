
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go


def apply_bar_chart_defaults(fig, xlabel: str, ylabel: str) -> None:
    """
    Aplica configurações padrão para gráficos de barras.

    Args:
        fig: Figura Plotly a ser modificada
        xlabel: Label do eixo X
        ylabel: Label do eixo Y
    """
    fig.update_layout(
        xaxis={
            "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
            "showgrid": False,
            "tickangle": -45,
            "automargin": True,
        },
        yaxis={
            "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
            "gridcolor": "#404040",
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        hovermode="x unified",
    )


def apply_grouped_barchart_defaults(
    fig, xlabel: str, ylabel: str, height: int = 650
) -> None:
    """
    Aplica padrões visuais para gráficos de barras agrupadas.

    Args:
        fig: Figura Plotly
        xlabel: Label eixo X
        ylabel: Label eixo Y
        height: Altura do gráfico
    """
    fig.update_layout(
        xaxis={
            "type": "category",
            "title": {"text": f"<b>{xlabel}</b>", "font": {"size": 14}},
            "tickangle": -45,
        },
        yaxis={"title": {"text": f"<b>{ylabel}</b>", "font": {"size": 14}}},
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        legend={
            "orientation": "h",
            "y": -0.25,
            "title": {"text": "<b>Microinversores Ativos</b>"},
        },
        margin={"t": 100, "b": 100},
        bargap=0.3,
        bargroupgap=0.1,
    )

    fig.update_traces(
        marker_line_width=1,
        marker_line_color="white",
        opacity=0.9,
        textposition="outside",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Ano: %{x}<br>"
            "Produção: %{y:,.2f} kWh<br>"
            "<extra></extra>"
        ),
    )


def create_grouped_barchart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str,
    title: str,
    colors: list[str],
    text_auto: bool = True,
    barmode: str = "group",
) -> go.Figure:
    """
    Cria gráfico de barras agrupadas padronizado com tipagem correta.

    Args:
        data: DataFrame com os dados
        x_col: Nome da coluna para eixo X
        y_col: Nome da coluna para eixo Y
        color_col: Coluna para diferenciação de cores
        title: Título do gráfico
        colors: Lista de cores (obrigatório)
        text_auto: Mostrar valores nas barras (True/False ou string de formatação)
        barmode: Tipo de agrupamento ('group', 'stack', etc.)

    Returns:
        Objeto Figure do Plotly

    Exemplo:
        >>> fig = create_grouped_barchart(df, "Year", "Energy", "Microinversor",
        ...                             "Produção por Ano", ["#00AA00", "#007700"])
    """
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        barmode=barmode,
        title=title,
        color_discrete_sequence=colors,
        text_auto=".2s" if text_auto is True else text_auto,
        category_orders={x_col: sorted(data[x_col].unique())},
        labels={x_col: x_col, y_col: y_col, color_col: color_col},
    )

    return fig


def create_comparison_area_chart(
    data,
    x_col: str,
    y_col: str,
    color_col: str,
    title: str,
    colors: list,
    month_mapping: dict[int, str],
    **kwargs,
) -> go.Figure:
    """
    Cria gráfico de área comparativo padronizado.

    Args:
        data: DataFrame com dados
        x_col: Coluna para eixo X (ex: 'Month')
        y_col: Coluna para eixo Y (ex: 'Energy')
        color_col: Coluna para diferenciação (ex: 'Year')
        title: Título do gráfico
        colors: Lista de cores
        month_mapping: Dicionário de mapeamento de meses

    Returns:
        Figura Plotly configurada
    """
    fig = px.area(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        color_discrete_sequence=colors,
        template="plotly_dark",
        **kwargs,
    )

    return fig


def apply_area_chart_defaults(
    fig: go.Figure, xlabel: str, ylabel: str, month_mapping: dict[int, str]
) -> None:
    """
    Aplica configurações padrão para gráficos de área comparativos.

    Args:
        fig: Figura Plotly
        xlabel: Label do eixo X
        ylabel: Label do eixo Y
        month_mapping: Dicionário de mapeamento de meses
    """
    fig.update_layout(
        xaxis={
            "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
            "tickvals": list(month_mapping.keys()),
            "ticktext": list(month_mapping.values()),
            "tickangle": -45,
            "gridcolor": "rgba(80, 80, 80, 0.3)",
        },
        yaxis={
            "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
            "gridcolor": "rgba(80, 80, 80, 0.3)",
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        hovermode="x unified",
        legend={
            "title": "Ano",
            "orientation": "h",
            "y": -0.2,
            "bgcolor": "rgba(0,0,0,0.3)",
        },
        margin=dict(l=50, r=30, t=80, b=50),
    )

    fig.update_traces(
        opacity=0.5,
        line=dict(width=1),
        hovertemplate=f"<b>Ano %{{color}}:</b> %{{y:,.2f}} kWh<br>{xlabel}: %{{x}}<extra></extra>",
    )


def create_comparison_line_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str,
    title: str,
    colors: list[str],
    month_mapping: dict[int, str],
    **kwargs,
) -> go.Figure:
    """
    Cria gráfico de linhas comparativo padronizado.

    Args:
        data: DataFrame com os dados
        x_col: Coluna para eixo X (ex: 'Month')
        y_col: Coluna para eixo Y (ex: 'Energy')
        color_col: Coluna para diferenciação (ex: 'Year')
        title: Título do gráfico
        colors: Lista de cores
        month_mapping: Dicionário de mapeamento de meses

    Returns:
        Figura Plotly configurada
    """
    return px.line(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        markers=True,
        title=title,
        color_discrete_sequence=colors,
        template="plotly_dark",
        labels={y_col: "Energia Gerada (kWh)"},
        **kwargs,
    )


def apply_line_chart_defaults(
    fig: go.Figure, xlabel: str, ylabel: str, month_mapping: dict[int, str]
) -> None:
    """
    Aplica configurações padrão para gráficos de linhas comparativos.

    Args:
        fig: Figura Plotly
        xlabel: Label do eixo X
        ylabel: Label do eixo Y
        month_mapping: Dicionário de mapeamento de meses
    """
    fig.update_layout(
        xaxis={
            "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
            "tickvals": list(month_mapping.keys()),
            "ticktext": list(month_mapping.values()),
            "tickangle": -45,
            "gridcolor": "rgba(80, 80, 80, 0.3)",
        },
        yaxis={
            "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
            "gridcolor": "rgba(80, 80, 80, 0.3)",
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        hovermode="x unified",
        legend={
            "title": "Ano",
            "orientation": "h",
            "y": -0.2,
            "bgcolor": "rgba(0,0,0,0.3)",
        },
        margin=dict(l=50, r=30, t=80, b=50),
    )

    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=8),
        hovertemplate=f"<b>%{{fullData.name}}:</b> %{{y:,.2f}} kWh<br>{xlabel}: %{{x}}<extra></extra>",
    )


def add_average_lines(
    fig: go.Figure, averages: dict, colors: list[str], x_range: tuple = (1, 12)
) -> None:
    """
    Adiciona linhas de média anual ao gráfico.

    Args:
        fig: Figura Plotly
        averages: Dicionário {ano: média}
        colors: Lista de cores
        x_range: Tuple (x0, x1) para extensão da linha
    """
    for i, (year, avg) in enumerate(averages.items()):
        fig.add_shape(
            type="line",
            x0=x_range[0],
            y0=avg,
            x1=x_range[1],
            y1=avg,
            line=dict(color=colors[i % len(colors)], width=1.5, dash="dash"),
            opacity=0.7,
        )


def add_trend_annotations(
    fig: go.Figure, trends: dict, data: pd.DataFrame, x_pos: int = 12, x_shift: int = 15
) -> None:
    """
    Adiciona anotações de tendência ao gráfico.

    Args:
        fig: Figura Plotly
        trends: Dicionário {ano: (valor_tendência, cor)}
        data: DataFrame com dados originais
        x_pos: Posição X da anotação
        x_shift: Deslocamento horizontal
    """
    for year, (trend_value, color) in trends.items():
        year_data = data[data["Year"] == year]
        fig.add_annotation(
            x=x_pos,
            y=year_data["Energy"].iloc[-1],
            text=f"{'↑' if trend_value > 0 else '↓'} {abs(trend_value):.0f} kWh",
            showarrow=False,
            font=dict(color=color, size=12),
            xshift=x_shift,
        )


def validate_heatmap_input(data: pd.DataFrame) -> None:
    """
    Valida os dados de entrada para o heatmap.

    Args:
        data: DataFrame de entrada

    Raises:
        ValueError: Se os dados forem inválidos
    """
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise ValueError("Dados de entrada inválidos ou DataFrame vazio")


def process_heatmap_years(columns: pd.Index) -> list:
    """
    Processa e valida os anos do heatmap.

    Args:
        columns: Índice com os anos

    Returns:
        Lista de anos convertidos para inteiro

    Raises:
        ValueError: Se nenhum ano válido for encontrado
    """
    years = [int(year) for year in columns if str(year).isdigit()]
    if not years:
        raise ValueError("Nenhum ano válido encontrado nos dados")
    return years


def create_safe_heatmap(
    data_values: list,
    years: list,
    microinverters: list,
    color_scale: list,
    height: int = 600,
) -> px.imshow:
    """
    Cria um heatmap com tratamento seguro de dados.

    Args:
        data_values: Valores da matriz do heatmap
        years: Lista de anos para eixo X
        microinverters: Lista de microinversores para eixo Y
        color_scale: Escala de cores
        height: Altura do gráfico

    Returns:
        Figura Plotly configurada
    """
    return px.imshow(
        data_values,
        labels=dict(x="Ano", y="Microinversor", color="Energia (kWh)"),
        color_continuous_scale=color_scale,
        aspect="auto",
        text_auto=".1f",
        x=years,
        y=microinverters,
    )


def configure_heatmap_layout(
    fig: px.imshow, title: str, height: int, years: list
) -> None:
    """
    Aplica configurações de layout ao heatmap.

    Args:
        fig: Figura Plotly
        title: Título do gráfico
        height: Altura do gráfico
        years: Lista de anos para formatação
    """
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18},
        },
        xaxis_title="Ano",
        yaxis_title="Microinversor",
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        margin=dict(l=100, r=30, t=100, b=50),
    )

    fig.update_xaxes(
        tickvals=list(range(len(years))),
        ticktext=[str(year) for year in years],
        tickangle=0,
    )


def apply_production_bar_style(
    fig: go.Figure,
    data: pd.DataFrame,
    unit: str = "kWh",
    margin: dict | None = None,
    xaxis_title: str = "Ano",  # Novo parâmetro para customização
) -> None:
    """
    Aplica estilo avançado ao gráfico de produção.

    Args:
        fig: Figura Plotly
        data: DataFrame usado no gráfico
        unit: Unidade de medida
        margin: Dicionário com margens personalizadas
        xaxis_title: Título personalizado para o eixo X (padrão: "Ano")
    """
    margin = margin or dict(l=60, r=30, t=90, b=60)

    fig.update_traces(
        marker=dict(line=dict(width=1.5, color="rgba(255,255,255,0.7)"), opacity=0.85),
        hovertemplate=(
            f"<b>{xaxis_title} %{{x}}:</b><br>"  # Atualizado para usar o título personalizado
            f"Produção: %{{y:,.0f}} {unit}<br>"
            "<extra></extra>"
        ),
        texttemplate="%{y:,.0f}",
        textposition="outside",
        textfont=dict(color="white", size=11),
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=margin,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(
            title=xaxis_title,
            tickmode="array",
            tickvals=data["Year"],
            gridcolor="rgba(100,100,100,0.1)",
            title_font=dict(size=14),
            tickangle= -45,
        ),
        yaxis=dict(
            title=f"Produção ({unit})",
            gridcolor="rgba(100,100,100,0.1)",
            zerolinecolor="rgba(100,100,100,0.3)",
            title_font=dict(size=14),
        ),
        hoverlabel=dict(bgcolor="rgba(30,30,30,0.8)", font_size=12),
    )


def create_production_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color_scale: list,
    unit: str = "kWh",
    height: int = 500,
) -> go.Figure:
    """
    Cria gráfico de barras de produção energética padronizado.

    Args:
        data: DataFrame com dados
        x_col: Coluna para eixo X (ex: 'Year')
        y_col: Coluna para eixo Y (ex: 'Energy')
        title: Título principal
        color_scale: Escala de cores gradiente
        unit: Unidade de medida
        height: Altura do gráfico

    Returns:
        Figura Plotly configurada
    """
    return px.bar(
        data,
        x=x_col,
        y=y_col,
        title=title,
        color=y_col,
        color_continuous_scale=color_scale,
        text_auto=True,
        labels={y_col: f"Produção ({unit})", x_col: x_col.replace("_", " ")},
        height=height,
    )

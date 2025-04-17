import plotly.express as px


def criar_grafico_area_empilhada(
    df,
    anos_col,
    microinversores_cols,
    title="Evolução da Produção de Energia por Microinversor",
    subtitle="Análise da produção de energia anual dos microinversores",
):
    """
    Função para criar um gráfico de área empilhada mostrando a evolução da produção de energia ao longo dos anos para cada microinversor.

    Args:
    - df: DataFrame contendo os dados de produção de energia.
    - anos_col: Nome da coluna que contém os anos.
    - microinversores_cols: Lista dos nomes das colunas que representam os microinversores.
    - title: Título do gráfico (opcional).
    - subtitle: Subtítulo do gráfico (opcional).

    Returns:
    - fig: Gráfico de área empilhada gerado.
    """

    # Criando o gráfico de área empilhada
    fig = px.area(
        df,
        x=anos_col,
        y=microinversores_cols,
        title=f"{title}<br><span style='font-size:14px;color:gray'>{subtitle}</span>",
        labels={anos_col: "Ano", "value": "Energia (kWh)", "variable": "Microinversor"},
        template="plotly_dark",
    )

    # Ajustes adicionais no layout
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Energia (kWh)",
        showlegend=True,
        legend_title="Microinversores",
        height=600,  # Altura do gráfico
        margin={"l": 40, "r": 40, "t": 100, "b": 40},  # Ajustando as margens
    )

    # Exibir o gráfico
    fig.show()

    return fig

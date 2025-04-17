import pandas as pd
import plotly.express as px


# Função para criar o gráfico de área empilhada
def criar_grafico_area_empilhada(
    df,
    anos_col,
    microinversores_cols,
    title="Evolução da Produção de Energia por Microinversor",
    subtitle="Análise da produção de energia anual dos microinversores",
):
    fig = px.area(
        df,
        x=anos_col,
        y="Energy",
        color="Microinversor",
        title=f"{title}<br><span style='font-size:14px;color:gray'>{subtitle}</span>",
        labels={
            anos_col: "Ano",
            "Energy": "Energia (kWh)",
            "Microinversor": "Microinversor",
        },
        template="plotly_dark",
    )

    # Ajustes adicionais no layout
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Energia (kWh)",
        showlegend=True,
        legend_title="Microinversores",
        height=600,
        margin={"l": 40, "r": 40, "t": 100, "b": 40},  # Ajustando as margens
    )

    # Exibir o gráfico
    fig.show()

    return fig


def criar_grafico_boxplot(
    df,
    anos_col,
    microinversores_cols,
    title="Variação na Produção de Energia por Microinversor",
    subtitle="Análise da variabilidade da produção de energia dos microinversores ao longo dos anos",
):
    """
    Função para criar um gráfico de boxplot mostrando a variação na produção de energia ao longo dos anos para cada microinversor.

    Args:
    - df: DataFrame contendo os dados de produção de energia.
    - anos_col: Nome da coluna que contém os anos.
    - microinversores_cols: Lista dos nomes das colunas que representam os microinversores.
    - title: Título do gráfico (opcional).
    - subtitle: Subtítulo do gráfico (opcional).

    Returns:
    - fig: Gráfico de boxplot gerado.
    """

    # Reorganizando os dados para o formato longo
    df_melted = pd.melt(
        df,
        id_vars=[anos_col],
        value_vars=microinversores_cols,
        var_name="Microinversor",
        value_name="Energia",
    )

    # Criando o gráfico de boxplot
    fig = px.box(
        df_melted,
        x=anos_col,
        y="Energia",
        color="Microinversor",
        title=f"{title}<br><span style='font-size:14px;color:gray'>{subtitle}</span>",
        labels={
            anos_col: "Ano",
            "Energia": "Energia (kWh)",
            "Microinversor": "Microinversor",
        },
        template="plotly_dark",
    )

    # Ajustes adicionais no layout
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Energia (kWh)",
        showlegend=True,
        legend_title="Microinversores",
        height=600,
        margin={"l": 40, "r": 40, "t": 100, "b": 40},  # Ajustando as margens
    )

    # Exibir o gráfico
    fig.show()

    return fig


def criar_grafico_heatmap_tendencias(
    df,
    anos_col,
    microinversores_cols,
    title="Análise de Tendências na Produção de Energia",
    subtitle="Tendências de crescimento ou queda de energia gerada por microinversores ao longo dos anos",
):
    """
    Função para criar um gráfico de heatmap mostrando a produção de energia ao longo dos anos para cada microinversor,
    destacando tendências de crescimento ou queda de energia.

    Args:
    - df: DataFrame contendo os dados de produção de energia.
    - anos_col: Nome da coluna que contém os anos.
    - microinversores_cols: Lista dos nomes das colunas que representam os microinversores.
    - title: Título do gráfico (opcional).
    - subtitle: Subtítulo do gráfico (opcional).

    Returns:
    - fig: Gráfico de heatmap gerado.
    """

    # Reorganizando os dados para o formato necessário para o heatmap
    df_pivot = df.pivot(index="Microinversor", columns=anos_col, values="Energy")

    # Criando o gráfico de Heatmap
    fig = px.imshow(
        df_pivot,
        labels=dict(x="Ano", y="Microinversor", color="Energia (kWh)"),
        title=f"{title}<br><span style='font-size:14px;color:gray'>{subtitle}</span>",
        color_continuous_scale="Viridis",  # Escala de cores contínuas
        template="plotly_dark",
    )

    # Ajustes adicionais no layout
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Microinversor",
        height=600,
        margin={"l": 40, "r": 40, "t": 100, "b": 40},  # Ajustando as margens
        coloraxis_colorbar=dict(title="Energia (kWh)"),
    )

    # Destacar anos com maior e menor produção
    max_year = df_pivot.max().max()
    min_year = df_pivot.min().min()

    fig.add_annotation(
        x=df_pivot.columns[df_pivot.max(axis=0) == max_year][0],
        y=df_pivot.index[df_pivot.max(axis=1) == max_year][0],
        text="Máximo",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        bgcolor="yellow",
        font=dict(color="black"),
    )

    fig.add_annotation(
        x=df_pivot.columns[df_pivot.min(axis=0) == min_year][0],
        y=df_pivot.index[df_pivot.min(axis=1) == min_year][0],
        text="Mínimo",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=30,
        bgcolor="red",
        font=dict(color="white"),
    )

    # Exibir o gráfico
    fig.show()

    return fig


def criar_grafico_barras_empilhadas(
    df,
    anos_col,
    microinversores_cols,
    title="Contribuição de Microinversores para a Produção de Energia",
    subtitle="Comparação da produção de energia dos microinversores ao longo dos anos",
):
    """
    Função para criar um gráfico de barras empilhadas para mostrar a contribuição de cada microinversor para a produção de energia ao longo dos anos.

    Args:
    - df: DataFrame contendo os dados de produção de energia.
    - anos_col: Nome da coluna que contém os anos.
    - microinversores_cols: Lista dos nomes das colunas que representam os microinversores.
    - title: Título do gráfico (opcional).
    - subtitle: Subtítulo do gráfico (opcional).

    Returns:
    - fig: Gráfico de barras empilhadas gerado.
    """

    # Criando o gráfico de barras empilhadas
    fig = px.bar(
        df,
        x=anos_col,
        y="Energy",
        color="Microinversor",
        title=f"{title}<br><span style='font-size:14px;color:gray'>{subtitle}</span>",
        labels={
            anos_col: "Ano",
            "Energy": "Energia (kWh)",
            "variable": "Microinversor",
        },
        template="plotly_dark",
        text_auto=True,  # Exibe o valor das barras
        color_discrete_sequence=px.colors.qualitative.Set2,
    )  # Define a paleta de cores

    # Ajustes adicionais no layout
    fig.update_layout(
        title_font=dict(
            size=22, color="white"
        ),  # Ajustando o tamanho e a cor do título
        xaxis_title="Ano",
        yaxis_title="Energia (kWh)",
        showlegend=True,
        legend_title="Microinversores",
        height=600,
        margin={"l": 40, "r": 40, "t": 100, "b": 40},  # Ajustando as margens
    )

    # Exibir o gráfico
    fig.show()

    return fig


# Chamando a função para criar o gráfico de barras empilhadas
# criar_grafico_barras_empilhadas(df_grouped, "Year", ["Microinversor"])

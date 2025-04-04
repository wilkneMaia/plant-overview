import pandas as pd
import streamlit as st

from charts.bar_chart import BarChart
from charts.chart_area import AreaChart
from charts.line_chart import LineChart
from config.constants import Colors, FontSettings

from .metrics import (
    aggregate_energy_by_year,
    aggregate_energy_by_year_microinverter,
    calculate_heatmap_height,
    calculate_yearly_averages,
    clean_year_column,
    detect_significant_trends,
    filter_positive_energy,
    get_month_names,
    handle_heatmap_error,
    handle_plot_error,
    prepare_data_for_heatmap,
    prepare_monthly_comparison_data,
    validate_columns,
)
from .visualization import (
    apply_grouped_barchart_defaults,
    create_grouped_barchart,
    create_safe_heatmap,
    process_heatmap_years,
    validate_heatmap_input,
)

# --- Gráficos ---


# Gráficos de energia gerada por ano
def plot_energy_production_by_year(df: pd.DataFrame, unit: str = "kWh") -> None:
    """
    Exibe o total de energia gerada por ano com design aprimorado.

    Args:
        df: DataFrame com dados de produção
        unit: Unidade de medida (padrão: kWh)
    """
    try:
        # Validação e preparação dos dados (mantido em metrics.py)
        validate_columns(df, {"Year", "Energy"})
        yearly_data = aggregate_energy_by_year(df)

        # Criação do gráfico usando funções de visualization.py
        chart = BarChart(
            data=yearly_data,
            x_col="Year",
            y_col="Energy",
            color_scale=Colors.GREEN_SEQUENTIAL,
            theme="dark",
            unit="MWh",
            xaxis_title="Ano",
            yaxis_title="Produção (MWh)",
        )

        # Personalização e exibição
        (
            chart.set_titles(
                title="Produção Energética Anual",
                subtitle="Dados consolidados 2020-2024",
                title_font={"size": 24, "color": "white"},
                subtitle_font={"size": 16, "color": "#CCCCCC"},
            )
            .apply_customizations(line_width=2, opacity=0.9)
            .show()
        )
        # fig = create_production_bar_chart(
        #     data=yearly_data,
        #     x_col="Year",
        #     y_col="Energy",
        #     title="PRODUÇÃO ANUAL DE ENERGIA",
        #     subtitle="Comparativo por Ano",
        #     title_font=FontSettings.TITLE_CHART,
        #     subtitle_font=FontSettings.SUBTITLE_CHART,
        #     color_scale=Colors.GREEN_SEQUENTIAL,
        #     unit=unit,
        # )

        # # Aplicação do estilo
        # apply_production_bar_style(
        #     fig=fig,
        #     data=yearly_data,
        #     unit="MWh",
        #     xaxis_title="ANO",
        #     yaxis_title="Produção: ",
        # )

        # # Exibição otimizada
        # st.plotly_chart(
        #     fig,
        #     use_container_width=True,
        #     config={
        #         "displayModeBar": True,
        #         "modeBarButtonsToRemove": ["toImage", "lasso2d"],
        #         "displaylogo": False,
        #     },
        # )

    except Exception as e:
        handle_plot_error(e, df)


# Gráficos de energia gerada por ano
def plot_energy_trend_by_year(df) -> None:
    """Exibe um gráfico de área comparativo dos meses por ano"""

    try:
        # Processamento de dados
        monthly_data = prepare_monthly_comparison_data(df)
        month_names = get_month_names()
        chart = (
            AreaChart(
                data=monthly_data,
                x_col="Month",
                y_col="Energy",
                color_col="Year",
                colors=Colors.GREEN_DISCRETE,
                period_mapping=month_names,
                theme="dark",
                title="Produção Energética",
                subtitle="Comparativo Anual",
            )
            .set_titles(
                title="Produção Energética Anual", subtitle="Comparativo Mensal por Ano"
            )
            .apply_style(opacity=0.8, line_width=3)
            .add_peak_annotation(
                text="Pico de Produção",
                font_size=14,
                arrowhead=3,
                y_offset=50,  # Ajusta 50 unidades acima do pico
                bgcolor="rgba(200,200,200,0.3)",
                bordercolor="#333333",
            )
        )
        chart.show()

    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e!s}")
        if "monthly_data" in locals():
            st.warning("Dados utilizados na tentativa:")
            st.dataframe(monthly_data.head())


# Grafico de linhas comparativo
def plot_line_comparison_by_year(df) -> None:
    """Exibe gráfico de linhas comparativo com análises de tendência aprimorado"""
    try:
        # Processamento de dados
        monthly_data = prepare_monthly_comparison_data(df)
        month_names = get_month_names()
        calculate_yearly_averages(monthly_data)
        detect_significant_trends(monthly_data)

        # Criação do gráfico usando a nova função
        chart = (
            LineChart(
                data=monthly_data,
                x_col="Month",
                y_col="Energy",
                color_col="Year",
                colors=Colors.GREEN_DISCRETE,
                period_mapping=month_names,
                theme="dark",
            )
            .set_titles(
                title="Análise de Produção", subtitle="Dados mensais consolidados"
            )
            .apply_style(line_width=3, marker_size=10, opacity=0.9)
            .add_peak_annotation()
        )

        chart.show()

        # Elementos adicionais
        # add_average_lines(fig, yearly_averages, Colors.GREEN_DISCRETE)
        # add_trend_annotations(fig, significant_trends, monthly_data)

        # st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        handle_plot_error(e, df)


# Gráfico de barras agrupadas
def plot_microinverter_year_barchart(data):
    """
    Gráfico de barras agrupadas com:
    - Filtro automático de valores zero
    - Legenda dinâmica
    - Ordenação cronológica
    - Tooltips detalhados
    """
    try:
        # Validação e pré-processamento
        validate_columns(data, {"Microinversor", "Year", "Energy"})
        df = clean_year_column(data)
        df = filter_positive_energy(df)
        df_agg = aggregate_energy_by_year_microinverter(df)

        # Adiciona customdata para tooltips
        df_agg["Microinversor"] = df_agg["Microinversor"].astype(str)
        custom_data = df_agg[["Microinversor"]]

        # Construção do gráfico
        fig = create_grouped_barchart(
            data=df_agg,
            x_col="Year",
            y_col="Energy",
            color_col="Microinversor",
            title="<b>Distribuição de Energia por Ano</b><br><sup>Microinversores com produção > 0</sup>",
            colors=Colors.GREEN_DISCRETE,
        )

        # Aplica configurações visuais
        apply_grouped_barchart_defaults(fig, "Ano", "Energia (kWh)")
        fig.update_traces(customdata=custom_data)

        # Adiciona nota explicativa
        fig.add_annotation(
            text="*Barras com valor zero são omitidas automaticamente",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.30,
            showarrow=False,
            font={"size": 10, "color": "gray"},
        )

        return fig

    except Exception as e:
        handle_plot_error(e, data)
        return None


# Gráfico de energia gerada por microinversor
def plot_energy_heatmap_by_microinverter(data):
    """
    Cria um heatmap com anos inteiros no eixo X e melhor legibilidade.
    Versão refatorada usando funções externalizadas.
    """
    try:
        # Validação e processamento
        validate_heatmap_input(data)
        df_agg = prepare_data_for_heatmap(data)
        years = process_heatmap_years(df_agg.columns)

        # Cálculo de altura com fallback
        try:
            height = calculate_heatmap_height(df_agg)
        except Exception as e:
            height = 600
            st.warning(f"Usando altura padrão: {e}")

        # Criação e configuração do heatmap
        fig = create_safe_heatmap(
            data_values=df_agg.values,
            years=years,
            microinverters=df_agg.index.astype(str),
            color_scale=Colors.GREEN_SEQUENTIAL,
            title="Energia por Ano e Microinversor",
            subtitle="Análise de Produção por Microinversor",
            title_font=FontSettings.TITLE_CHART,
            subtitle_font=FontSettings.SUBTITLE_CHART,
            height=height,
        )

        return fig
    except Exception as e:
        handle_heatmap_error(e, data)
        return None

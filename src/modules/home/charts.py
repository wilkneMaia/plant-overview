import pandas as pd
import streamlit as st

from charts.bar_chart import BarChart
from charts.chart_area import AreaChart
from charts.grouped_bar_chart import GroupedBarChart
from charts.line_chart import LineChart
from charts.safe_heatmap_chart import Heatmap
from config.constants import Colors

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
            xaxis_title=None,
            yaxis_title=None,
        )

        # Obter os anos únicos para inserir no subtítulo
        years = sorted(yearly_data["Year"].unique())  # Ordena os anos
        year_range = (
            f"{years[0]}-{years[-1]}" if len(years) > 1 else f"{years[0]}"
        )  # Intervalo de anos

        # Personalização e exibição com subtítulo dinâmico
        (
            chart.set_titles(
                title="Produção Energética Anual",
                subtitle=f"Análise da geração de energia por ano ({year_range}), destacando a variação da produção ao longo dos anos.",
                title_font={"size": 24, "color": "white"},
                subtitle_font={"size": 12, "color": "#CCCCCC"},
            )
            .apply_customizations(line_width=2, opacity=0.9)
            .show()
        )

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

        # Obter os anos únicos para inserir no subtítulo
        years = sorted(monthly_data["Year"].unique())  # Ordena os anos
        year_range = (
            f"{years[0]}-{years[-1]}" if len(years) > 1 else f"{years[0]}"
        )  # Intervalo de anos

        # Criação do gráfico usando a nova função
        chart = (
            LineChart(
                data=monthly_data,
                x_col="Month",
                y_col="Energy",
                color_col="Year",
                colors=Colors.LINE_COLORS,
                period_mapping=month_names,
                theme="dark",
                xlabel=None,
                ylabel=None,
            )
            .set_titles(
                title="Análise de Produção de Energia",
                subtitle=f"Comparação da geração de energia por ano e mês ({year_range}), destacando os picos de produção por ano.",
            )
            .apply_style(line_width=3, marker_size=10, opacity=0.9)
            .add_peaks_per_group()
        )

        chart.show()

    except Exception as e:
        handle_plot_error(e, df)


# Gráfico de barras agrupadas
def plot_microinverter_year_barchart(data):
    """Exibe gráfico de barras agrupadas com anotações de pico e médias"""
    try:
        # Validação e pré-processamento
        validate_columns(data, {"Microinversor", "Year", "Energy"})
        df = clean_year_column(data)
        df = filter_positive_energy(df)
        df_agg = aggregate_energy_by_year_microinverter(df)

        # Adiciona customdata para tooltips
        df_agg["Microinversor"] = df_agg["Microinversor"].astype(str)

        # Dividir os valores de energia por 100 para exibir em MWh
        df_agg["Energy"] = df_agg["Energy"] / 100

        # Obter os anos únicos para inserir no subtítulo
        monthly_data = prepare_monthly_comparison_data(df)
        years = sorted(monthly_data["Year"].unique())  # Ordena os anos
        year_range = (
            f"{years[0]}-{years[-1]}" if len(years) > 1 else f"{years[0]}"
        )  # Intervalo de anos

        # Construção do gráfico
        chart = GroupedBarChart(
            title="Produção Anual por Microinversor",
            subtitle=f"Comparativo da geração de energia entre microinversores nos anos de ({year_range}), com destaque para a média anual consolidada.",
            data=df_agg,
            x_col="Year",
            y_col="Energy",
            color_col="Microinversor",
            colors=Colors.GREEN_DISCRETE,
            theme="dark",
            ylabel=None,
            xlabel=None,
            legend_title="Microinversor",
            height=500,
        )

        fig = chart.fig

        return fig

    except Exception as e:
        handle_plot_error(e, data)
        return None

        # .set_titles(
        #     title="Distribuição de Energia por Ano",
        #     subtitle="Microinversores com produção > 0",
        # )
        # .apply_style(
        #     xaxis_title="Ano",
        #     yaxis_title="Energia (kWh)",
        #     line_width=2,
        #     opacity=0.9,
        # )
        # .add_peak_annotation(
        #     # text="Pico de Produção",
        #     font_size=14,
        #     arrowhead=3,
        #     y_offset=50,
        #     bgcolor="rgba(200,200,200,0.3)",
        #     bordercolor="#333333",
        # )
        # )
        # chart.show()

        # fig = create_grouped_barchart(
        #     data=df_agg,
        #     x_col="Year",
        #     y_col="Energy",
        #     color_col="Microinversor",
        #     title="<b>Distribuição de Energia por Ano</b><br><sup>Microinversores com produção > 0</sup>",
        #     colors=Colors.GREEN_DISCRETE,
        # )

        # # Aplica configurações visuais
        # apply_grouped_barchart_defaults(fig, "Ano", "Energia (kWh)")
        # fig.update_traces(customdata=custom_data)

        # # Adiciona nota explicativa
        # fig.add_annotation(
        #     text="*Barras com valor zero são omitidas automaticamente",
        #     xref="paper",
        #     yref="paper",
        #     x=0.5,
        #     y=-0.30,
        #     showarrow=False,
        #     font={"size": 10, "color": "gray"},
        # )

        # return fig

    # except Exception as e:
    #     handle_plot_error(e, data)
    #     return None


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
            calculate_heatmap_height(df_agg)
        except Exception as e:
            st.warning(f"Usando altura padrão: {e}")

        # Obter os anos únicos para inserir no subtítulo
        monthly_data = prepare_monthly_comparison_data(data)
        years = sorted(monthly_data["Year"].unique())  # Ordena os anos
        year_range = (
            f"{years[0]}-{years[-1]}" if len(years) > 1 else f"{years[0]}"
        )  # Intervalo de anos

        # Criação e configuração do heatmap
        heatmap = Heatmap(
            data_values=df_agg.values.tolist(),
            x_labels=years,
            y_labels=df_agg.index.tolist(),
            color_scale=Colors.GREEN_SEQUENTIAL,
            theme="dark",
            title="Distribuição de Energia por Microinversor ao Longo dos Anos",
            subtitle=f"Análise da produção de energia anual dos microinversores com produção superior a 0 kWh, de ({year_range}).",
            xlabel=None,
            ylabel=None,
            height=450,
            title_font={"size": 24, "color": "white"},
            subtitle_font={"size": 16, "color": "#CCCCCC"},
            margin=dict(l=30, r=145, t=90, b=30),
        )

        # Exibição do heatmap
        fig = heatmap.fig
        return fig

    except Exception as e:
        handle_heatmap_error(e, data)
        return None


def plot_grafico_area_empilhada(data):

    pass

import pandas as pd
import streamlit as st

from config.constants import Colors

from .metrics import (
    aggregate_energy_by_year_microinverter,
    calculate_heatmap_height,
    calculate_yearly_averages,
    clean_year_column,
    detect_significant_trends,
    filter_positive_energy,
    get_month_names,
    handle_plot_error,
    prepare_data_for_heatmap,
    prepare_monthly_comparison_data,
    prepare_year_production_data,
    validate_columns,
)
from .visualization import (
    add_average_lines,
    add_trend_annotations,
    apply_area_chart_defaults,
    apply_grouped_barchart_defaults,
    apply_line_chart_defaults,
    configure_heatmap_layout,
    create_comparison_area_chart,
    create_comparison_line_chart,
    create_custom_bar_chart,
    create_grouped_barchart,
    create_safe_heatmap,
    handle_heatmap_error,
    process_heatmap_years,
    validate_heatmap_input,
)


# --- Gráficos ---
# Gráficos de energia gerada por microinversor
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
            height=height,
        )

        configure_heatmap_layout(
            fig=fig, title="Energia por Ano e Microinversor", height=height, years=years
        )

        return fig

    except Exception as e:
        handle_heatmap_error(e, data)
        return None


# Grafico de linhas comparativo
def plot_line_comparison_by_year(df):
    """Exibe gráfico de linhas comparativo com análises de tendência"""
    try:
        # Processamento de dados
        monthly_comparison = prepare_monthly_comparison_data(df)
        month_names = get_month_names()
        yearly_averages = calculate_yearly_averages(monthly_comparison)
        significant_trends = detect_significant_trends(monthly_comparison)

        # Criação do gráfico base
        fig = create_comparison_line_chart(
            data=monthly_comparison,
            x_col="Month",
            y_col="Energy",
            color_col="Year",
            title="Comparativo de Geração por Mês e Ano",
            colors=Colors.GREEN_DISCRETE,
            month_mapping=month_names,
        )

        # Aplicação de configurações padrão
        apply_line_chart_defaults(
            fig=fig,
            xlabel="Mês",
            ylabel="Energia Gerada (kWh)",
            month_mapping=month_names,
        )

        # Elementos adicionais
        add_average_lines(fig, yearly_averages, Colors.GREEN_DISCRETE)
        add_trend_annotations(fig, significant_trends, monthly_comparison)

        # Personalizações específicas
        fig.update_layout(
            title={
                "text": "Comparativo de Geração por Mês e Ano",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18, "color": "white"},
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        handle_plot_error(e, df)


# Gráficos de energia gerada por ano
def plot_energy_trend_by_year(df):
    """Exibe um gráfico de área comparativo dos meses por ano"""
    try:
        # Processamento de dados
        monthly_comparison = prepare_monthly_comparison_data(df)
        month_names = get_month_names()

        # Criação do gráfico
        fig = create_comparison_area_chart(
            data=monthly_comparison,
            x_col="Month",
            y_col="Energy",
            color_col="Year",
            title="Comparativo de Energia por Mês e Ano",
            colors=Colors.GREEN_DISCRETE,
            month_mapping=month_names,
            labels={"Energy": "Energia Gerada (kWh)"},
        )

        # Aplicação de configurações
        apply_area_chart_defaults(
            fig=fig,
            xlabel="Mês",
            ylabel="Energia Gerada (kWh)",
            month_mapping=month_names,
        )

        # Personalizações específicas
        fig.update_layout(
            title={
                "text": "Comparativo de Energia por Mês e Ano",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18, "color": "white"},
            }
        )

        st.plotly_chart(fig, use_container_width=True)

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
            y=-0.35,
            showarrow=False,
            font={"size": 10, "color": "gray"},
        )

        return fig

    except Exception as e:
        handle_plot_error(e, data)
        return None


# Gráficos de energia gerada por ano
def plot_energy_production_by_year(df: pd.DataFrame) -> None:
    """Exibe o total de energia gerada por ano com cores gradientes"""
    try:
        # Obtém dados processados
        yearly_data, colors = prepare_year_production_data(df)

        # Cria gráfico com funções do módulo de visualização
        fig = create_custom_bar_chart(
            data=yearly_data,
            x_col="Year",
            y_col="Energy",
            title="Produção Anual (kWh)",
            color=colors,
            show_values=True,
            margin=dict(l=60, r=30, t=100, b=70),
        )

        # Configurações específicas deste gráfico
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e!s}")

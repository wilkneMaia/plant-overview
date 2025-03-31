import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from components.charts import (
    plot_area_overlay_by_year,
    plot_total_by_year,
    plot_line_comparison_by_year,
    plot_grouped_bar_comparison,
    create_microinverter_year_heatmap,
    create_microinverter_year_barchart,
)
from components.custom_card import create_card
from config.constants import EconomicFactors, EnergyFactors, Icons, SystemFactors
from utils.helpers import load_icon_as_base64


class HomeView:
    def display(self, data):
        """Exibe um resumo total dos dados de energia"""
        st.title("Dashboard de Energia")

        # Debug: Verifique os dados recebidos
        # st.write("### Pré-visualização dos dados")
        # st.write(data.head(3))

        # Secão dos cards
        st.header("Indicadores de Desempenho")
        col1, col2, col3 = st.columns(3)
        with col1:
            card_total_performance_indicators(data)
        with col2:
            card_revenue_summary(data)
        with col3:
            card_environmental_benefits(data)
        st.write("---")

        # Seção dos gráficos
        st.header("Análise Temporal")
        col1, col2 = st.tabs(["Heatmap", "Barras Agrupadas"])
        with col1:
            plot_total_by_year(data)
            plot_area_overlay_by_year(data)

        with col2:
            plot_grouped_bar_comparison(data)
            plot_line_comparison_by_year(data)

        # Seção dos gráficos
        st.header("Análise Temporal por Microinversor")

        # Verifique se as colunas necessárias existem
        if all(col in data.columns for col in ['Microinversor', 'Year', 'Energy']):
            tab1, tab2 = st.tabs(["Heatmap", "Barras Agrupadas"])

            with tab1:
                fig_heatmap = create_microinverter_year_heatmap(data)
                if fig_heatmap:
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.warning("Não foi possível gerar o heatmap")

            with tab2:
                chart = create_microinverter_year_barchart(data)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
                else:
                    st.warning("Não foi possível gerar o gráfico com os dados fornecidos.")
        else:
            st.error("""
                Dados insuficientes para análise. Verifique se existem as colunas:
                - 'Microinversor'
                - 'Year'
                - 'Energy'
            """)


def card_total_performance_indicators(df: pd.DataFrame) -> None:
    """Exibe indicadores de desempenho da usina com cálculo otimizado e padrões consistentes."""

    # Cálculos principais (otimizados)
    energy_data = _calculate_energy_metrics(df)
    efficiency_metrics = _calculate_efficiency(df, energy_data["total_energy_kwh"])

    # Construção dos cards
    rows_data = [
        _create_metric_row(
            icon=Icons.POWER_MONTH,
            label="Energia este mês:",
            value=energy_data["current_month_mwh"],
            unit="MWh",
        ),
        _create_metric_row(
            icon=Icons.POWER_YEAR,
            label="Energia este ano:",
            value=energy_data["current_year_mwh"],
            unit="MWh",
        ),
        _create_metric_row(
            icon=Icons.POWER_TOTAL,
            label="Energia Total:",
            value=energy_data["total_energy_mwh"],
            unit="MWh",
        ),
        _create_metric_row(
            icon=Icons.STATS,
            label="Desvio Padrão:",
            value=df["Energy"].std(),
            unit="kWh",
        ),
        _create_metric_row(
            icon=Icons.EFFICIENCY,
            label="Eficiência:",
            value=efficiency_metrics["efficiency"],
            unit="%",
        ),
    ]

    components.html(create_card("Desempenho da Usina", rows_data), height=400)


def card_revenue_summary(df: pd.DataFrame) -> None:
    """Exibe resumo de receita com ícones padronizados."""
    # Setup
    # locale.setlocale(locale.LC_ALL, LOCALE_CURRENCY)

    # Validação
    required_columns = {"Energy", "Year", "Month"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Colunas faltando: {required_columns - set(df.columns)}")

    # Cálculos
    total_energy = df["Energy"].sum()
    current_month_energy = _get_current_month_energy(df)

    rows_data = [
        {
            "icon": load_icon_as_base64(Icons.INCOME_TODAY),
            "label": "Este mês:",
            "value": (
                f"{current_month_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
            ),
            "unit": "R$",
        },
        {
            "icon": load_icon_as_base64(Icons.INCOME_MONTH),
            "label": "Total:",
            "value": f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}",
            "unit": "R$",
        },
    ]
    components.html(create_card("Receita da Usina", rows_data), height=200)


def card_environmental_benefits(df: pd.DataFrame) -> None:
    """Exibe cards de benefícios ambientais."""
    rows_data = [
        {
            "icon": load_icon_as_base64(Icons.CO2),
            "label": "Redução de CO2:",
            "value": (
                f"{(df['Energy'].sum() * EnergyFactors.CO2_KG_PER_KWH) / 1000:,.2f}"
            ),
            "unit": "Toneladas",
        },
        {
            "icon": load_icon_as_base64(Icons.TREE),
            "label": "Neutralização:",
            "value": f"{(df['Energy'].sum() * EnergyFactors.TREES_PER_KG_CO2):,.2f}",
            "unit": "Árvores",
        },
    ]
    components.html(create_card("Benefícios Ambientais", rows_data), height=200)


# --- Funções auxiliares ---
def _validate_dataframe(df: pd.DataFrame) -> None:
    """Valida a estrutura do DataFrame."""
    required = {"Energy", "Year", "Month"}
    if missing := required - set(df.columns):
        raise ValueError(f"Colunas faltando: {missing}")


def _calculate_energy_metrics(df: pd.DataFrame) -> dict:
    """Calcula todas as métricas de energia de uma vez."""
    current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month

    return {
        "total_energy_kwh": df["Energy"].sum(),
        "current_month_energy": (
            df[(df["Year"] == current_year) & (df["Month"] == current_month)][
                "Energy"
            ].sum()
        ),
        "current_year_energy": df[df["Year"] == current_year]["Energy"].sum(),
        "total_energy_mwh": df["Energy"].sum() / SystemFactors.MWH_CONVERSION_FACTOR,
        "current_month_mwh": (
            df[(df["Year"] == current_year) & (df["Month"] == current_month)][
                "Energy"
            ].sum()
            / SystemFactors.MWH_CONVERSION_FACTOR
        ),
        "current_year_mwh": (
            df[df["Year"] == current_year]["Energy"].sum()
            / SystemFactors.MWH_CONVERSION_FACTOR
        ),
    }


def _calculate_efficiency(df: pd.DataFrame, total_energy: float) -> dict:
    """Calcula métricas de eficiência."""
    max_possible = (
        SystemFactors.SYSTEM_CAPACITY_KW
        * len(df)
        * SystemFactors.OPERATIONAL_HOURS_PER_DAY
    )
    return {
        "efficiency": (total_energy / max_possible * 100) if max_possible > 0 else 0,
        "max_possible": max_possible,
    }


def _create_metric_row(icon: str, label: str, value: float, unit: str) -> dict:
    """Factory para criação de linhas padronizadas."""
    return {
        "icon": load_icon_as_base64(icon),
        "label": label,
        "value": f"{value:,.2f}",
        "unit": unit,
    }


def _get_current_month_energy(df: pd.DataFrame) -> float:
    """Retorna energia do mês atual."""
    current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
    return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
        "Energy"
    ].sum()

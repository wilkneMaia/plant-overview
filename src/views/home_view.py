import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from components.charts import (
    create_microinverter_year_barchart,
    plot_energy_heatmap_by_microinverter,
    plot_energy_production_by_year,
    plot_energy_trend_by_year,
    plot_line_comparison_by_year,
)
from components.custom_card import create_card, create_card_html
from config.constants import EconomicFactors, EnergyFactors, Icons
from config.styles import setup_shared_styles
from utils.helpers import load_icon_as_base64


class HomeView:
    def __init__(self):
        """Configura apenas estilos (não mais a página)"""
        setup_shared_styles()

    def display(self, data: pd.DataFrame):
        """Método principal para exibir o dashboard"""
        # Seção de filtros (sidebar)
        with st.sidebar:
            st.header("⚙️ Filtros")
            year_min, year_max = int(data["Year"].min()), int(data["Year"].max())
            year_range = st.slider(
                "Selecione o intervalo de anos:",
                min_value=year_min,
                max_value=year_max,
                value=(year_min, year_max),
            )

            microinverters = st.multiselect(
                "Selecione os microinversores:",
                options=data["Microinversor"].unique(),
                default=data["Microinversor"].unique()[:4],
            )

            show_zeros = st.checkbox("Mostrar valores zero", False)
            show_details = st.checkbox("Mostrar detalhes técnicos", False)

        # Filtragem dos dados
        filtered_data = self._filter_data(data, year_range, microinverters, show_zeros)

        # Seção de KPIs
        st.title("🌿 Dashboard de Eficiência Energética")
        self._display_kpi_cards(filtered_data)
        st.divider()

        # Visualizações principais
        self._display_main_visualizations(filtered_data, show_details)

        # Rodapé
        st.caption(
            f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
        )

    def _filter_data(self, data, year_range, microinverters, show_zeros):
        """Aplica filtros aos dados"""
        return data[
            (data["Year"].between(*year_range))
            & (data["Microinversor"].isin(microinverters))
            & ((data["Energy"] > 0) if not show_zeros else True)
        ]

    def _display_kpi_cards(self, data: pd.DataFrame):
        """Exibe todos os cards métricos"""
        # Cards principais (3 métricas)
        cols = st.columns(3)
        metrics = [
            ("Energia Total", f"{data['Energy'].sum():,.1f} kWh", "⚡ Produção total"),
            ("Microinversores", data["Microinversor"].nunique(), "🔌 Unidades ativas"),
            (
                "Eficiência",
                f"{data['Energy'].sum() / data['Microinversor'].nunique():,.1f} kWh/unid",
                "📈 Performance",
            ),
        ]

        for col, (title, value, help_text) in zip(cols, metrics):
            with col:
                st.metric(title, value, help=help_text)

        # Linha divisória
        st.divider()

        # Cards de receita e ambiental
        self._display_metric_cards(data)

    def _display_main_visualizations(self, data: pd.DataFrame, show_details: bool):
        """Gerencia as visualizações principais"""
        tab1, tab2 = st.tabs(["📅 Visão Anual", "🔍 Análise Detalhada"])

        with tab1:
            self._display_yearly_overview(data)

        with tab2:
            self._display_microinverter_analysis(data, show_details)

    def _display_yearly_overview(self, data: pd.DataFrame):
        """Visualizações de evolução anual"""
        col1, col2 = st.columns(2)
        with col1:
            plot_energy_production_by_year(data)

        with col2:
            plot_energy_trend_by_year(data)

        plot_line_comparison_by_year(data)

    def _display_microinverter_analysis(self, data: pd.DataFrame, show_details: bool):
        """Análise detalhada por microinversor"""
        if data.empty:
            st.warning("Nenhum dado disponível com os filtros atuais")
            return

        fig_heatmap = create_microinverter_year_barchart(data)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("Não foi possível gerar o heatmap")

        chart = plot_energy_heatmap_by_microinverter(data)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.warning("Não foi possível gerar o gráfico com os dados fornecidos.")

        if show_details:
            with st.expander("🧐 Dados Técnicos Detalhados"):
                st.dataframe(
                    data.groupby(["Year", "Microinversor"])["Energy"]
                    .sum()
                    .unstack()
                    .style.format("{:.1f} kWh"),
                    use_container_width=True,
                )

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
                "value": (
                    f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
                ),
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
                "value": (
                    f"{(df['Energy'].sum() * EnergyFactors.TREES_PER_KG_CO2):,.2f}"
                ),
                "unit": "Árvores",
            },
        ]
        components.html(create_card("Benefícios Ambientais", rows_data), height=200)

    def _get_current_month_energy(df: pd.DataFrame) -> float:
        """Retorna energia do mês atual."""
        current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
        return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
            "Energy"
        ].sum()

    def _display_metric_cards(self, data: pd.DataFrame) -> None:
        """Exibe todos os cards métricos (receita e benefícios ambientais) em layout organizado."""
        # Validação inicial
        required_cols = {"Energy", "Year", "Month"}
        if missing := required_cols - set(data.columns):
            st.error(f"Dados incompletos para cards. Faltam: {missing}")
            return

        # Layout com 2 colunas
        col1, col2 = st.columns(2)

        with col1:
            self._display_revenue_card(data)

        with col2:
            self._display_environmental_card(data)

    def _display_environmental_card(self, data: pd.DataFrame) -> None:
        """Card de impacto ambiental com visualização intuitiva."""
        try:
            total_energy = data["Energy"].sum()
            co2_reduced = (total_energy * EnergyFactors.CO2_KG_PER_KWH) / 1000
            trees_equivalent = total_energy * EnergyFactors.TREES_PER_KG_CO2

            rows = [
                {
                    "icon": load_icon_as_base64(Icons.CO2),
                    "label": "Redução de CO₂:",
                    "value": f"{co2_reduced:,.1f}",
                    "unit": "Toneladas",
                    "help": f"Equivalente a {co2_reduced * 1000:,.0f} kg",
                },
                {
                    "icon": load_icon_as_base64(Icons.TREE),
                    "label": "Neutralização:",
                    "value": f"{trees_equivalent:,.0f}",
                    "unit": "Árvores",
                    "help": "Necessárias para absorver o CO₂",
                },
            ]

            # Container para agrupar card e caption
            with st.container():
                # Card sem help_text interno
                components.html(
                    create_card_html(
                        title="🌱 Impacto Ambiental",
                        rows=rows,
                        footer=f"Fator: {EnergyFactors.CO2_KG_PER_KWH}kg CO₂/kWh",
                    ),
                    height=420,  # Ajuste para acomodar o footer
                )

        except Exception as e:
            st.error(f"Erro ao gerar card ambiental: {e!s}")

    def _get_current_month_energy(self, df: pd.DataFrame) -> float:  # Adicione 'self'
        """Retorna energia do mês atual."""
        current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
        return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
            "Energy"
        ].sum()

    def _display_revenue_card(self, data: pd.DataFrame) -> None:
        """Card de resumo financeiro com cálculos integrados."""
        try:
            total_energy = data["Energy"].sum()
            current_month_energy = self._get_current_month_energy(
                data
            )  # Agora com self

            rows = [
                {
                    "icon": load_icon_as_base64(Icons.INCOME_TODAY),
                    "label": "Receita Mensal:",
                    "value": (
                        f"{current_month_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
                    ),
                    "unit": "R$",
                    "help": "Baseado na tarifa média de R$0,75/kWh",
                },
                {
                    "icon": load_icon_as_base64(Icons.INCOME_MONTH),
                    "label": "Receita Total:",
                    "value": (
                        f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
                    ),
                    "unit": "R$",
                    "help": "Acumulado no período selecionado",
                },
            ]

            # Modificação para a função create_card sem footer
            with st.container():
                components.html(
                    create_card_html(
                        title="💰 Receita Financeira",
                        rows=rows,
                        footer=f"Tarifa: R${EconomicFactors.ELECTRICITY_PRICE_PER_KWH}/kWh",
                    ),
                    height=420,
                )

        except Exception as e:
            st.error(f"Erro ao gerar card financeiro: {e!s}")


# # --- Funções auxiliares ---
# def _validate_dataframe(df: pd.DataFrame) -> None:
#     """Valida a estrutura do DataFrame."""
#     required = {"Energy", "Year", "Month"}
#     if missing := required - set(df.columns):
#         raise ValueError(f"Colunas faltando: {missing}")


# def _calculate_energy_metrics(df: pd.DataFrame) -> dict:
#     """Calcula todas as métricas de energia de uma vez."""
#     current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month

#     return {
#         "total_energy_kwh": df["Energy"].sum(),
#         "current_month_energy": (
#             df[(df["Year"] == current_year) & (df["Month"] == current_month)][
#                 "Energy"
#             ].sum()
#         ),
#         "current_year_energy": df[df["Year"] == current_year]["Energy"].sum(),
#         "total_energy_mwh": df["Energy"].sum() / SystemFactors.MWH_CONVERSION_FACTOR,
#         "current_month_mwh": (
#             df[(df["Year"] == current_year) & (df["Month"] == current_month)][
#                 "Energy"
#             ].sum()
#             / SystemFactors.MWH_CONVERSION_FACTOR
#         ),
#         "current_year_mwh": (
#             df[df["Year"] == current_year]["Energy"].sum()
#             / SystemFactors.MWH_CONVERSION_FACTOR
#         ),
#     }


# def _calculate_efficiency(df: pd.DataFrame, total_energy: float) -> dict:
#     """Calcula métricas de eficiência."""
#     max_possible = (
#         SystemFactors.SYSTEM_CAPACITY_KW
#         * len(df)
#         * SystemFactors.OPERATIONAL_HOURS_PER_DAY
#     )
#     return {
#         "efficiency": (total_energy / max_possible * 100) if max_possible > 0 else 0,
#         "max_possible": max_possible,
#     }


# def _create_metric_row(icon: str, label: str, value: float, unit: str) -> dict:
#     """Factory para criação de linhas padronizadas."""
#     return {
#         "icon": load_icon_as_base64(icon),
#         "label": label,
#         "value": f"{value:,.2f}",
#         "unit": unit,
#     }


# -------------------- Funções de cards específicos -------------------
# def card_total_performance_indicators(df: pd.DataFrame) -> None:
#     """Exibe indicadores de desempenho da usina com cálculo otimizado e padrões consistentes."""

#     # Cálculos principais (otimizados)
#     energy_data = _calculate_energy_metrics(df)
#     efficiency_metrics = _calculate_efficiency(df, energy_data["total_energy_kwh"])

#     # Construção dos cards
#     rows_data = [
#         _create_metric_row(
#             icon=Icons.POWER_MONTH,
#             label="Energia este mês:",
#             value=energy_data["current_month_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.POWER_YEAR,
#             label="Energia este ano:",
#             value=energy_data["current_year_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.POWER_TOTAL,
#             label="Energia Total:",
#             value=energy_data["total_energy_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.STATS,
#             label="Desvio Padrão:",
#             value=df["Energy"].std(),
#             unit="kWh",
#         ),
#         _create_metric_row(
#             icon=Icons.EFFICIENCY,
#             label="Eficiência:",
#             value=efficiency_metrics["efficiency"],
#             unit="%",
#         ),
#     ]

#     components.html(create_card("Desempenho da Usina", rows_data), height=400)


# def card_total_performance_indicators(df: pd.DataFrame) -> None:
#     """Exibe indicadores de desempenho da usina com cálculo otimizado e padrões consistentes."""

#     # Cálculos principais (otimizados)
#     energy_data = _calculate_energy_metrics(df)
#     efficiency_metrics = _calculate_efficiency(df, energy_data["total_energy_kwh"])

#     # Construção dos cards
#     rows_data = [
#         _create_metric_row(
#             icon=Icons.POWER_MONTH,
#             label="Energia este mês:",
#             value=energy_data["current_month_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.POWER_YEAR,
#             label="Energia este ano:",
#             value=energy_data["current_year_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.POWER_TOTAL,
#             label="Energia Total:",
#             value=energy_data["total_energy_mwh"],
#             unit="MWh",
#         ),
#         _create_metric_row(
#             icon=Icons.STATS,
#             label="Desvio Padrão:",
#             value=df["Energy"].std(),
#             unit="kWh",
#         ),
#         _create_metric_row(
#             icon=Icons.EFFICIENCY,
#             label="Eficiência:",
#             value=efficiency_metrics["efficiency"],
#             unit="%",
#         ),
#     ]

#     components.html(create_card("Desempenho da Usina", rows_data), height=400)


# def card_revenue_summary(df: pd.DataFrame) -> None:
#     """Exibe resumo de receita com ícones padronizados."""
#     # Setup
#     # locale.setlocale(locale.LC_ALL, LOCALE_CURRENCY)

#     # Validação
#     required_columns = {"Energy", "Year", "Month"}
#     if not required_columns.issubset(df.columns):
#         raise ValueError(f"Colunas faltando: {required_columns - set(df.columns)}")

#     # Cálculos
#     total_energy = df["Energy"].sum()
#     current_month_energy = _get_current_month_energy(df)

#     rows_data = [
#         {
#             "icon": load_icon_as_base64(Icons.INCOME_TODAY),
#             "label": "Este mês:",
#             "value": (
#                 f"{current_month_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
#             ),
#             "unit": "R$",
#         },
#         {
#             "icon": load_icon_as_base64(Icons.INCOME_MONTH),
#             "label": "Total:",
#             "value": f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}",
#             "unit": "R$",
#         },
#     ]
#     components.html(create_card("Receita da Usina", rows_data), height=200)


# def card_environmental_benefits(df: pd.DataFrame) -> None:
#     """Exibe cards de benefícios ambientais."""
#     rows_data = [
#         {
#             "icon": load_icon_as_base64(Icons.CO2),
#             "label": "Redução de CO2:",
#             "value": (
#                 f"{(df['Energy'].sum() * EnergyFactors.CO2_KG_PER_KWH) / 1000:,.2f}"
#             ),
#             "unit": "Toneladas",
#         },
#         {
#             "icon": load_icon_as_base64(Icons.TREE),
#             "label": "Neutralização:",
#             "value": f"{(df['Energy'].sum() * EnergyFactors.TREES_PER_KG_CO2):,.2f}",
#             "unit": "Árvores",
#         },
#     ]
#     components.html(create_card("Benefícios Ambientais", rows_data), height=200)


# # --- Funções auxiliares ---
# def _validate_dataframe(df: pd.DataFrame) -> None:
#     """Valida a estrutura do DataFrame."""
#     required = {"Energy", "Year", "Month"}
#     if missing := required - set(df.columns):
#         raise ValueError(f"Colunas faltando: {missing}")


# def _calculate_energy_metrics(df: pd.DataFrame) -> dict:
#     """Calcula todas as métricas de energia de uma vez."""
#     current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month

#     return {
#         "total_energy_kwh": df["Energy"].sum(),
#         "current_month_energy": (
#             df[(df["Year"] == current_year) & (df["Month"] == current_month)][
#                 "Energy"
#             ].sum()
#         ),
#         "current_year_energy": df[df["Year"] == current_year]["Energy"].sum(),
#         "total_energy_mwh": df["Energy"].sum() / SystemFactors.MWH_CONVERSION_FACTOR,
#         "current_month_mwh": (
#             df[(df["Year"] == current_year) & (df["Month"] == current_month)][
#                 "Energy"
#             ].sum()
#             / SystemFactors.MWH_CONVERSION_FACTOR
#         ),
#         "current_year_mwh": (
#             df[df["Year"] == current_year]["Energy"].sum()
#             / SystemFactors.MWH_CONVERSION_FACTOR
#         ),
#     }


# def _calculate_efficiency(df: pd.DataFrame, total_energy: float) -> dict:
#     """Calcula métricas de eficiência."""
#     max_possible = (
#         SystemFactors.SYSTEM_CAPACITY_KW
#         * len(df)
#         * SystemFactors.OPERATIONAL_HOURS_PER_DAY
#     )
#     return {
#         "efficiency": (total_energy / max_possible * 100) if max_possible > 0 else 0,
#         "max_possible": max_possible,
#     }


# def _create_metric_row(icon: str, label: str, value: float, unit: str) -> dict:
#     """Factory para criação de linhas padronizadas."""
#     return {
#         "icon": load_icon_as_base64(icon),
#         "label": label,
#         "value": f"{value:,.2f}",
#         "unit": unit,
#     }


# def _get_current_month_energy(df: pd.DataFrame) -> float:
#     """Retorna energia do mês atual."""
#     current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
#     return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
#         "Energy"
#     ].sum()

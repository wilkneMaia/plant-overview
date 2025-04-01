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
from components.custom_card import create_card_html
from config.constants import EconomicFactors, EnergyFactors, Icons
from config.styles import setup_shared_styles
from utils.helpers import load_icon_as_base64


class HomeView:
    def __init__(self):
        """Configura estilos compartilhados para a página."""
        setup_shared_styles()

    def display(self, data: pd.DataFrame):
        """Método principal para exibir o dashboard."""
        self._render_sidebar(data)
        filtered_data = self._apply_filters(data)
        self._render_dashboard(filtered_data)

    def _render_sidebar(self, data: pd.DataFrame):
        """Renderiza a barra lateral com filtros."""
        with st.sidebar:
            st.header("⚙️ Filtros")
            self.year_range = st.slider(
                "Selecione o intervalo de anos:",
                min_value=int(data["Year"].min()),
                max_value=int(data["Year"].max()),
                value=(int(data["Year"].min()), int(data["Year"].max())),
            )
            self.microinverters = st.multiselect(
                "Selecione os microinversores:",
                options=data["Microinversor"].unique(),
                default=data["Microinversor"].unique()[:4],
            )
            self.show_zeros = st.checkbox("Mostrar valores zero", False)
            self.show_details = st.checkbox("Mostrar detalhes técnicos", False)

    def _apply_filters(self, data: pd.DataFrame) -> pd.DataFrame:
        """Aplica os filtros selecionados na barra lateral."""
        return data[
            (data["Year"].between(*self.year_range))
            & (data["Microinversor"].isin(self.microinverters))
            & ((data["Energy"] > 0) if not self.show_zeros else True)
        ]

    def _render_dashboard(self, data: pd.DataFrame):
        """Renderiza o conteúdo principal do dashboard."""
        st.title("🌿 Dashboard de Eficiência Energética")
        self._display_kpi_cards(data)
        st.divider()
        self._display_main_visualizations(data)
        st.caption(
            f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
        )

    def _display_kpi_cards(self, data: pd.DataFrame):
        """Exibe os KPIs principais no formato de cards."""
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

        st.divider()
        self._display_metric_cards(data)

    def _display_metric_cards(self, data: pd.DataFrame):
        """Exibe os cards de receita e impacto ambiental."""
        col1, col2, col3 = st.columns(3)
        with col1:
            self.display_system_overview_card(data)

            self._display_revenue_card(data)

        with col2:
            self._display_total_energy_card(data)

            self._display_environmental_card(data)

        with col3:
            self.display_efficiency_card(data)

    def display_system_overview_card(self, data: pd.DataFrame):
        """Exibe o card com informações de registros, período e total de microinversores ativos."""
        # Calcular o número total de registros
        total_records = len(data)

        # Determinar o período dos dados (data mais antiga até a mais recente)
        if not data.empty and "Date" in data.columns:
            start_date = data["Date"].min()
            end_date = data["Date"].max()
            period = (
                f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
            )
        else:
            period = "Não disponível"

        # Contar microinversores ativos únicos
        total_active_microinverters = data["Microinversor"].nunique()

        # Define as linhas do card
        rows = [
            {
                "icon": load_icon_as_base64(Icons.DATABASE),
                "label": "Registros:",
                "value": f"{total_records:,}",
                "unit": "entradas",
                "help": "Total de registros no conjunto de dados selecionado",
            },
            {
                "icon": load_icon_as_base64(Icons.CALENDAR),
                "label": "Período:",
                "value": period,
                "unit": "",
                "help": "Intervalo de datas dos registros analisados",
            },
            {
                "icon": load_icon_as_base64(Icons.DEVICES),
                "label": "Microinversores Ativos:",
                "value": f"{total_active_microinverters:,}",
                "unit": "unidades",
                "help": "Quantidade total de microinversores ativos no período",
            },
        ]

        # Renderiza o card
        self._render_card("📋 Visão Geral do Sistema", rows)

    def display_efficiency_card(self, data: pd.DataFrame):
        """Exibe o card de desvio padrão e eficiência."""
        # Calcula o desvio padrão da energia gerada
        energy_std_dev = data["Energy"].std()

        # Calcula a eficiência média por microinversor
        efficiency = data["Energy"].sum() / data["Microinversor"].nunique()

        # Calcula o coeficiente de variação (cv = desvio padrão / média)
        mean_energy = data["Energy"].mean()
        coef_variation = (energy_std_dev / mean_energy) * 100 if mean_energy > 0 else 0

        # Define as linhas do card
        rows = [
            {
                "icon": load_icon_as_base64(Icons.POWER_TOTAL),
                "label": "Desvio Padrão:",
                "value": f"{energy_std_dev:,.2f}",
                "unit": "kWh",
                "help": "Desvio padrão da energia gerada no período selecionado",
            },
            {
                "icon": load_icon_as_base64(Icons.POWER_YEAR),
                "label": "Eficiência Média:",
                "value": f"{efficiency:,.2f}",
                "unit": "kWh/unid",
                "help": "Eficiência média por microinversor no período selecionado",
            },
            {
                "icon": load_icon_as_base64(Icons.PERFORMANCE),
                "label": "Coef. de Variação:",
                "value": f"{coef_variation:,.2f}",
                "unit": "%",
                "help": (
                    "Variabilidade relativa entre os microinversores (menor valor indica maior consistência)"
                ),
            },
        ]

        # Renderiza o card
        self._render_card("📊 Desvio Padrão | Eficiência", rows)

    def _display_total_energy_card(self, data: pd.DataFrame):
        """Exibe o card de energia total gerada."""
        total_energy = data["Energy"].sum()
        rows = [
            {
                "icon": load_icon_as_base64(Icons.POWER_MONTH),
                "label": "Energia Mensal:",
                "value": f"{self._get_current_month_energy(data):,.1f}",
                "unit": "kWh",
                "help": "Energia gerada no período selecionado",
            },
            {
                "icon": load_icon_as_base64(Icons.POWER_YEAR),
                "label": "Energia Anual:",
                "value": f"{data['Energy'].sum():,.1f}",
                "unit": "kWh",
                "help": "Energia gerada no ano atual",
            },
            {
                "icon": load_icon_as_base64(Icons.POWER_TOTAL),
                "label": "Energia Total:",
                "value": f"{total_energy:,.1f}",
                "unit": "kWh",
                "help": "Energia total gerada no período selecionado",
            },
        ]
        self._render_card("⚡ Energia Total", rows)

    def _display_revenue_card(self, data: pd.DataFrame):
        """Exibe o card de resumo financeiro."""
        total_energy = data["Energy"].sum()
        current_month_energy = self._get_current_month_energy(data)
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
        self._render_card(
            "💰 Receita Financeira",
            rows,
            f"Tarifa: R${EconomicFactors.ELECTRICITY_PRICE_PER_KWH}/kWh",
        )

    def _display_environmental_card(self, data: pd.DataFrame):
        """Exibe o card de impacto ambiental."""
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
        self._render_card(
            "🌱 Impacto Ambiental",
            rows,
            f"Fator: {EnergyFactors.CO2_KG_PER_KWH}kg CO₂/kWh",
        )

    def _render_card(self, title: str, rows: list, footer: str = None):
        """Renderiza um card estilizado."""
        with st.container():
            components.html(
                create_card_html(title=title, rows=rows, footer=footer),
                height=275,
            )

    def _get_current_month_energy(self, df: pd.DataFrame) -> float:
        """Calcula a energia gerada no mês atual."""
        current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
        return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
            "Energy"
        ].sum()

    def _display_main_visualizations(self, data: pd.DataFrame):
        """Exibe as visualizações principais."""
        tab1, tab2 = st.tabs(["📅 Visão Anual", "🔍 Análise Detalhada"])
        with tab1:
            self._display_yearly_overview(data)
        with tab2:
            self._display_microinverter_analysis(data)

    def _display_yearly_overview(self, data: pd.DataFrame):
        """Exibe gráficos de evolução anual."""
        col1, col2 = st.columns(2)
        with col1:
            plot_energy_production_by_year(data)
        with col2:
            plot_energy_trend_by_year(data)
        plot_line_comparison_by_year(data)

    def _display_microinverter_analysis(self, data: pd.DataFrame):
        """Exibe análise detalhada por microinversor."""
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

    # def card_revenue_summary(self, df: pd.DataFrame) -> None:
    #     """Exibe resumo de receita com ícones padronizados."""
    #     # Setup
    #     # locale.setlocale(locale.LC_ALL, LOCALE_CURRENCY)

    #     # Validação
    #     required_columns = {"Energy", "Year", "Month"}
    #     if not required_columns.issubset(df.columns):
    #         raise ValueError(f"Colunas faltando: {required_columns - set(df.columns)}")

    #     # Cálculos
    #     total_energy = df["Energy"].sum()
    #     current_month_energy = self._get_current_month_energy(df)

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
    #             "value": (
    #                 f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
    #             ),
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
    #             "value": (
    #                 f"{(df['Energy'].sum() * EnergyFactors.TREES_PER_KG_CO2):,.2f}"
    #             ),
    #             "unit": "Árvores",
    #         },
    #     ]
    #     components.html(create_card("Benefícios Ambientais", rows_data), height=200)

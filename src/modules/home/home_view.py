import pandas as pd
import streamlit as st

from config.styles import setup_shared_styles

from .charts import (
    plot_energy_heatmap_by_microinverter,
    plot_energy_production_by_year,
    plot_line_comparison_by_year,
    plot_microinverter_year_barchart,
)
from .components import (
    card_info_average_efficiency,
    card_info_co2,
    card_info_coefficient_of_variation,
    card_info_energy_month,
    card_info_energy_total,
    card_info_energy_year,
    card_info_microinverters,
    card_info_period,
    card_info_raw_coal_saved,
    card_info_records,
    card_info_std_dev,
    card_info_tree,
)


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
        self._display_metric_cards(data)
        # self._display_kpi_cards(data)
        st.divider()
        self._display_main_visualizations(data)
        st.caption(
            f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}"
        )

    def _display_metric_cards(self, data: pd.DataFrame):
        """Exibe os cards de receita e impacto ambiental."""
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # display_system_overview_card(data)
            # display_revenue_card(data)
            # display_total_energy_card(data)
            # display_environmental_card(data)
            # display_efficiency_card(data)
            card_info_period(data)
            card_info_records(data)
            card_info_microinverters(data)

        with col2:
            card_info_energy_month(data)
            card_info_energy_year(data)
            card_info_energy_total(data)

        with col3:
            card_info_std_dev(data)
            card_info_average_efficiency(data)
            card_info_coefficient_of_variation(data)
        with col4:
            card_info_raw_coal_saved(data)
            card_info_co2(data)
            card_info_tree(data)

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
            # plot_energy_trend_by_year(data)

            plot_line_comparison_by_year(data)

        st.divider()
        fig_barchart = plot_microinverter_year_barchart(data)
        if fig_barchart:
            st.plotly_chart(fig_barchart, use_container_width=True)
        else:
            st.warning("Não foi possível gerar o gráfico de barras agrupadas.")

    def _display_microinverter_analysis(self, data: pd.DataFrame):
        """Exibe análise detalhada por microinversor."""
        if data.empty:
            st.warning("Nenhum dado disponível com os filtros atuais")
            return

        # Verificar se as colunas necessárias estão presentes
        required_columns = {"Microinversor", "Year", "Energy"}
        if not required_columns.issubset(data.columns):
            st.error(
                f"Os dados fornecidos estão incompletos. Colunas necessárias: {required_columns}"
            )
            return

        # Gráfico de barras agrupadas
        try:
            fig_barchart = plot_microinverter_year_barchart(data)
            if fig_barchart:
                st.plotly_chart(fig_barchart, use_container_width=True)
            else:
                st.warning("Não foi possível gerar o gráfico de barras agrupadas.")
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico de barras agrupadas: {e}")

        # Heatmap de energia
        try:
            fig_heatmap = plot_energy_heatmap_by_microinverter(data)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.warning("Não foi possível gerar o heatmap.")
        except Exception as e:
            st.error(f"Erro ao gerar o heatmap: {e}")

    # def display_efficiency_card(self, data: pd.DataFrame):
    #     """Exibe o card de desvio padrão, eficiência e coeficiente de variação."""
    #     # Calcula as métricas usando funções externas
    #     energy_std_dev = calculate_energy_std_dev(data)
    #     efficiency = calculate_efficiency(data)
    #     coef_variation = calculate_coefficient_of_variation(data)

    #     # Define as linhas do card
    #     rows = [
    #         create_row(
    #             icon=Icons.POWER_TOTAL,
    #             label="Desvio Padrão:",
    #             value=f"{energy_std_dev:,.2f}",
    #             unit="kWh",
    #             help_text="Desvio padrão da energia gerada no período selecionado",
    #         ),
    #         create_row(
    #             icon=Icons.POWER_YEAR,
    #             label="Eficiência Média:",
    #             value=f"{efficiency:,.2f}",
    #             unit="kWh/unid",
    #             help_text="Eficiência média por microinversor no período selecionado",
    #         ),
    #         create_row(
    #             icon=Icons.PERFORMANCE,
    #             label="Coef. de Variação:",
    #             value=f"{coef_variation:,.2f}",
    #             unit="%",
    #             help_text="Variabilidade relativa entre os microinversores (menor valor indica maior consistência)",
    #         ),
    #     ]

    #     # Renderiza o card
    #     render_card("📊 Desvio Padrão | Eficiência", rows)

    # def _display_environmental_card(self, data: pd.DataFrame):
    #     """Exibe o card de impacto ambiental."""
    #     total_energy = data["Energy"].sum()
    #     co2_reduced = (total_energy * EnergyFactors.CO2_KG_PER_KWH) / 1000
    #     trees_equivalent = total_energy * EnergyFactors.TREES_PER_KG_CO2
    #     rows = [
    #         {
    #             "icon": load_icon_as_base64(Icons.CO2),
    #             "label": "Redução de CO₂:",
    #             "value": f"{co2_reduced:,.1f}",
    #             "unit": "Toneladas",
    #             "help": f"Equivalente a {co2_reduced * 1000:,.0f} kg",
    #         },
    #         {
    #             "icon": load_icon_as_base64(Icons.TREE),
    #             "label": "Neutralização:",
    #             "value": f"{trees_equivalent:,.0f}",
    #             "unit": "Árvores",
    #             "help": "Necessárias para absorver o CO₂",
    #         },
    #     ]
    #     render_card(
    #         "🌱 Impacto Ambiental",
    #         rows,
    #         f"Fator: {EnergyFactors.CO2_KG_PER_KWH}kg CO₂/kWh",
    #     )

    # def _display_total_energy_card(self, data: pd.DataFrame):
    #     """Exibe o card de energia total gerada."""
    #     # Importa cálculos do arquivo metrics.py
    #     from .metrics import calculate_current_month_energy, calculate_total_energy

    #     # Calcula as métricas
    #     total_energy = calculate_total_energy(data)
    #     current_month_energy = calculate_current_month_energy(data)

    #     # Define as linhas do card
    #     rows = [
    #         create_row(
    #             icon=Icons.POWER_MONTH,
    #             label="Energia Mensal:",
    #             value=f"{current_month_energy:,.1f}",
    #             unit="kWh",
    #             help_text="Energia gerada no mês atual",
    #         ),
    #         create_row(
    #             icon=Icons.POWER_YEAR,
    #             label="Energia Anual:",
    #             value=f"{data['Energy'].sum():,.1f}",
    #             unit="kWh",
    #             help_text="Energia gerada no ano atual",
    #         ),
    #         create_row(
    #             icon=Icons.POWER_TOTAL,
    #             label="Energia Total:",
    #             value=f"{total_energy:,.1f}",
    #             unit="kWh",
    #             help_text="Energia total gerada no período selecionado",
    #         ),
    #     ]

    #     # Renderiza o card
    #     render_card("⚡ Energia Total", rows)

    # def _display_revenue_card(self, data: pd.DataFrame):
    #     """Exibe o card de resumo financeiro."""
    #     total_energy = calculate_total_energy(data)
    #     current_month_energy = calculate_current_month_energy(data)
    #     rows = [
    #         {
    #             "icon": load_icon_as_base64(Icons.INCOME_TODAY),
    #             "label": "Receita Mensal:",
    #             "value": (
    #                 f"{current_month_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
    #             ),
    #             "unit": "R$",
    #             "help": "Baseado na tarifa média de R$0,75/kWh",
    #         },
    #         {
    #             "icon": load_icon_as_base64(Icons.INCOME_MONTH),
    #             "label": "Receita Total:",
    #             "value": (
    #                 f"{total_energy * EconomicFactors.ELECTRICITY_PRICE_PER_KWH:,.2f}"
    #             ),
    #             "unit": "R$",
    #             "help": "Acumulado no período selecionado",
    #         },
    #     ]
    #     render_card(
    #         "💰 Receita Financeira",
    #         rows,
    #         f"Tarifa: R${EconomicFactors.ELECTRICITY_PRICE_PER_KWH}/kWh",
    #     )

    # def _display_kpi_cards(self, data: pd.DataFrame):
    #     """Exibe os KPIs principais no formato de cards."""
    #     cols = st.columns(3)
    #     metrics = [
    #         ("Energia Total", f"{data['Energy'].sum():,.1f} kWh", "⚡ Produção total"),
    #         ("Microinversores", data["Microinversor"].nunique(), "🔌 Unidades ativas"),
    #         (
    #             "Eficiência",
    #             f"{data['Energy'].sum() / data['Microinversor'].nunique():,.1f} kWh/unid",
    #             "📈 Performance",
    #         ),
    #     ]
    #     for col, (title, value, help_text) in zip(cols, metrics):
    #         with col:
    #             st.metric(title, value, help=help_text)

    # def _get_current_month_energy(self, df: pd.DataFrame) -> float:
    #     """Calcula a energia gerada no mês atual."""
    #     current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
    #     return df[(df["Year"] == current_year) & (df["Month"] == current_month)][
    #         "Energy"
    #     ].sum()

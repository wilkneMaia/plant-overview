import pandas as pd
import streamlit.components.v1 as components

from components.card_info import card_info
from components.card_info_2 import card_info_2
from components.custom_card import create_card_html
from config.constants import EconomicFactors, EnergyFactors, FontCards, Icons
from utils.helpers import load_icon_as_base64

from .metrics import (
    alculate_current_year_energy,
    calculate_coefficient_of_variation,
    calculate_current_month_energy,
    calculate_efficiency,
    calculate_energy_std_dev,
    calculate_total_energy,
)


def render_card(title: str, rows: list, footer: str = None, height: int = 220):
    """
    Renderiza um card estilizado no Streamlit.

    Args:
        title (str): Título do card.
        rows (list): Lista de dicionários com {icon, label, value, unit, help}.
        footer (str, opcional): Texto de rodapé. Se None, o rodapé não será exibido.
        height (int, opcional): Altura do card. Padrão: 220.

    Returns:
        None: Renderiza o card diretamente no Streamlit.
    """
    components.html(
        create_card_html(title=title, rows=rows, footer=footer), height=height
    )


def create_row(
    icon: str, label: str, value: str, unit: str, help_text: str = None
) -> dict:
    """
    Cria uma linha para ser usada em um card.

    Args:
        icon (str): Caminho ou base64 do ícone.
        label (str): Texto descritivo da linha.
        value (str): Valor a ser exibido.
        unit (str): Unidade do valor.
        help_text (str, opcional): Texto de ajuda para exibição.

    Returns:
        dict: Dicionário representando a linha.
    """
    return {
        "icon": load_icon_as_base64(icon),
        "label": label,
        "value": value,
        "unit": unit,
        "help": help_text,
    }


def display_system_overview_card(data: pd.DataFrame, microinverters=None):
    """
    Exibe o card com informações de registros, período e total de microinversores ativos.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados a serem analisados
        microinverters (list, optional): Lista de microinversores. Se None, conta os microinversores
                                        únicos no DataFrame.
    """
    # Calcular o número total de registros
    total_records = len(data)

    # Determinar o período dos dados (data mais antiga até a mais recente)
    if not data.empty and "Date" in data.columns:
        start_date = data["Date"].min()
        end_date = data["Date"].max()
        period = f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
    else:
        period = "Não disponível"

    # Contar total de microinversores
    if microinverters is not None:
        total_microinverters = len(microinverters)
    else:
        total_microinverters = (
            data["Microinversor"].nunique() if "Microinversor" in data.columns else 0
        )

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
            "value": f"{total_microinverters:,}",
            "unit": "unidades",
            "help": "Total de microinversores ativos no período selecionado",
        },
    ]

    components.html(
        create_card_html(title="📋 Visão Geral do Sistema", rows=rows), height=220
    )


# --- Cards de Métricas ---
# Card de resumo financeiro
def display_revenue_card(data: pd.DataFrame, tariff_kwh=None):
    """
    Exibe o card de resumo financeiro.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados a serem analisados
        tariff_kwh (float, optional): Valor da tarifa de energia por kWh.
                                      Se None, usa o valor de EconomicFactors.ELECTRICITY_PRICE_PER_KWH
    """
    # Usa o valor padrão da tarifa se não for fornecido
    if tariff_kwh is None:
        tariff_kwh = EconomicFactors.ELECTRICITY_PRICE_PER_KWH

    # Calcula as métricas de energia
    total_energy = calculate_total_energy(data)
    current_month_energy = calculate_current_month_energy(data)

    # Define as linhas do card
    rows = [
        {
            "icon": load_icon_as_base64(Icons.INCOME_TODAY),
            "label": "Este mês:",
            "value": f"{current_month_energy * tariff_kwh:,.2f}",
            "unit": "R$",
            "help": f"Baseado na tarifa média de R${tariff_kwh:.2f}/kWh",
        },
        {
            "icon": load_icon_as_base64(Icons.INCOME_MONTH),
            "label": "Total:",
            "value": f"{total_energy * tariff_kwh:,.2f}",
            "unit": "R$",
            "help": "Acumulado no período selecionado",
        },
    ]

    # Renderiza o card
    render_card(
        "💰 Receita Financeira",
        rows,
        f"Tarifa: R${tariff_kwh}/kWh",
    )


# Card de energia gerada total
def display_total_energy_card(data: pd.DataFrame):
    """
    Exibe o card de energia total gerada.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados a serem analisados
    """

    # Calcula as métricas
    total_energy_mwh = calculate_total_energy(data) / 1000
    current_year_energy_mwh = alculate_current_year_energy(data) / 1000
    current_month_energy = calculate_current_month_energy(data)

    # Define as linhas do card
    rows = [
        create_row(
            icon=Icons.POWER_MONTH,
            label="Energia este mês:",
            value=f"{current_month_energy:,.2f}",
            unit="kWh",
            help_text="Energia gerada no mês atual",
        ),
        create_row(
            icon=Icons.POWER_YEAR,
            label="Energia Anual:",
            value=f"{current_year_energy_mwh:,.2f}",
            unit="MWh",
            help_text="Energia gerada no ano atual",
        ),
        create_row(
            icon=Icons.POWER_TOTAL,
            label="Energia Total:",
            value=f"{total_energy_mwh:,.2f}",
            unit="MWh",
            help_text="Energia total gerada no período selecionado",
        ),
    ]

    # Renderiza o card
    render_card("⚡ Energia Total", rows)


# Card de impacto ambiental
def display_environmental_card(data: pd.DataFrame):
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
    render_card(
        "🌱 Impacto Ambiental",
        rows,
        f"Fator: {EnergyFactors.CO2_KG_PER_KWH}kg CO₂/kWh",
    )


# Card de desvio padrão, eficiência e coeficiente de variação
def display_efficiency_card(data: pd.DataFrame):
    """Exibe o card de desvio padrão, eficiência e coeficiente de variação."""
    # Calcula as métricas usando funções externas
    energy_std_dev = calculate_energy_std_dev(data)
    efficiency = calculate_efficiency(data)
    coef_variation = calculate_coefficient_of_variation(data)

    # Define as linhas do card
    rows = [
        create_row(
            icon=Icons.POWER_TOTAL,
            label="Desvio Padrão:",
            value=f"{energy_std_dev:,.2f}",
            unit="kWh",
            help_text="Desvio padrão da energia gerada no período selecionado",
        ),
        create_row(
            icon=Icons.POWER_YEAR,
            label="Eficiência Média:",
            value=f"{efficiency:,.2f}",
            unit="kWh/unid",
            help_text="Eficiência média por microinversor no período selecionado",
        ),
        create_row(
            icon=Icons.PERFORMANCE,
            label="Coef. de Variação:",
            value=f"{coef_variation:,.2f}",
            unit="%",
            help_text="Variabilidade relativa entre os microinversores (menor valor indica maior consistência)",
        ),
    ]

    # Renderiza o card
    render_card("📊 Desvio Padrão | Eficiência", rows)


# --- Cards de informações ---
#  Card de energia gerada no mês atual
def card_info_energy_month(data: pd.DataFrame, tariff_kwh=None):
    # Calcula as métricas
    current_month_energy = calculate_current_month_energy(data)

    # Usa o valor padrão da tarifa se não for fornecido
    if tariff_kwh is None:
        tariff_kwh = EconomicFactors.ELECTRICITY_PRICE_PER_KWH

    card_info(
        title="Energia este mês",
        title_style=FontCards.TITLE,
        primary_value=f"{current_month_energy:,.2f}",
        primary_value_style=FontCards.PRIMARY_VALUE,
        primary_unit=" kWh",
        primary_unit_style=FontCards.PRIMARY_UNIT,
        subtitle="Receita: ",
        subtitle_style=FontCards.SUBTITLE,
        secondary_value=f"{current_month_energy * tariff_kwh:,.2f}",
        secondary_value_style=FontCards.SECONDARY_VALUE,
        secondary_unit="R$",
        secondary_unit_style=FontCards.SECONDARY_UNIT,
        secondary_unit_position="left",
        icon_name=Icons.POWER_MONTH,
        icon_size="40px",
        card_height="100px",
        card_width="300px",
        card_background_color="#f4f5f7",
    )


# Card de energia gerada no ano atual
def card_info_energy_year(data: pd.DataFrame, tariff_kwh=None):
    # Calcula as métricas
    current_year_energy_mwh = alculate_current_year_energy(data)

    # Usa o valor padrão da tarifa se não for fornecido
    if tariff_kwh is None:
        tariff_kwh = EconomicFactors.ELECTRICITY_PRICE_PER_KWH

    card_info(
        title="Energia este ano",
        title_style=FontCards.TITLE,
        primary_value=f"{current_year_energy_mwh:,.2f}",
        primary_value_style=FontCards.PRIMARY_VALUE,
        primary_unit=" MWh",
        primary_unit_style=FontCards.PRIMARY_UNIT,
        subtitle="Receita: ",
        subtitle_style=FontCards.SUBTITLE,
        secondary_value=f"{current_year_energy_mwh * tariff_kwh:,.2f}",
        secondary_value_style=FontCards.SECONDARY_VALUE,
        secondary_unit="R$",
        secondary_unit_style=FontCards.SECONDARY_UNIT,
        secondary_unit_position="left",
        icon_name=Icons.POWER_YEAR,
        icon_size="40px",
        card_height="100px",
        card_width="300px",
        card_background_color="#f4f5f7",
    )


# Card de energia gerada total
def card_info_energy_total(data: pd.DataFrame, tariff_kwh=None):
    # Calcula as métricas
    total_energy_mwh = calculate_total_energy(data)

    # Usa o valor padrão da tarifa se não for fornecido
    if tariff_kwh is None:
        tariff_kwh = EconomicFactors.ELECTRICITY_PRICE_PER_KWH

    card_info(
        title="Energia total",
        title_style=FontCards.TITLE,
        primary_value=f"{total_energy_mwh:,.2f}",
        primary_value_style=FontCards.PRIMARY_VALUE,
        primary_unit=" MWh",
        primary_unit_style=FontCards.PRIMARY_UNIT,
        subtitle="Receita: ",
        subtitle_style=FontCards.SUBTITLE,
        secondary_value=f"{total_energy_mwh * tariff_kwh:,.2f}",
        secondary_value_style=FontCards.SECONDARY_VALUE,
        secondary_unit="R$",
        secondary_unit_style=FontCards.SECONDARY_UNIT,
        secondary_unit_position="left",
        icon_name=Icons.POWER_TOTAL,
        icon_size="40px",
        card_height="100px",
        card_width="300px",
        card_background_color="#f4f5f7",
    )


# --- Cards de informações impacto ambiental ---
def card_info_raw_coal_saved(data: pd.DataFrame):
    # Calcula a energia total em MWh
    total_energy_mwh = data["Energy"].sum() / 1000  # Converte kWh para MWh

    # Calcula o carvão bruto economizado
    raw_coal_saved = total_energy_mwh * EnergyFactors.COAL_SAVED_PER_MWH

    # Renderiza o card
    card_info_2(
        title_style=FontCards.TITLE,
        icon_name=Icons.RAW_COAL_SAVED,
        main_title="Carvão bruto economizado",
        value=f"{raw_coal_saved:,.2f}",  # Formata com 2 casas decimais
        unit="Tonelada(s)",
        card_height="100px",
        card_width="300px",
    )


def card_info_co2(data: pd.DataFrame):

    # Calcula as métricas
    total_energy = data["Energy"].sum()
    co2_reduced = (total_energy * EnergyFactors.CO2_KG_PER_KWH) / 1000

    # Renderiza o card
    card_info_2(
        title_style=FontCards.TITLE,
        icon_name=Icons.CO2,
        main_title="Redução da emissão de CO2",
        value=f"{co2_reduced:,.2f}",
        unit="Tonelada(s)",
        card_height="100px",
        card_width="300px",
    )


def card_info_tree(data: pd.DataFrame):
    # Calcula as métricas
    total_energy = data["Energy"].sum()
    trees_equivalent = total_energy * EnergyFactors.TREES_PER_KG_CO2

    # Renderiza o card
    card_info_2(
        title_style=FontCards.TITLE,
        icon_name=Icons.TREE,
        main_title="Neutralização de carbono",
        value=f"{trees_equivalent:,.0f}",
        unit="Arvores",
        card_height="100px",
        card_width="300px",
    )

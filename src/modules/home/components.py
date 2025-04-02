import pandas as pd
import streamlit.components.v1 as components

from config.constants import EconomicFactors, EnergyFactors, Icons
from utils.helpers import load_icon_as_base64

from .metrics import (
    alculate_current_year_energy,
    calculate_coefficient_of_variation,
    calculate_current_month_energy,
    calculate_efficiency,
    calculate_energy_std_dev,
    calculate_total_energy,
)


def render_card(title: str, rows: list, footer: str = None, height: int = 275):
    """
    Renderiza um card estilizado no Streamlit.

    Args:
        title (str): Título do card.
        rows (list): Lista de dicionários com {icon, label, value, unit, help}.
        footer (str, opcional): Texto de rodapé. Se None, o rodapé não será exibido.
        height (int, opcional): Altura do card. Padrão: 275.

    Returns:
        None: Renderiza o card diretamente no Streamlit.
    """
    from components.custom_card import create_card_html

    components.html(
        create_card_html(title=title, rows=rows, footer=footer),
        height=height,
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

    # Renderiza o card
    render_card("📋 Visão Geral do Sistema", rows)


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

import base64
import locale
import os

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from components.custom_card import create_card, create_card_html

# Caminho base para os ícones
base_dir = os.path.dirname(os.path.abspath(__file__))
icons_dir = os.path.join(base_dir, "../assets/icons")


# Função para carregar uma imagem como base64
def load_image_as_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado - {image_path}")
        return None


# Dicionário para armazenar imagens em base64
images_base64 = {
    "icon-power-month": load_image_as_base64(
        os.path.join(icons_dir, "icon-power-month.svg")
    ),
    "icon-power-year": load_image_as_base64(
        os.path.join(icons_dir, "icon-power-year.svg")
    ),
    "icon-power-total": load_image_as_base64(
        os.path.join(icons_dir, "icon-power-total.svg")
    ),
    "icon-income-today": load_image_as_base64(
        os.path.join(icons_dir, "icon-income-today.svg")
    ),
    "icon-income-month": load_image_as_base64(
        os.path.join(icons_dir, "icon-income-month.svg")
    ),
    "icon-co2": load_image_as_base64(os.path.join(icons_dir, "icon-co2.svg")),
    "icon-tree": load_image_as_base64(os.path.join(icons_dir, "icon-tree.svg")),
    # Adicione mais imagens conforme necessário
}

# Configure locale to format Brazilian currency
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


def create_line_chart(df, x, y, title, color_discrete_sequence=None):
    fig = px.line(df, x=x, y=y, color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Value")
    return fig


def plot_total_by_year(df):
    """Exibe o total de energia gerada por ano"""
    total_data = df.groupby("Year")["Energy"].sum().reset_index()
    fig = create_bar_chart(
        total_data,
        "Year",
        "Energy",
        "Total de Energia Gerada por Ano",
        "Ano",
        "Total de Energia Gerada (kWh)",
    )
    st.plotly_chart(fig)


def display_home_page(df):
    """Exibe um resumo total dos dados de energia"""

    col1, col2, col3 = st.columns(3)

    with col1:
        display_total_performance_indicators(df)
    with col2:
        display_revenue_summary(df)
    with col3:
        display_environmental_benefits(df)

    plot_total_by_year(df)


def display_total_performance_indicators(df):
    """Exibe os indicadores de desempenho total da usina."""

    # Cálculos principais
    system_capacity_kw = 4.4
    total_energy_kwh = df["Energy"].sum()
    total_energy_mwh = total_energy_kwh / 1000
    current_year = pd.Timestamp.now().year
    current_month = pd.Timestamp.now().month

    current_month_energy_kwh = df[
        (df["Year"] == current_year) & (df["Month"] == current_month)
    ]["Energy"].sum()
    current_month_energy_mwh = current_month_energy_kwh / 1000

    current_year_energy_kwh = df[df["Year"] == current_year]["Energy"].sum()
    current_year_energy_mwh = current_year_energy_kwh / 1000

    total_hours = len(df) * 24  # Número total de horas no período (aproximado)
    max_possible_energy_kwh = system_capacity_kw * total_hours
    efficiency = (
        (total_energy_kwh / max_possible_energy_kwh) * 100
        if max_possible_energy_kwh > 0
        else 0
    )
    std_dev_energy = df["Energy"].std()

    rows_data = [
        {
            "icon": images_base64["icon-power-month"],
            "label": "Energia este mês:",
            "value": locale.format_string(
                "%.2f", current_month_energy_mwh, grouping=True
            ),
            "unit": "kWh",
        },
        {
            "icon": images_base64["icon-power-year"],
            "label": "Energia este ano:",
            "value": locale.format_string(
                "%.2f", current_year_energy_mwh, grouping=True
            ),
            "unit": "kWh",
        },
        {
            "icon": images_base64["icon-power-total"],
            "label": "Energia Total:",
            "value": locale.format_string("%.2f", total_energy_mwh, grouping=True),
            "unit": "MWh",
        },
        {
            "icon": images_base64["icon-power-year"],
            "label": "Desvio Padrão:",
            "value": locale.format_string("%.2f", std_dev_energy, grouping=True),
            "unit": "kWh",
        },
        {
            "icon": images_base64["icon-power-year"],
            "label": "Eficiência (%):",
            "value": locale.format_string("%.2f", efficiency, grouping=True),
            "unit": "%",
        },
    ]

    card = create_card_html("Energia", rows_data)
    components.html(card, height=400)


def display_revenue_summary(df):
    """Exibe o resumo de receita com base nos dados de energia."""

    # Cálculos principais
    total_energy_kwh = df["Energy"].sum()
    electricity_price_per_kwh = 1.00  # Preço da eletricidade (R$/kWh)
    current_year = pd.Timestamp.now().year
    current_month = pd.Timestamp.now().month

    current_month_energy_kwh = df[
        (df["Year"] == current_year) & (df["Month"] == current_month)
    ]["Energy"].sum()

    total_revenue = total_energy_kwh * electricity_price_per_kwh
    current_month_revenue = current_month_energy_kwh * electricity_price_per_kwh

    # Dados para o card
    rows_data = [
        {
            "icon": images_base64["icon-income-today"],
            "label": "Este mês:",
            "value": locale.format_string("%.2f", current_month_revenue, grouping=True),
            "unit": "R$",
        },
        {
            "icon": images_base64["icon-income-month"],
            "label": "Total:",
            "value": locale.format_string("%.2f", total_revenue, grouping=True),
            "unit": "R$",
        },
    ]

    card_html = create_card("Receita da Usina", rows_data)
    components.html(card_html, height=200)  # Altura ajustável conforme necessário


def display_environmental_benefits(df):
    """Exibe os benefícios ambientais com cards renderizados corretamente."""
    # Cálculos
    total_energy_kwh = df["Energy"].sum()
    total_co2_reduction_ton = (total_energy_kwh * 1.0) / 1000  # 1 kg CO2/kWh
    total_trees = total_energy_kwh * 1.0 / 18.32  # 18.32 kg CO2/árvore/ano

    # Dados para o card
    rows_data = [
        {
            "icon": images_base64["icon-co2"],
            "label": "Redução da emissão de CO2:",
            "value": f"{total_co2_reduction_ton:,.2f}",
            "unit": "Tonelada(s)",
        },
        {
            "icon": images_base64["icon-tree"],
            "label": "Neutralização de carbono:",
            "value": f"{total_trees:,.2f}",
            "unit": "Árvores",
        },
    ]

    # Gerar e renderizar o card
    card_html = create_card("Benefícios Ambientais", rows_data)
    components.html(card_html, height=200)  # Altura ajustável conforme necessário


def create_bar_chart(data, x, y, title, xlabel, ylabel):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels={x: xlabel, y: ylabel},
        template="plotly_dark",
    )
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="white")),
        xaxis=dict(
            title=xlabel,
            showgrid=False,
            tickmode="linear",
            ticks="outside",
            tickwidth=2,
            tickangle=45,
            tickfont=dict(color="#ffffff"),
        ),
        yaxis=dict(
            title=ylabel,
            showgrid=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="gray",
            tickfont=dict(color="#ffffff"),
        ),
        plot_bgcolor="#181818",
        paper_bgcolor="#181818",
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig


def create_bar_chart_2(
    data,
    *,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = None,
    ylabel: str = None,
    template: str = "plotly_dark",
    margin: dict = None,
    **layout_kwargs,
):
    """Cria um gráfico de barras altamente customizável.

    Args:
        data: DataFrame com os dados
        x (str): Coluna para eixo X
        y (str): Coluna para eixo Y
        title (str): Título do gráfico (opcional)
        xlabel (str): Label do eixo X (padrão: nome da coluna X)
        ylabel (str): Label do eixo Y (padrão: nome da coluna Y)
        template (str): Template do Plotly (padrão: "plotly_dark")
        margin (dict): Margens do gráfico (padrão: dict(l=40, r=40, t=40, b=40))
        **layout_kwargs: Argumentos adicionais para update_layout()

    Returns:
        plotly.graph_objects.Figure
    """
    # Valores padrão inteligentes
    xlabel = xlabel or x
    ylabel = ylabel or y
    margin = margin or dict(l=40, r=40, t=40, b=40)

    # Criação do gráfico base
    fig = px.bar(
        data, x=x, y=y, title=title, labels={x: xlabel, y: ylabel}, template=template
    )

    # Customização do layout
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16, color="white")),
        xaxis=dict(
            title=xlabel,
            showgrid=False,
            tickmode="linear",
            ticks="outside",
            tickwidth=2,
            tickangle=45,
            tickfont=dict(color="#ffffff"),
        ),
        yaxis=dict(
            title=ylabel,
            showgrid=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="gray",
            tickfont=dict(color="#ffffff"),
        ),
        plot_bgcolor="#181818",
        paper_bgcolor="#181818",
        margin=margin,
        **layout_kwargs,
    )

    return fig


# # Uso básico (igual ao anterior)
# fig = create_bar_chart(
#     data=df,
#     x="category",
#     y="value",
#     title="Meu Gráfico",
#     xlabel="Categorias",
#     ylabel="Valores"
# )

# # Com customizações adicionais
# fig = create_bar_chart(
#     data=df,
#     x="date",
#     y="sales",
#     title="Vendas por Data",
#     template="plotly_white",
#     margin=dict(l=60, r=30, t=80, b=60),
#     hovermode="x unified"
# )

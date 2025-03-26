import base64
import locale
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# Caminho base para os ícones
base_dir = os.path.dirname(os.path.abspath(__file__))
icons_dir = os.path.join(base_dir, "../assets/icons")


def get_card_style():
    """Retorna o estilo CSS para os cards."""
    return """
    <style>
    .card {
        background-color: #1e1e1e;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        overflow: hidden; /* Garante que o conteúdo não ultrapasse as bordas arredondadas */
    }
    .card-header {
        padding: 15px;
        text-align: center;
    }
    .card-header h3 {
        color: #ffffff;
        margin: 0;
    }
    .card-header hr {
        border: 0;
        height: 1px;
        background: #444444; /* Cor da linha abaixo do título */
        margin: 10px 0 0 0; /* Margem apenas acima da linha */
    }
    .card-content {
        padding: 20px; /* Espaçamento interno para o conteúdo */
    }
    .card-content .row {
        display: flex; /* Garante que os itens fiquem lado a lado */
        justify-content: space-between; /* Espaço entre o texto e o valor */
        align-items: center; /* Alinha os itens verticalmente */
        margin: 5px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid #444444; /* Linha separadora */
    }
    .card-content .row .label {
        color: #ffffff;
        font-weight: normal;
        text-align: left;
        flex: 1; /* O texto ocupa o espaço à esquerda */
    }
    .card-content .row .value {
        color: #00ff00; /* Cor verde para os valores */
        font-weight: bold;
        text-align: right;
        flex: 0; /* O valor ocupa o espaço à direita */
    }
    .title {
        color: grey;
        font-size: 12px; /* Ajuste o tamanho da fonte */
        margin-left: 5px; /* Adiciona um pequeno espaçamento à esquerda */
        vertical-align: middle; /* Alinha verticalmente com o valor */
    }
    </style>
    """


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
    "icon_energy": load_image_as_base64(
        os.path.join(icons_dir, "icon-energy.svg")
    ),
    # Adicione mais imagens conforme necessário
}

# Configure locale to format Brazilian currency
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


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
    # Capacidade máxima do sistema (em kW)
    system_capacity_kw = 4.4

    # Calcular o total de energia gerada (kWh)
    total_energy_kwh = df["Energy"].sum()

    # Preço da unidade da eletricidade (R$/kWh)
    electricity_price_per_kwh = 1.00

    # Calcular o total de energia gerada (kWh e MWh)
    total_energy_kwh = df["Energy"].sum()
    total_energy_mwh = total_energy_kwh / 1000

    # Calcular o total de energia gerada no mês atual
    current_year = pd.Timestamp.now().year
    current_month = pd.Timestamp.now().month
    current_month_data = df[
        (df["Year"] == current_year) & (df["Month"] == current_month)
    ]
    current_month_energy_kwh = current_month_data["Energy"].sum()
    current_month_energy_mwh = current_month_energy_kwh / 1000
    current_year_energy_kwh = df[df["Year"] == current_year]["Energy"].sum()
    current_year_energy_mwh = current_year_energy_kwh / 1000

    # Calcular a eficiência com base na capacidade máxima do sistema
    total_hours = len(df) * 24  # Número total de horas no período (aproximado)
    max_possible_energy_kwh = system_capacity_kw * total_hours
    efficiency = (
        (total_energy_kwh / max_possible_energy_kwh) * 100
        if max_possible_energy_kwh > 0
        else 0
    )

    # Calcular a receita total e a receita do mês atual
    total_revenue = (
        total_energy_kwh * electricity_price_per_kwh
    )  # Receita total (R$)
    current_month_revenue = (
        current_month_energy_kwh * electricity_price_per_kwh
    )  # Receita do mês atual (R$)

    # Fatores de conversão
    co2_emission_factor = 1.0  # kg de CO2 evitados por kWh
    carbon_absorption_per_tree = (
        18.32  # kg de CO2 absorvidos por árvore por ano
    )

    # Calcular o total de energia gerada (kWh)
    total_energy_kwh = df["Energy"].sum()

    # Calcular a redução de emissão de CO2 (em toneladas)
    total_co2_reduction_kg = total_energy_kwh * co2_emission_factor
    total_co2_reduction_ton = (
        total_co2_reduction_kg / 1000
    )  # Conversão para toneladas

    # Calcular a neutralização de carbono (número de árvores)
    total_trees = total_co2_reduction_kg / carbon_absorption_per_tree

    std_dev_energy = df["Energy"].std()

    st.markdown(get_card_style(), unsafe_allow_html=True)

    plant_overview_card = f"""
    <div class="card">
        <div class="card-header">
            <h3>Visão geral da usina</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-month']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label">
                    <strong>Energia este mês:</strong>
                </span>
                <span class="value">
                    {locale.format_string('%.2f', current_month_energy_mwh, grouping=True)}
                </span>
                <span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Energia este ano:</strong></span>
                <span class="value">{locale.format_string('%.2f', current_year_energy_mwh, grouping=True)}</span><span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-total']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Energia Total:</strong></span>
                <span class="value">{locale.format_string('%.2f', total_energy_mwh, grouping=True)}</span><span class="title">MWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Desvio Padrão:</strong></span>
                <span class="value">{locale.format_string('%.2f', std_dev_energy, grouping=True)}</span><span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Eficiência (%):</strong></span>
                <span class="value">{locale.format_string('%.2f', efficiency, grouping=True)}</span><span class="title">kWh</span>
            </div>
        </div>
    </div>
    """

    plant_revenue_card = f"""
    <div class="card">
        <div class="card-header">
            <h3>Receita da usina</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-income-today']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Este mês:</strong></span>
                <span class="value">
                    <span class="title">R$</span> {locale.format_string('%.2f', current_month_revenue, grouping=True)}
                </span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-income-month']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Total:</strong></span>
                <span class="value">
                    <span class="title">R$</span> {locale.format_string('%.2f', total_revenue, grouping=True)}
                </span>
            </div>
        </div>
    </div>
    """

    environmental_benefits_card = f"""
    <div class="card">
        <div class="card-header">
            <h3>Benefícios ambientais</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-co2']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label">
                    <strong>Redução da emissão de CO2:</strong>
                </span>
                <span class="value">
                    {locale.format_string('%.2f', total_co2_reduction_ton, grouping=True)}
                </span>
                <span class="title">Tonelada(s)</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-tree']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Neutralização de carbono:</strong></span>
                <span class="value">{locale.format_string('%.2f', total_trees, grouping=True)}</span>
                <span class="title">Árvores</span>
            </div>
        </div>
    </div>
    """

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

    # HTML do card
    card_content = f"""
    <div class="card">
        <div class="card-header">
            <h3>Visão geral da usina</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-month']}" alt="Ícone Energia Mês" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Energia este mês:</strong></span>
                <span class="value">{locale.format_string('%.2f', current_month_energy_mwh, grouping=True)}</span>
                <span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone Energia Ano" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Energia este ano:</strong></span>
                <span class="value">{locale.format_string('%.2f', current_year_energy_mwh, grouping=True)}</span>
                <span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-total']}" alt="Ícone Energia Total" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Energia Total:</strong></span>
                <span class="value">{locale.format_string('%.2f', total_energy_mwh, grouping=True)}</span>
                <span class="title">MWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone Desvio Padrão" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Desvio Padrão:</strong></span>
                <span class="value">{locale.format_string('%.2f', std_dev_energy, grouping=True)}</span>
                <span class="title">kWh</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-power-year']}" alt="Ícone Eficiência" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Eficiência (%):</strong></span>
                <span class="value">{locale.format_string('%.2f', efficiency, grouping=True)}</span>
                <span class="title">%</span>
            </div>
        </div>
    </div>
    """

    # Renderizar o card no Streamlit
    st.markdown(card_content, unsafe_allow_html=True)


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

    # HTML do card
    card_content = f"""
    <div class="card">
        <div class="card-header">
            <h3>Receita da usina</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-income-today']}" alt="Ícone Receita Mês" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Este mês:</strong></span>
                <span class="value">
                    <span class="title">R$</span> {locale.format_string('%.2f', current_month_revenue, grouping=True)}
                </span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-income-month']}" alt="Ícone Receita Total" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Total:</strong></span>
                <span class="value">
                    <span class="title">R$</span> {locale.format_string('%.2f', total_revenue, grouping=True)}
                </span>
            </div>
        </div>
    </div>
    """

    # Renderizar o card no Streamlit
    st.markdown(card_content, unsafe_allow_html=True)


def display_environmental_benefits(df):
    """Exibe os benefícios ambientais com base nos dados de energia."""

    # Cálculos principais
    total_energy_kwh = df["Energy"].sum()
    co2_emission_factor = 1.0  # kg de CO2 evitados por kWh
    carbon_absorption_per_tree = 18.32  # kg de CO2 absorvidos por árvore por ano

    total_co2_reduction_ton = (total_energy_kwh * co2_emission_factor) / 1000
    total_trees = total_energy_kwh * co2_emission_factor / carbon_absorption_per_tree

    # HTML do card
    card_content = f"""
    <div class="card">
        <div class="card-header">
            <h3>Benefícios ambientais</h3>
            <hr>
        </div>
        <div class="card-content">
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-co2']}" alt="Ícone CO2" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Redução da emissão de CO2:</strong></span>
                <span class="value">{locale.format_string('%.2f', total_co2_reduction_ton, grouping=True)}</span>
                <span class="title">Tonelada(s)</span>
            </div>
            <div class="row">
                <img src="data:image/svg+xml;base64,{images_base64['icon-tree']}" alt="Ícone Árvore" style="width: 20px; height: 20px; margin-right: 10px; margin-left: 5px;">
                <span class="label"><strong>Neutralização de carbono:</strong></span>
                <span class="value">{locale.format_string('%.2f', total_trees, grouping=True)}</span>
                <span class="title">Árvores</span>
            </div>
        </div>
    </div>
    """

    # Renderizar o card no Streamlit
    st.markdown(card_content, unsafe_allow_html=True)

import html

import streamlit as st

from config.constants import FontCards
from utils.helpers import load_icon_as_base64


def format_value(value: float | int | str) -> str:
    """Formata valores numéricos para o padrão brasileiro."""
    if isinstance(value, (int, float)):
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(value)


def generate_card_css(
    card_width: str,
    card_height: str,
    card_background_color: str,
    title_style: dict,
    value_style: dict,
) -> str:
    """Gera o CSS do card de forma modular."""
    return f"""
    <style>
    /* Zera padding do layout Streamlit */
    [data-testid="stAppViewContainer"] > .main {{
        padding: 0;
    }}

    .card-wrapper {{
        padding: 0;
        margin: 0;
    }}

    .card {{
        background-color: {card_background_color};
        padding: 15px;
        border-radius: 8px;
        width: 100%;
        max-width: {card_width};
        min-width: 200px;
        height: auto;
        max-height: {card_height};
        overflow: hidden;
        font-family: Arial, sans-serif;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    }}

    .card-icon {{
        width: 50px;
        height: 50px;
        margin-right: 20px;
        flex-shrink: 0;
    }}

    .card-content {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
    }}

    .title {{
        font-size: {title_style['size']};
        font-family: {title_style['family']};
        font-weight: bold;
        color: {title_style['color']};
    }}

    .value {{
        font-size: {value_style['size']};
        font-family: {value_style['family']};
        color: {value_style['color']};
        margin-top: 4px;
    }}

    .unit {{
        font-size: 0.9rem;
        color: #34495E;
        margin-left: 4px;
    }}
    </style>
    """


def build_card_html(icon_base64: str, title: str, value: str, unit: str) -> str:
    """Monta o HTML do card."""
    return f"""
    <div class="card-wrapper">
        <div class="card">
            <img class="card-icon" src="data:image/svg+xml;base64,{icon_base64}" alt="Icon">
            <div class="card-content">
                <div class="title">{title}</div>
                <div class="value">{value} <span class="unit">{unit}</span></div>
            </div>
        </div>
    </div>
    """


def card_info_2(
    icon_name: str,
    main_title: str,
    value: float | int | str,
    unit: str = "unit",
    card_height: str = "200px",
    card_width: str = "250px",
    card_background_color: str = "#f4f5f7",
    title_style: dict = FontCards.TITLE,
    value_style: dict = FontCards.PRIMARY_VALUE,
) -> None:
    """
    Renderiza um card compacto com ícone, título e valor principal com unidade.
    """
    icon_base64 = load_icon_as_base64(icon_name)
    formatted_value = format_value(value)

    html_css = generate_card_css(
        card_width, card_height, card_background_color, title_style, value_style
    )

    card_html = build_card_html(
        icon_base64, html.escape(main_title), formatted_value, html.escape(unit)
    )

    st.markdown(html_css, unsafe_allow_html=True)
    st.markdown(card_html, unsafe_allow_html=True)

import html
from typing import Literal

import streamlit as st

from config.constants import FontCards
from utils.helpers import load_icon_as_base64


def render_secondary_value(
    value: float, unit: str, position: Literal["left", "right"]
) -> str:
    """Renderiza o valor secundário com a unidade à esquerda ou à direita."""
    if position == "left":
        return f'<div class="secondary-value"><span class="secondary-unit">{unit}</span> {value}</div>'
    return f'<div class="secondary-value">{value} <span class="secondary-unit">{unit}</span></div>'


def render_icon_html(icon_base64: str | None) -> str:
    """Renderiza o ícone (base64) ou um fallback SVG."""
    if icon_base64:
        return f'<img src="data:image/svg+xml;base64,{icon_base64}" alt="Icon" class="icon">'
    return '<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#6c757d"><circle cx="12" cy="12" r="10"/></svg>'


def generate_card_css(
    card_background_color: str,
    card_width: str,
    card_height: str,
    icon_size: str,
    title_style: dict,
    subtitle_style: dict,
    primary_value_style: dict,
    secondary_value_style: dict,
    primary_unit_style: dict,
    secondary_unit_style: dict,
) -> str:
    """Gera o CSS para estilizar o card."""
    return f"""
    <style>
    .card {{
        background-color: {card_background_color};
        padding: 15px;
        border-radius: 8px;
        width: clamp(220px, 100%, {card_width});
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
    .icon {{
        width: {icon_size};
        height: {icon_size};
        margin-right: 10px;
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
    .subtitle-container {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 10px;
        border-top: 1px solid #ddd;
        padding-top: 3px;
        margin-top: 3px;
        width: calc(100% - 20px);
        margin-left: auto;
        margin-right: auto;
    }}
    .subtitle {{
        font-size: {subtitle_style['size']};
        font-family: {subtitle_style['family']};
        color: {subtitle_style['color']};
        margin-right: 10px;
    }}
    .primary-value {{
        font-size: {primary_value_style['size']};
        font-family: {primary_value_style['family']};
        font-weight: bold;
        color: {primary_value_style['color']};
    }}
    .secondary-value {{
        font-size: {secondary_value_style['size']};
        font-family: {secondary_value_style['family']};
        font-weight: bold;
        color: {secondary_value_style['color']};
    }}
    .primary-unit {{
        font-size: {primary_unit_style['size']};
        font-family: {primary_unit_style['family']};
        color: {primary_unit_style['color']};
    }}
    .secondary-unit {{
        font-size: {secondary_unit_style['size']};
        font-family: {secondary_unit_style['family']};
        color: {secondary_unit_style['color']};
        margin-right: 0.3px;
    }}
    </style>
    """


def card_info(
    title: str,
    subtitle: str,
    primary_value: float,
    secondary_value: float,
    primary_unit: str = "unit",
    secondary_unit: str = "unit",
    card_background_color: str = "#f4f5f7",
    icon_name: str | None = None,
    card_height: str = "200px",
    card_width: str = "250px",
    icon_size: str = "40px",
    title_style: dict = FontCards.TITLE,
    subtitle_style: dict = FontCards.SUBTITLE,
    primary_unit_style: dict = FontCards.PRIMARY_UNIT,
    secondary_unit_style: dict = FontCards.SECONDARY_UNIT,
    primary_value_style: dict = FontCards.PRIMARY_VALUE,
    secondary_value_style: dict = FontCards.SECONDARY_VALUE,
    secondary_unit_position: Literal["left", "right"] = "right",
) -> None:
    """
    Renderiza um card estilizado com informações resumidas, valores e ícone.

    Exibe título, subtítulo, valor principal com unidade, valor secundário com unidade
    e um ícone SVG base64.

    Uso:
        card_info("Consumo", "Janeiro", 120.5, 245.75, "kWh", "R$")
    """
    # Segurança: escapar HTML nos textos
    title = html.escape(title)
    subtitle = html.escape(subtitle)

    # Formatação de valores (duas casas decimais)
    primary_value_fmt = primary_value
    # primary_value_fmt = f"{primary_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    secondary_value_fmt = secondary_value
    # secondary_value_fmt = f"{secondary_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Ícone como base64
    icon_base64 = load_icon_as_base64(icon_name) if icon_name else None

    # Geração de HTML
    css = generate_card_css(
        card_background_color,
        card_width,
        card_height,
        icon_size,
        title_style,
        subtitle_style,
        primary_value_style,
        secondary_value_style,
        primary_unit_style,
        secondary_unit_style,
    )

    secondary_value_html = render_secondary_value(
        secondary_value_fmt, secondary_unit, secondary_unit_position
    )
    icon_html = render_icon_html(icon_base64)

    html_card = f"""
    <div class="card-wrapper">
        <div class="card">
            {icon_html}
            <div class="card-content">
                <div>
                    <span class="title">{title}</span>
                    <div class="primary-value">{primary_value_fmt} <span class="primary-unit">{primary_unit}</span></div>
                </div>
                <div class="subtitle-container">
                    <span class="subtitle">{subtitle}</span>
                    {secondary_value_html}
                </div>
            </div>
        </div>
    </div>
    """

    # Exibe no Streamlit
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html_card, unsafe_allow_html=True)

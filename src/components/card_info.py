import streamlit as st

from config.constants import FontCards
from utils.helpers import load_icon_as_base64


def card_info(
    title: str,
    subtitle: str,
    primary_value: float,
    secondary_value: float,
    primary_unit: str = "unit",
    secondary_unit: str = "unit",
    card_background_color: str = "#f4f5f7",
    icon_name: str = None,
    card_height: str = "200px",
    card_width: str = "250px",
    icon_size: str = "40px",
    title_style: dict = FontCards.TITLE,
    subtitle_style: dict = FontCards.SUBTITLE,
    primary_unit_style: dict = FontCards.PRIMARY_UNIT,
    secondary_unit_style: dict = FontCards.SECONDARY_UNIT,
    primary_value_style: dict = FontCards.PRIMARY_VALUE,
    secondary_value_style: dict = FontCards.SECONDARY_VALUE,
    secondary_unit_position: str = "right",
):
    """
    Function to create a reusable card displaying information with optional customization.

    Args:
        title (str): Title text to display in the card.
        subtitle (str): Subtitle text to display in the card.
        primary_value (float): Primary value to display (e.g., energy consumption).
        secondary_value (float): Secondary value to display (e.g., revenue).
        primary_unit (str): Unit of the primary value (default "kWh").
        secondary_unit (str): Unit of the secondary value (default "R$").
        card_background_color (str): Background color of the card (hexadecimal format).
        icon_name (str): Name of the icon to load as base64 (optional).
        card_height (str): Height of the card (default "200px").
        card_width (str): Width of the card (default "250px").
        icon_size (str): Size of the icon (default "40px").
        title_style (dict): Style for the title text.
        subtitle_style (dict): Style for the subtitle text.
        primary_unit_style (dict): Style for the primary unit text.
        secondary_unit_style (dict): Style for the secondary unit text.
        primary_value_style (dict): Style for the primary value text.
        secondary_value_style (dict): Style for the secondary value text.
        secondary_unit_position (str): Position of the secondary unit, either "left" or "right" (default "right").
    """

    # Load the icon as base64 if provided
    icon_base64 = load_icon_as_base64(icon_name) if icon_name else None

    # CSS style for the card
    card_style = f"""
    <style>
    .card {{
        background-color: {card_background_color};
        padding: 15px;
        border-radius: 8px;
        width: 100%; /* Ajusta o card para ocupar toda a largura disponível */
        max-width: {card_width}; /* Define a largura máxima */
        min-width: 200px; /* Define uma largura mínima */
        height: auto; /* Ajusta a altura automaticamente */
        max-height: {card_height}; /* Define a altura máxima */
        overflow: hidden; /* Esconde o conteúdo que ultrapassa a altura máxima */
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
        width: {icon_size}; /* Tamanho do ícone */
        height: {icon_size};
        margin-right: 10px; /* Espaço entre o ícone e o texto */
        flex-shrink: 0; /* Garante que o ícone não seja redimensionado */
    }}

    .card-content {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%; /* Garante que o conteúdo ocupe toda a largura disponível */
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
        justify-content: space-between;
        border-top: 1px solid #ddd;
        padding-top: 3px;
        margin-top: 3px;
        width: calc(100% - 20px); /* Margem lateral */
        margin-left: auto;
        margin-right: auto;
    }}

    .subtitle {{
        font-size: {subtitle_style['size']};
        font-family: {subtitle_style['family']};
        color: {subtitle_style['color']};
        margin-right: 10px; /* Espaço entre o subtitle e o valor */
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
        margin-right: 0.3px; /* Espaço entre o unit e o value quando estiver à esquerda */
    }}
    </style>
    """

    # HTML for the secondary value and unit with dynamic positioning
    if secondary_unit_position == "left":
        secondary_value_html = f'<div class="secondary-value"><span class="secondary-unit">{secondary_unit}</span> {secondary_value}</div>'
    else:
        secondary_value_html = f'<div class="secondary-value">{secondary_value} <span class="secondary-unit">{secondary_unit}</span></div>'

    # HTML for the card with optional icon
    icon_html = (
        f'<img src="data:image/svg+xml;base64,{icon_base64}" alt="Icon" class="icon">'
        if icon_base64
        else '<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#6c757d"><circle cx="12" cy="12" r="10"/></svg>'
    )

    card_html = f"""
    <div class="card">
        {icon_html}
        <div class="card-content">
            <div>
                <span class="title">{title}</span>
                <div class="primary-value">{primary_value} <span class="primary-unit">{primary_unit}</span></div>
            </div>
            <div class="subtitle-container">
                <span class="subtitle">{subtitle}</span>
                {secondary_value_html}
            </div>
        </div>
    </div>
    """

    # Display the style and the card in Streamlit
    st.markdown(card_style, unsafe_allow_html=True)
    st.markdown(card_html, unsafe_allow_html=True)

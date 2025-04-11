import streamlit as st

from config.constants import FontCards
from utils.helpers import load_icon_as_base64


def card_info_2(
    icon_name: str,
    main_title: str,
    value,
    unit: str = "unit",
    card_height: str = "200px",
    card_width: str = "250px",
    card_background_color: str = "#f4f5f7",
    title_style: dict = FontCards.TITLE,
):
    icon_base64 = load_icon_as_base64(icon_name)

    card_html = f"""
    <style>
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

    .value {{
        font-size: 1.5rem;
        font-weight: bold;
        color: #34495E;
    }}

    .unit {{
        font-size: 0.9rem;
        color: #34495E;
    }}
    </style>

    <div class="card">
        <img class="card-icon" src="data:image/svg+xml;base64,{icon_base64}" alt="Icon">
        <div class="card-content">
            <div class="title">{main_title}</div>
            <div class="value">{value} <span class="unit">{unit}</span></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

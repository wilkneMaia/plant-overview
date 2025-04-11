import streamlit as st

from utils.helpers import load_icon_as_base64


def create_custom_card_2(icon_name, main_title, value, unit):
    icon_base64 = load_icon_as_base64(icon_name)

    card_html = f"""
    <style>
    .custom-card {{
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: #F0F4F8;
        color: #2C3E50;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    .card-icon {{
        width: 50px;
        height: 50px;
        margin-right: 20px;
    }}

    .card-content {{
        display: flex;
        flex-direction: column;
    }}

    .main-title {{
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-bottom: 8px;
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

    <div class="custom-card">
        <img class="card-icon" src="data:image/svg+xml;base64,{icon_base64}" alt="Icon">
        <div class="card-content">
            <div class="main-title">{main_title}</div>
            <div class="value">{value} <span class="unit">{unit}</span></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

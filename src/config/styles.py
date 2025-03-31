import streamlit as st


def setup_shared_styles():
    """Configura estilos CSS compartilhados entre todas as páginas"""
    st.markdown(
        """
        <style>
            [data-testid="stMetric"] {
                background-color: rgba(28, 131, 106, 0.1);
                border: 1px solid rgba(28, 131, 106, 0.1);
                padding: 5% 5% 5% 10%;
                border-radius: 5px;
            }
            [data-testid="stMetricLabel"] {
                opacity: 0.6;
                font-size: 0.95rem;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.5rem;
            }
            .stPlotlyChart {
                border: 1px solid rgba(151, 166, 195, 0.1);
                border-radius: 5px;
                padding: 0 1rem;
            }
            .stTabs [role="tablist"] {
                margin-bottom: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

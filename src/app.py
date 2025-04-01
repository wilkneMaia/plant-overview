import time

import streamlit as st

from utils.load_data import load_data
from utils.router import Router

# Configuração avançada da página
st.set_page_config(
    layout="wide",
    page_title="Sistema de Energia",
    page_icon="⚡",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://example.com",
        "Report a bug": "mailto:support@example.com",
    },
)


def main():
    router = Router()

    # Sidebar melhorada
    with st.sidebar:
        with st.expander("🗂️ Navegação", expanded=True):
            selected = st.radio(
                "Selecione a página",
                options=["Home", "Semana", "Mês", "Ano"],
                key="page_selector",
                label_visibility="collapsed",
            )

        with st.expander("⚙️ Configurações", expanded=True):
            uploaded_file = st.file_uploader(
                "Upload de CSV",
                type=["csv"],
                help="Carregue o arquivo de dados energéticos",
            )

            if uploaded_file is not None:
                with st.spinner("Processando..."):
                    try:
                        progress_bar = st.progress(0)
                        for percent in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(percent + 1)

                        data = load_data(uploaded_file)
                        st.session_state.df = data
                        st.toast("Arquivo carregado!", icon="✅")
                        progress_bar.empty()

                    except Exception as e:
                        st.error(f"Erro: {e!s}")
                        st.stop()

        # Seção de pré-visualização
        if "df" in st.session_state:
            with st.expander("📊 Visualização Rápida"):
                st.write(f"**Registros:** {len(st.session_state.df):,}")
                if st.checkbox("Mostrar amostra"):
                    st.dataframe(st.session_state.df.head(3))

        # Debug (opcional)
        with st.expander("🐞 Debug", False):
            if st.button("Limpar cache"):
                st.session_state.clear()
                st.rerun()

    # Validação de dados
    if "df" not in st.session_state:
        st.warning("Por favor, carregue um arquivo CSV")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
            <div style='
                border: 2px dashed #ccc;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: #f8f9fa;
                margin: 20px 0;
            '>
                <div style='font-size: 50px'>📁</div>
                <h3 style='color: #495057'>Nenhum dado carregado</h3>
                <p style='color: #6c757d'>Faça upload de um arquivo CSV para começar</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
            ### Como começar?
            1. Clique em `Browse files` na sidebar
            2. Selecione seu arquivo CSV
            3. Aguarde o processamento
            """
            )
        return

    # Barra de status
    # if "df" in st.session_state:
    #     status_cols = st.columns(3)
    #     with status_cols[0]:
    #         st.metric("Registros", len(st.session_state.df))
    #     with status_cols[1]:
    #         st.metric(
    #             "Período",
    #             f"{st.session_state.df['Date'].min().date()} a {st.session_state.df['Date'].max().date()}",
    #         )
    #     with status_cols[2]:
    #         st.metric(
    #             "Energia Total", f"{st.session_state.df['Energy'].sum():,.1f} kWh"
    #         )
    #     st.divider()

    # Container principal
    main_container = st.container()
    with main_container:
        router.navigate(selected, st.session_state.df)
        st.markdown(
            "<div style='height: 100px;'></div>", unsafe_allow_html=True
        )  # Espaço no rodapé


if __name__ == "__main__":
    main()

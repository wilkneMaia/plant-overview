import pandas as pd
import streamlit as st

from utils.load_data import load_data
from utils.router import Router

# ⚠️ DEVE SER O PRIMEIRO COMANDO STREAMLIT (antes de qualquer função/def)
st.set_page_config(layout="wide", page_title="Sistema de Energia", page_icon="⚡")


def main():
    # Inicializa o roteador

    router = Router()

    # Sidebar - Menu de navegação e upload de arquivo
    with st.sidebar:
        st.title("Navegação")
        selected = st.radio(
            "Selecione a página",
            options=["Home", "Energia", "Ambiental"],
            key="page_selector",
        )

        st.title("Configurações")
        uploaded_file = st.file_uploader("Faça upload do arquivo CSV", type=["csv"])

        if uploaded_file is not None:
            try:
                data = load_data(uploaded_file)
                # st.write(f"Tipo do objeto retornado: {type(data).__name__}")
                st.session_state.df = data

                if isinstance(data, pd.DataFrame):
                    st.success("Arquivo carregado com sucesso!")
                else:
                    st.error("O arquivo não é um DataFrame válido.")
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {e!s}")

    # Verificação de dados
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("Por favor, carregue um arquivo CSV para continuar")
        return

    # Roteamento
    router.navigate(selected, st.session_state.df)


if __name__ == "__main__":
    main()  # Chamada da função principal

import pandas as pd
import streamlit as st

from utils.load_data import load_data
from utils.router import Router


def main():
    # Configurações gerais da aplicação
    st.set_page_config(layout="wide", page_title="Sistema de Energia", page_icon="⚡")

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
                data = load_data(uploaded_file)  # Chame a função corretamente
                st.write(
                    f"Tipo do objeto retornado: {type(data).__name__}"
                )  # Exibe apenas o nome da classe
                st.session_state.df = data  # Salve os dados no estado da sessão
                if isinstance(data, pd.DataFrame):
                    # Verificação de sucesso
                    st.success("O arquivo foi carregado com sucesso!")
                    # st.write("Prévia dos dados carregados:")
                    # st.dataframe(data.head())  # Exibe as primeiras linhas do DataFrame
                    # Verificação de colunas
                    # required_columns = ["Energy", "Year", "Month"]
                    # if all(col in data.columns for col in required_columns):
                    #     st.success("O arquivo contém todas as colunas necessárias!")
                    # else:
                    #     st.error(f"O arquivo está faltando as colunas necessárias: {required_columns}")
                    # if not pd.api.types.is_numeric_dtype(data["Energy"]):
                    #     st.error("A coluna 'Energy' não contém valores numéricos.")
                else:
                    st.error("O arquivo carregado não é um DataFrame válido.")
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {str(e)}")

    # Verificação de dados carregados
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("Por favor, carregue um arquivo CSV para continuar")
        return

    # Roteamento para a página selecionada
    router.navigate(selected, st.session_state.df)


if __name__ == "__main__":
    main()

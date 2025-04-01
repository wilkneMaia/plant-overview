import pandas as pd
import streamlit as st

from utils.router import Router

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema de Energia", page_icon="⚡")


def load_fixed_data():
    """Carrega e valida o arquivo fixo"""
    try:
        # Carrega os dados
        data = pd.read_csv("data/arquivo_3.csv")

        # Verifica colunas obrigatórias
        required_columns = {
            "Plant Name",
            "Date",
            "Sn",
            "Port",
            "Energy (kWh)",
            "ID",
            "SN",
            "Microinversor",
        }

        missing_cols = required_columns - set(data.columns)
        if missing_cols:
            raise ValueError(f"Colunas faltando: {missing_cols}")

        # Pré-processamento básico
        data["Date"] = pd.to_datetime(data["Date"])
        data["Year"] = data["Date"].dt.year

        return data

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e!s}")
        st.error(f"Colunas encontradas: {list(data.columns)}")
        return None


def main():
    # Carrega os dados
    if "df" not in st.session_state:
        st.session_state.df = load_fixed_data()
        if st.session_state.df is not None:
            st.session_state.available_years = sorted(
                st.session_state.df["Year"].unique()
            )

    # Roteador
    router = Router()

    # Sidebar
    with st.sidebar:
        st.title("Navegação")
        selected = st.radio(
            "Selecione a página",
            options=["Home", "Energia", "Ambiental"],
            key="page_selector",
        )

        # Filtro de anos (se os dados foram carregados)
        if "available_years" in st.session_state:
            year_range = st.slider(
                "Selecione o intervalo de anos:",
                min_value=min(st.session_state.available_years),
                max_value=max(st.session_state.available_years),
                value=(
                    min(st.session_state.available_years),
                    max(st.session_state.available_years),
                ),
            )
        else:
            st.warning("Dados não carregados")

    # Verificação de dados
    if st.session_state.df is None:
        st.error("Não foi possível carregar os dados. Verifique o arquivo CSV.")
        return

    # Aplica filtro de anos
    filtered_data = (
        st.session_state.df[st.session_state.df["Year"].between(*year_range)]
        if "available_years" in st.session_state
        else st.session_state.df
    )

    # Roteamento com dados filtrados
    router.navigate(selected, filtered_data)


if __name__ == "__main__":
    main()

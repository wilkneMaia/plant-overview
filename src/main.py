import streamlit as st

from data_loader import load_data
from visualizations import display_home_page


def main():
    st.set_page_config(
        page_title="Dashboard de Geração de Energia",
        page_icon="🌳",
        layout="wide",
    )

    uploaded_file = st.sidebar.file_uploader(
        "Selecione um arquivo CSV", type="csv"
    )

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        filter_option = st.sidebar.radio(
            "Selecione a visualização",
            ["Início", "Semana", "Mês", "Ano"],
            key="filter_option",
        )

        if filter_option == "Início":
            # Criar colunas para exibir os displays lado a lado
            display_home_page(df)

        elif filter_option == "Semana":
            selected_week = st.sidebar.number_input(
                "Selecione uma semana",
                min_value=df["Week"].min(),
                max_value=df["Week"].max(),
            )
            filtered_df = df[df["Week"] == selected_week]
        elif filter_option == "Mês":
            selected_month = st.sidebar.number_input(
                "Selecione um mês",
                min_value=df["Month"].min(),
                max_value=df["Month"].max(),
            )
            filtered_df = df[df["Month"] == selected_month]
        else:
            selected_year = st.sidebar.number_input(
                "Selecione um ano",
                min_value=df["Year"].min(),
                max_value=df["Year"].max(),
            )
            filtered_df = df[df["Year"] == selected_year]

        st.sidebar.markdown("---")

        # if not filtered_df.empty:
        #     st.sidebar.markdown("### Dados selecionados:")
        #     st.sidebar.write(filtered_df[["Date", "Energy", "Month", "Month_Year", "Week", "Year"]])

        #     st.sidebar.markdown("---")

        #     st.sidebar.markdown("### Visualizações:")
        # chart_type = st.sidebar.radio("Selecione o tipo de gráfico", ["Barra", "Linha"])

        # if chart_type == "Barra":
        #     create_bar_chart(filtered_df, "Date", "Energy", "Geração de Energia")
        # else:
        #     create_line_chart(filtered_df, "Date", "Energy", "Geração de Energia")


if __name__ == "__main__":
    main()

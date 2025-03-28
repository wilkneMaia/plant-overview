import streamlit as st


class MonthView:
    def display(self, data):
        """Exibe a página inicial com os dados"""
        st.title("Página Inicial")

        # Exemplo de métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Energia", f"{data['Energy'].sum():,.2f} kWh")
        with col2:
            st.metric("Média Mensal", f"{data['Energy'].mean():,.2f} kWh")

        # Gráfico de exemplo
        st.line_chart(data.set_index("Date")["Energy"])

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(uploaded_file):
    """Carrega e processa os dados do arquivo CSV"""
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    df.rename(columns={"Energy (kWh)": "Energy"}, inplace=True)  # Renomeia a coluna
    df["Date"] = pd.to_datetime(df["Date"])  # Converter para datetime
    df["Day"] = df["Date"].dt.day  # Adiciona a coluna de dias do mês
    df["Month"] = df["Date"].dt.month  # Adiciona a coluna do mês
    df["Month_Year"] = df["Date"].dt.strftime("%Y-%m")  # Adiciona a coluna Ano-Mês
    df["Year"] = df["Date"].dt.year  # Adiciona a coluna do ano
    df["Week"] = df["Date"].dt.isocalendar().week  # Adiciona a coluna de semana do ano
    return df

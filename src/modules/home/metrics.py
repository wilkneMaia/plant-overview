import logging

import pandas as pd
import streamlit as st

from config.constants import Colors

logging.basicConfig(level=logging.INFO)


# Calcula o desvio padrão
def calculate_energy_std_dev(data: pd.DataFrame) -> float:
    """
    Calcula o desvio padrão da energia gerada.

    Args:
        data (pd.DataFrame): DataFrame contendo a coluna 'Energy'.

    Returns:
        float: Desvio padrão da energia gerada.
    """
    return data["Energy"].std()


# Calcula a eficiência média
def calculate_efficiency(data: pd.DataFrame) -> float:
    """
    Calcula a eficiência média por microinversor.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Energy' e 'Microinversor'.

    Returns:
        float: Eficiência média por microinversor.

    Raises:
        ValueError: Se as colunas necessárias não estiverem presentes no DataFrame.

    Exemplo:
        >>> data = pd.DataFrame({
        ...     "Energy": [100, 200, 300],
        ...     "Microinversor": ["A", "B", "A"]
        ... })
        >>> calculate_efficiency(data)
        150.0
    """
    if "Energy" not in data.columns or "Microinversor" not in data.columns:
        raise ValueError(
            "O DataFrame deve conter as colunas 'Energy' e 'Microinversor'."
        )
    return data["Energy"].sum() / data["Microinversor"].nunique()


# Calcula o coeficiente de variação
def calculate_coefficient_of_variation(data: pd.DataFrame) -> float:
    """
    Calcula o coeficiente de variação da energia gerada.

    Args:
        data (pd.DataFrame): DataFrame contendo a coluna 'Energy'.

    Returns:
        float: Coeficiente de variação (em porcentagem).
    """
    mean_energy = data["Energy"].mean()
    std_dev = data["Energy"].std()
    return (std_dev / mean_energy) * 100 if mean_energy > 0 else 0


# Calcula a energia gerada no mês atual
def calculate_current_month_energy(data: pd.DataFrame) -> float:
    """
    Calcula a energia gerada no mês atual.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Year', 'Month' e 'Energy'.

    Returns:
        float: Energia gerada no mês atual.
    """
    required_columns = {"Year", "Month", "Energy"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"O DataFrame deve conter as colunas {required_columns}.")

    current_year, current_month = pd.Timestamp.now().year, pd.Timestamp.now().month
    filtered_data = data[
        (data["Year"] == current_year) & (data["Month"] == current_month)
    ]

    if filtered_data.empty:
        return 0.0  # Retorna 0 se não houver dados para o mês atual

    return filtered_data["Energy"].sum()


# Calcula a energia gerada no ano atual
def alculate_current_year_energy(data: pd.DataFrame) -> float:
    """
    Calcula a energia gerada no ano atual.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Year' e 'Energy'.

    Returns:
        float: Energia gerada no ano atual.
    """
    required_columns = {"Year", "Energy"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"O DataFrame deve conter as colunas {required_columns}.")

    current_year = pd.Timestamp.now().year
    filtered_data_kwh = data[data["Year"] == current_year]

    if filtered_data_kwh.empty:
        return 0.0  # Retorna 0 se não houver dados para o ano atual

    return filtered_data_kwh["Energy"].sum()


# Calcula a energia total
def calculate_total_energy(data: pd.DataFrame) -> float:
    logging.info("Calculando energia total...")
    validate_columns(data, {"Energy"})
    total_energy_kwh = data["Energy"].sum()
    logging.info(f"Energia total calculada: {total_energy_kwh}")
    return total_energy_kwh


# Valida se o DataFrame contém as colunas necessárias
def validate_columns(data: pd.DataFrame, required_columns: set):
    """
    Valida se o DataFrame contém as colunas necessárias.

    Args:
        data (pd.DataFrame): DataFrame a ser validado.
        required_columns (set): Conjunto de colunas obrigatórias.

    Raises:
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """
    if not required_columns.issubset(data.columns):
        raise ValueError(f"O DataFrame deve conter as colunas {required_columns}.")


def prepare_data_for_heatmap(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para exibição em um heatmap, garantindo que o campo 'Year'
    seja tratado como inteiro.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Microinversor', 'Year' e 'Energy'.

    Returns:
        pd.DataFrame: DataFrame com os dados agregados por Microinversor e Year.

    Raises:
        ValueError: Se as colunas necessárias não estiverem presentes no DataFrame.
    """
    validate_columns(data, {"Microinversor", "Year", "Energy"})

    # Garante que Year seja tratado como inteiro
    df = data.copy()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").dropna().astype(int)

    # Agregação
    df_agg = df.groupby(["Microinversor", "Year"])["Energy"].sum().unstack()

    return df_agg


def calculate_heatmap_height(
    data_agg: pd.DataFrame, min_height: int = 400, height_per_item: int = 25
) -> int:
    """
    Calcula a altura ideal para um heatmap com base no número de itens.

    Args:
        data_agg (pd.DataFrame): DataFrame agregado que será usado no heatmap.
        min_height (int, optional): Altura mínima do gráfico em pixels. Padrão: 400.
        height_per_item (int, optional): Pixels por item no eixo Y. Padrão: 25.

    Returns:
        int: Altura calculada para o heatmap.
    """
    return max(min_height, len(data_agg) * height_per_item)


def validate_energy_year_data(df: pd.DataFrame) -> bool:
    """
    Valida se o DataFrame contém as colunas necessárias para análise de energia por ano.

    Args:
        df (pd.DataFrame): DataFrame a ser validado.

    Returns:
        bool: True se o DataFrame contém as colunas necessárias, False caso contrário.
    """
    required_columns = {"Year", "Energy"}
    return required_columns.issubset(df.columns)


def aggregate_energy_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega os dados de energia por ano.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'Year' e 'Energy'.

    Returns:
        pd.DataFrame: DataFrame com a soma de energia agrupada por ano.

    Raises:
        ValueError: Se as colunas necessárias não estiverem presentes no DataFrame.
    """
    validate_columns(df, {"Year", "Energy"})
    return df.groupby("Year")["Energy"].sum().reset_index()


def calculate_color_mapping(
    data: pd.DataFrame, value_column: str, colorscale: list
) -> list:
    """
    Calcula o mapeamento de cores para valores numéricos em uma coluna do DataFrame.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados.
        value_column (str): Nome da coluna contendo os valores a serem mapeados.
        colorscale (list): Lista de cores para a escala.

    Returns:
        list: Lista de cores mapeadas para cada valor.
    """
    min_value = data[value_column].min()
    max_value = data[value_column].max()

    # Evita divisão por zero se min e max forem iguais
    range_value = max_value - min_value
    if range_value == 0:
        # Retorna a cor do meio da escala para todos os valores
        middle_color_index = len(colorscale) // 2
        return [colorscale[middle_color_index]] * len(data)

    # Normaliza os valores para a escala de cores
    normalized = (data[value_column] - min_value) / range_value

    # Mapeia para cores
    color_indices = (normalized * (len(colorscale) - 1)).astype(int)
    return [colorscale[i] for i in color_indices]


def clean_year_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converte a coluna 'Year' para inteiro extraindo apenas dígitos.

    Args:
        data: DataFrame contendo coluna 'Year'

    Returns:
        DataFrame com coluna 'Year' convertida para inteiro
    """
    df = data.copy()
    df["Year"] = df["Year"].astype(str).str.extract(r"(\d+)")[0].astype(int)
    return df


def filter_positive_energy(data: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra apenas registros com energia positiva.

    Args:
        data: DataFrame contendo coluna 'Energy'

    Raises:
        ValueError: Se DataFrame filtrado for vazio

    Returns:
        DataFrame filtrado
    """
    df = data[data["Energy"] > 0].copy()
    if df.empty:
        raise ValueError("Nenhum dado positivo encontrado")
    return df


def aggregate_energy_by_year_microinverter(data: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega energia por ano e microinversor.

    Args:
        data: DataFrame com colunas 'Year', 'Microinversor', 'Energy'

    Returns:
        DataFrame agregado e ordenado
    """
    return (
        data.groupby(["Year", "Microinversor"], as_index=False)["Energy"]
        .sum()
        .sort_values(["Year", "Microinversor"])
    )


def prepare_monthly_comparison_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara dados para comparação mensal de energia por ano.

    Args:
        df: DataFrame contendo colunas 'Year', 'Month' e 'Energy'

    Returns:
        DataFrame agregado por ano e mês

    Raises:
        ValueError: Se colunas necessárias não existirem
    """
    validate_columns(df, {"Year", "Month", "Energy"})

    return df.groupby(["Year", "Month"])["Energy"].sum().reset_index()


def get_month_names() -> dict:
    """
    Retorna mapeamento de números para nomes abreviados dos meses.

    Returns:
        Dicionário com {número: nome_abreviado}
    """
    return {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }


def calculate_yearly_averages(monthly_data: pd.DataFrame) -> dict:
    """
    Calcula médias anuais para adicionar como linhas de referência.

    Args:
        monthly_data: DataFrame com colunas 'Year' e 'Energy'

    Returns:
        Dicionário com {ano: média_energia}
    """
    return monthly_data.groupby("Year")["Energy"].mean().to_dict()


def detect_significant_trends(monthly_data: pd.DataFrame, threshold=0.2) -> dict:
    """
    Identifica tendências anuais significativas.

    Args:
        monthly_data: DataFrame com colunas 'Year' e 'Energy'
        threshold: Limite percentual para considerar significativo

    Returns:
        Dicionário com {ano: (valor_tendência, cor)}
    """
    trends = {}
    for year in monthly_data["Year"].unique():
        year_data = monthly_data[monthly_data["Year"] == year]
        trend_value = year_data["Energy"].iloc[-1] - year_data["Energy"].iloc[0]
        if abs(trend_value) > (year_data["Energy"].max() * threshold):
            trends[year] = (trend_value, "green" if trend_value > 0 else "red")
    return trends


def prepare_year_production_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """
    Prepara dados para gráfico de produção anual com cores gradientes.

    Args:
        df: DataFrame com colunas 'Year' e 'Energy'

    Returns:
        Tuple: (dados_agregados, lista_cores)

    Raises:
        ValueError: Se colunas necessárias não existirem
    """
    validate_columns(df, {"Year", "Energy"})

    df_agg = aggregate_energy_by_year(df)
    colors = calculate_color_mapping(df_agg, "Energy", Colors.GREEN_SEQUENTIAL)

    return df_agg, colors


def handle_plot_error(error: Exception, raw_data: pd.DataFrame = None) -> None:
    """
    Tratamento padronizado para erros em gráficos.

    Args:
        error: Exceção capturada
        raw_data: Dados originais para debug
    """
    st.error(f"Erro na geração do gráfico: {error!s}")
    if raw_data is not None and not raw_data.empty:
        st.warning("Visualização parcial dos dados recebidos:")
        st.dataframe(raw_data.head(3))

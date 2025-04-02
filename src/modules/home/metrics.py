import logging

import pandas as pd

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

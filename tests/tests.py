import pandas as pd

from src.modules.home.metrics import calculate_current_month_energy, calculate_total_energy


def test_calculate_total_energy():
    data = pd.DataFrame({"Energy": [100, 200, 300]})
    assert calculate_total_energy(data) == 600


def test_calculate_current_month_energy():
    data = pd.DataFrame({
        "Year": [2025, 2025, 2024],
        "Month": [4, 4, 3],
        "Energy": [100, 200, 300],
    })
    assert calculate_current_month_energy(data) == 300  # Supondo que o mês atual seja abril de 2025

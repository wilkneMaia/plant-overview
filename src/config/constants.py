from pathlib import Path
from typing import Final, Literal


# --- Locale ---
class LocaleSettings:
    CURRENCY: Final[str] = "pt_BR.UTF-8"  # Padrão BRL
    FALLBACK: Final[str] = "en_US.UTF-8"  # Fallback universal


# --- Caminhos ---
ICONS_DIR: Final[Path] = Path(__file__).parent / "../../assets/icons/"

# --- Tipos ---
IconName = Literal[
    "icon-co2", "icon-tree", "icon-default", "icon-income-month", "icon-income-today"
]


# --- Ícones ---
class Icons:
    POWER_MONTH = "icon-power-month"
    POWER_YEAR = "icon-power-year"
    POWER_TOTAL = "icon-power-total"
    STATS = "icon-stats"
    EFFICIENCY = "icon-efficiency"
    CO2: IconName = "icon-co2"
    TREE: IconName = "icon-tree"
    DEFAULT: IconName = "icon-default"
    INCOME_MONTH: IconName = "icon-income-month"
    INCOME_TODAY: IconName = "icon-income-today"
    DATABASE = "icon-database"
    DEVICES = "icon-devices"
    CALENDAR = "icon-calendar"
    PERFORMANCE = "icon-performance"


# --- Fatores ---
class EnergyFactors:
    CO2_KG_PER_KWH: Final[float] = 1.0  # Fonte: IPCC 2021 (exemplo)
    TREES_PER_KG_CO2: Final[float] = 1.0 / 18.32  # Fonte: EPA


class EconomicFactors:
    ELECTRICITY_PRICE_PER_KWH: Final[float] = 1.00  # R$/kWh (ajustar conforme região)


class SystemFactors:
    SYSTEM_CAPACITY_KW: Final[float] = 4.4  # kW
    MWH_CONVERSION_FACTOR: Final[float] = 1000.0  # kWh → MWh
    OPERATIONAL_HOURS_PER_DAY: Final[int] = 24  # horas/dia
    NOMINAL_EFFICIENCY: Final[float] = 0.85  # 85% (valor de referência)

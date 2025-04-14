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


# --- Font Sizes ---
class FontSettings:
    TITLE_CHART: Final[dict] = {"size": 16, "color": "white", "family": "Arial"}
    SUBTITLE_CHART: Final[dict] = {"size": 12, "color": "gray", "family": "Arial"}
    AXIS_TITLE: Final[dict] = {"size": 14, "color": "black", "family": "Arial"}
    TICK_LABEL: Final[dict] = {"size": 12, "color": "black", "family": "Arial"}
    LEGEND_TITLE: Final[dict] = {"size": 12, "color": "black", "family": "Arial"}
    HOVER_LABEL: Final[dict] = {"size": 12, "color": "black", "family": "Arial"}
    DEFAULT_COLOR: Final[str] = "black"  # Cor padrão para textos


# --- Font cards ---
class FontCards:
    TITLE: Final[dict] = {"size": "14px", "color": "#455564", "family": "Arial"}
    SUBTITLE: Final[dict] = {"size": "12px", "color": "#202E38", "family": "Arial"}
    PRIMARY_VALUE: Final[dict] = {"size": "22px", "color": "#00205B", "family": "Arial"}
    SECONDARY_VALUE: Final[dict] = {
        "size": "12px",
        "color": "#2FC774",
        "family": "Arial",
    }
    PRIMARY_UNIT: Final[dict] = {"size": "15px", "color": "#00205B", "family": "Arial"}
    SECONDARY_UNIT: Final[dict] = {
        "size": "12px",
        "color": "#2FC774",
        "family": "Arial",
    }


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
    RAW_COAL_SAVED = "icon-raw-coal-saved"


# --- Fatores ---
class EnergyFactors:
    CO2_KG_PER_KWH: Final[float] = 1.0  # Fonte: IPCC 2021 (exemplo)
    TREES_PER_KG_CO2: Final[float] = 1.0 / 18.32  # Fonte: EPA
    COAL_SAVED_PER_MWH = 0.405  # Exemplo: 0.405 toneladas de carvão economizado por MWh


class EconomicFactors:
    ELECTRICITY_PRICE_PER_KWH: Final[float] = 1.00  # R$/kWh (ajustar conforme região)


class SystemFactors:
    SYSTEM_CAPACITY_KW: Final[float] = 4.4  # kW
    MWH_CONVERSION_FACTOR: Final[float] = 1000.0  # kWh → MWh
    OPERATIONAL_HOURS_PER_DAY: Final[int] = 24  # horas/dia
    NOMINAL_EFFICIENCY: Final[float] = 0.85  # 85% (valor de referência)


# --- Colores ---
class Colors:
    PRIMARY: Final[str] = "#00aaff"
    SECONDARY: Final[str] = "#00ffff"
    PRIMARY_GREEN: Final[str] = "#00A878"
    GREEN_SEQUENTIAL: Final[list[str]] = [
        "#e0f5ee",
        "#c1e9db",
        "#a2dec9",
        "#83d3b6",
        "#64c8a4",
        "#45bd91",
        "#26b27f",
        "#07a76c",
        "#059059",
        "#047a47",
    ]
    GREEN_DISCRETE: Final[list[str]] = [
        "#00A878",  # Verde principal (mais vibrante)
        "#004B49",  # Verde profundo (contraste.maxcdn)
        "#7DCD85",  # Verde claro
        "#027357",  # Verde escuro
        "#C6EBBE",  # Verde pálido
        "#36877A",  # Verde-petróleo
        "#4ECDC4",  # Verde-água
        "#87D37C",  # Verde médio
        "#C7F9CC",  # Verde limão
        "#E3F5E8",  # Verde limão claro
    ]
    LINE_COLORS = [
        "#00A878",  # verde
        "#4ECDC4",  # verde-água
        "#F9C80E",  # amarelo vibrante
        "#F86624",  # laranja
        "#EA3546",  # vermelho rosado
        "#5D2E8C",  # roxo escuro
    ]

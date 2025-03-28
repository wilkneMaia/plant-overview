import base64
import locale
from functools import lru_cache
from pathlib import Path

from config.constants import ICONS_DIR, LocaleSettings


@lru_cache(maxsize=32)
def load_icon_as_base64(icon_name: str) -> str:
    """Carrega ícone como base64, com fallback implícito."""
    icon_path = ICONS_DIR / f"{icon_name}.svg"  # Adiciona extensão automaticamente

    if not icon_path.is_file():
        return ""  # Ou carregue Icons.DEFAULT aqui

    try:
        with open(icon_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Erro ao carregar ícone {icon_name}: {e}")
        return ""


def validate_icon(icon_name: str) -> str:
    """Verifica se o ícone existe antes de carregá-lo."""
    icon_path = Path(ICONS_DIR) / icon_name
    return icon_name if icon_path.is_file() else "icon-default.svg"


def setup_locale() -> bool:
    """Configura o locale com fallback seguro."""
    try:
        locale.setlocale(locale.LC_ALL, LocaleSettings.CURRENCY)
        return True
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, LocaleSettings.FALLBACK)
            return True
        except locale.Error:
            locale.setlocale(locale.LC_ALL, "")
            return False


def format_currency(value: float) -> str:
    """Formata valores monetários com locale seguro."""
    if not setup_locale():
        # Fallback manual se o locale falhar
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    try:
        return locale.currency(value, grouping=True, symbol=True)
    except:
        return f"R$ {value:,.2f}"

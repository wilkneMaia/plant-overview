def create_card(
    title: str,
    rows: list[dict],
    *,
    width: str = "100%",
    height: str = "auto",
    background: str = "linear-gradient(135deg, #0F2027 0%, #203A43 100%)",
    border_color: str = "#4CAF50",
    text_color: str = "#FFFFFF",
    secondary_text: str = "#B0B0B0",
    title_color: str = None,
    divider_color: str = "#333",
    icon_size: str = "20px",
    border_radius: str = "10px",
    box_shadow: str = "0 4px 8px 0 rgba(0,0,0,0.3)",
    padding: str = "15px",
    margin: str = "15px 0",
    border_left_width: str = "5px",
) -> str:
    """
    Gera um card HTML altamente customizável para uso no Streamlit.

    Parâmetros:
    -----------
    title : str
        Título do card (centralizado automaticamente)
    rows : list[dict]
        Lista de dicionários contendo os dados de cada linha. Cada dicionário deve conter:
        - icon: str (imagem em base64)
        - label: str
        - value: str
        - unit: str

    Parâmetros de Estilo (opcionais):
    --------------------------------
    width : str             Largura do card (ex: "300px", "50%"). Padrão: "100%"
    height : str            Altura do card. Padrão: "auto"
    background : str        Cor/background do card. Padrão: gradiente azul
    border_color : str      Cor da borda esquerda. Padrão: "#4CAF50" (verde)
    text_color : str        Cor do texto principal. Padrão: "#FFFFFF" (branco)
    secondary_text : str    Cor do texto secundário. Padrão: "#B0B0B0" (cinza claro)
    title_color : str      Cor do título (se None, usa border_color). Padrão: None
    divider_color : str    Cor dos divisores. Padrão: "#333"
    icon_size : str        Tamanho dos ícones. Padrão: "20px"
    border_radius : str    Arredondamento das bordas. Padrão: "10px"
    box_shadow : str       Sombra do card. Padrão: "0 4px 8px 0 rgba(0,0,0,0.3)"
    padding : str          Espaçamento interno. Padrão: "15px"
    margin : str           Margem externa. Padrão: "15px 0"
    border_left_width : str Largura da borda esquerda. Padrão: "5px"

    Retorna:
    --------
    str
        HTML do card pronto para uso com st.markdown(unsafe_allow_html=True)

    Exemplos de Uso:
    ----------------
    # Uso básico
    card = create_card("Título", rows)

    # Card com tema claro
    card = create_card(
        "Título",
        rows,
        background="#FFFFFF",
        text_color="#333333",
        border_color="#4CAF50"
    )

    # Card minimalista
    card = create_card(
        "Métricas",
        rows,
        background="#F8F9FA",
        border_color="#6C757D",
        box_shadow="none",
        border_left_width="2px"
    )
    """
    # Usa a cor da borda para o título se não for especificado
    title_color = title_color or border_color

    # Gera cada linha do card
    rows_html = []
    for i, row in enumerate(rows):
        # Adiciona divisor apenas entre linhas
        border_style = (
            f"border-bottom: 1px solid {divider_color}; padding-bottom: 10px;"
            if i < len(rows) - 1
            else ""
        )

        rows_html.append(
            f"""
        <div style="
            display: flex;
            align-items: center;
            margin: 10px 0;
            {border_style}
        ">
            <img src="data:image/svg+xml;base64,{row['icon']}"
                 alt="{row['label']}"
                 style="width: {icon_size};
                        height: {icon_size};
                        margin-right: 10px;">
            <span style="flex: 1; color: {text_color};">
                <strong>{row['label']}</strong>
            </span>
            <span style="font-weight: bold;
                         color: {border_color};
                         margin-right: 5px;">
                {row['value']}
            </span>
            <span style="color: {secondary_text};
                         font-size: 0.9em;">
                {row['unit']}
            </span>
        </div>
        """
        )

    # Template do card
    return f"""
    <div style="
        border-radius: {border_radius};
        box-shadow: {box_shadow};
        padding: {padding};
        margin: {margin};
        background: {background};
        border-left: {border_left_width} solid {border_color};
        font-family: Arial, sans-serif;
        color: {text_color};
        width: {width};
        height: {height};
        box-sizing: border-box;
    ">
        <div style="
            border-bottom: 1px solid {divider_color};
            padding-bottom: 10px;
            margin-bottom: 10px;
            text-align: center;
        ">
            <h3 style="margin: 0; color: {title_color};">
                {title}
            </h3>
        </div>
        <div>
            {"".join(rows_html)}
        </div>
    </div>
    """


def create_card_html(title: str, rows: list, footer: str = None) -> str:
    """
    Gera um card estilizado com design moderno e interativo.

    Args:
        title (str): Título do card com ícone opcional (ex: "📈 Performance").
        rows (list): Lista de dicionários com {icon, label, value, unit, trend, help}.
        footer (str, opcional): Texto de rodapé. Se None, o rodapé não será exibido.

    Returns:
        str: HTML completo do card com CSS inline.
    """
    # CSS modernizado com variáveis e animações
    css = """
    <style>
    :root {
        --primary-color: #00C853;
        --secondary-color: #5E35B1;
        --background-dark: #121212;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --card-border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .energy-card {
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: var(--background-dark);
        color: var(--text-primary);
        font-family: 'Segoe UI', system-ui;
        border: var(--card-border);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .energy-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 200, 83, 0.2);
    }

    .energy-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
    }

    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--primary-color);
    }

    .card-row {
        display: flex;
        align-items: center;
        margin: 12px 0;
        padding: 8px 0;
        transition: all 0.2s ease;
    }

    .card-row:hover {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
    }

    .card-icon {
        width: 24px;
        height: 24px;
        margin-right: 12px;
        flex-shrink: 0;
    }

    .card-label {
        flex: 1;
        color: var(--text-primary);
        font-size: 0.95rem;
    }

    .card-value {
        font-weight: 700;
        margin-right: 6px;
        color: var(--primary-color);
        font-size: 1.05rem;
    }

    .card-unit {
        color: var(--text-secondary);
        font-size: 0.85rem;
        min-width: 60px;
        text-align: right;
    }

    .card-trend {
        margin-left: 8px;
        font-size: 0.8rem;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .trend-up {
        background: rgba(0, 200, 83, 0.15);
        color: var(--primary-color);
    }

    .trend-down {
        background: rgba(255, 82, 82, 0.15);
        color: #FF5252;
    }

    .card-footer {
        margin-top: 5px;
        padding-top: 5px;
        font-size: 0.8rem;
        color: var(--text-secondary);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """

    # Gera o conteúdo das linhas com suporte a trend indicators
    rows_html = ""
    for row in rows:
        trend_html = ""
        if "trend" in row:
            trend_class = "trend-up" if row["trend"] >= 0 else "trend-down"
            trend_icon = "↑" if row["trend"] >= 0 else "↓"
            trend_html = f"""<span class="card-trend {trend_class}">
                              {trend_icon} {abs(row['trend'])}%
                            </span>"""

        help_html = (
            f"""<span class="card-help" title="{row.get('help', '')}">ⓘ</span>"""
            if "help" in row
            else ""
        )

        rows_html += f"""
        <div class="card-row">
            <img src="data:image/svg+xml;base64,{row['icon']}" class="card-icon">
            <span class="card-label">{row['label']}{help_html}</span>
            <span class="card-value">{row['value']}</span>
            <span class="card-unit">{row['unit']}</span>
            {trend_html}
        </div>
        """

    # Adiciona o rodapé apenas se fornecido
    footer_html = ""
    if footer:
        footer_html = f"""
        <div class="card-footer">
            {footer}
        </div>
        """

    # HTML completo do card
    card_content = f"""
    <div class="energy-card">
        <div class="card-title">{title}</div>
        {rows_html}
        {footer_html}
    </div>
    """

    return css + card_content

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
                         margin-right: 2px;">
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
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
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


# def create_card_html(title: str, rows: list, footer: str = None) -> str:
def create_card_html(title: str, rows: list, footer: str = None) -> str:
    """
    Cria o HTML para um card otimizado para tema escuro com boa legibilidade.

    Args:
        title: Título do card
        rows: Lista de dicionários com dados das linhas
        footer: Texto do rodapé (opcional)

    Returns:
        HTML como string com tooltips funcionais e contraste adequado
    """
    css = """
    <style>
    .energy-card {
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background: #1E1E1E;  /* Fundo mais escuro para melhor contraste */
        color: #F0F0F0;      /* Texto principal mais claro */
        font-family: 'Segoe UI', system-ui;
        border: 1px solid #333;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
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
        background: linear-gradient(to bottom, #4CAF50, #2E7D32);  /* Gradiente verde mais visível */
    }

    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #333;  /* Divisor mais visível */
        display: flex;
        align-items: center;
        gap: 8px;
        color: #4CAF50;  /* Verde para o título */
    }

    .card-row {
        display: flex;
        align-items: center;
        margin: 6px 0;  /* Maior espaçamento para melhor legibilidade */
        padding: 4px 0;
        transition: all 0.2s ease;
    }

    .card-row:hover {
        background: rgba(255, 255, 255, 0.05);  /* Hover sutil */
        border-radius: 6px;
    }

    .card-help {
        display: inline-block;
        margin-left: 6px;
        font-size: 12px;
        color: #64B5F6;  /* Azul mais claro para melhor visibilidade */
        cursor: help;
    }

    .card-icon {
        width: 24px;
        height: 24px;
        margin-right: 12px;
        flex-shrink: 0;
        filter: brightness(0) invert(0.8);  /* Ícones mais claros */
    }

    .card-label {
        flex: 1;
        color: #E0E0E0;  /* Texto mais claro */
        font-size: 0.95rem;
        font-weight: 500;  /* Mais espessura para melhor legibilidade */
    }

    .card-value {
        font-weight: 700;
        margin-right: 2px;
        color: #FFFFFF;  /* Branco puro para valores */
        font-size: 1.05rem;
    }

    .card-unit {
        color: #B0B0B0;  /* Cinza para unidades */
        font-size: 0.85rem;
        min-width: 60px;
        text-align: right;
    }

    .card-trend {
        margin-left: 8px;
        font-size: 0.8rem;
        padding: 2px 6px;  /* Mais padding para melhor visibilidade */
        border-radius: 4px;
        font-weight: 600;
    }

    .trend-up {
        background: rgba(76, 175, 80, 0.2);  /* Verde mais transparente */
        color: #4CAF50;
    }

    .trend-down {
        background: rgba(255, 82, 82, 0.2);  /* Vermelho mais transparente */
        color: #FF5252;
    }

    .card-footer {
        margin-top: 5px;
        padding-top: 5px;
        font-size: 0.8rem;
        color: #9E9E9E;  /* Cinza para o rodapé */
        border-top: 1px solid #333;
        background-color: rgba(255, 255, 255, 0.03);
        padding-bottom: 10px;
    }

    @media only screen and (max-width: 768px) {
        .energy-card {
            padding: 15px;
            margin: 10px 0;
        }
        .card-title {
            font-size: 1.1rem;
        }
        .card-row {
            margin: 4px 0;
        }
    }
    </style>
    """

    # Gera o conteúdo das linhas
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
            f'<span class="card-help" title="{row["help"]}">ⓘ</span>'
            if row.get("help")
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

    footer_html = f'<div class="card-footer">{footer}</div>' if footer else ""

    return f"""
    {css}
    <div class="energy-card">
        <div class="card-title">{title}</div>
        {rows_html}
        {footer_html}
    </div>
    """

import streamlit.components.v1 as components

from utils.helpers import load_icon_as_base64


def card_animated(
    title: str,
    title_style: dict,
    subtitle: str,
    subtitle_style: dict,
    primary_value: float,
    secondary_value: float,
    primary_unit: str = "unit",
    secondary_unit: str = "unit",
    icon: str = None,
    icon_size: str = "40px",
):
    # Load the icon as base64 if provided
    icon_base64 = load_icon_as_base64(icon) if icon else None
    # HTML for the card with optional icon
    icon_html = (
        f'<img src="data:image/svg+xml;base64,{icon_base64}" alt="Icon" class="icon">'
        if icon_base64
        else '<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#6c757d"><circle cx="12" cy="12" r="10"/></svg>'
    )

    html_code = f"""
    <div class="card">
        {icon_html}
        <div class="card-content">
            <div>
                <span class="title">{title}</span>
                <div class="primary-value">
                    <span id="primary-value" data-target="{primary_value}">0</span>
                    <span class="primary-unit">{primary_unit}</span>
                </div>
            </div>
            <div class="subtitle-container">
                <span class="subtitle">{subtitle}</span>
                <div class="secondary-value">
                    <span id="secondary-value" data-target="{secondary_value}">0</span>
                    <span class="secondary-unit">{secondary_unit}</span>
                </div>
            </div>
        </div>
    </div>
    <script>
        function animateValue(id, target) {{
            const element = document.getElementById(id);
            const duration = 2000; // Duração da animação em milissegundos
            const increment = target / (duration / 16); // Incremento por frame (~60fps)
            let current = 0;

            function updateValue() {{
                current += increment;
                if (current >= target) {{
                    element.textContent = target.toFixed(2); // Formata o valor final
                }} else {{
                    element.textContent = current.toFixed(2); // Atualiza o valor animado
                    requestAnimationFrame(updateValue);
                }}
            }}
            updateValue();
        }}

        document.addEventListener("DOMContentLoaded", function() {{
            animateValue("primary-value", parseFloat(document.getElementById("primary-value").getAttribute("data-target")));
            animateValue("secondary-value", parseFloat(document.getElementById("secondary-value").getAttribute("data-target")));
        }});
    </script>
    <style>
        .card {{
            background-color: #f4f5f7;
            padding: 15px;
            border-radius: 8px;
            width: 100%;
            max-width: 250px;
            font-family: Arial, sans-serif;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        }}
        .title {{
            font-size: {title_style['size']};
            font-family: {title_style['family']};
            font-weight: bold;
            color: {title_style['color']};
        }}
        .primary-value {{
            font-size: 24px;
            font-weight: bold;
            color: #28a745;
        }}
        .subtitle {{
            font-size: {subtitle_style['size']};
            font-family: {subtitle_style['family']};
            color: {subtitle_style['color']};
            margin-right: 3px; /* Espaço entre o subtitle e o valor */
        }}
        .secondary-value {{
            font-size: 20px;
            font-weight: bold;
            color: #28a745;
        }}

        .icon {{
            width: {icon_size}; /* Custom icon size */
            height: {icon_size};
            margin-right: 10px; /* Space between the icon and the text */
        }}
        .card-content {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
    </style>
    """
    components.html(html_code, height=300)

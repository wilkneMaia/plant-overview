import pandas as pd
import plotly.express as px
import streamlit as st


class AreaChart:
    """Classe para criação de gráficos de área com suporte a temas dark/light"""

    # Configurações de tema padrão
    THEME_SETTINGS = {
        "dark": {
            "title_color": "white",
            "subtitle_color": "#AAAAAA",
            "axis_color": "white",
            "bg_color": "rgba(0,0,0,0)",
            "plot_bg_color": "rgba(0,0,0,0)",
            "grid_color": "rgba(80,80,80,0.3)",
            "legend_bg": "rgba(40,40,40,0.7)",
        },
        "light": {
            "title_color": "#333333",
            "subtitle_color": "#666666",
            "axis_color": "#333333",
            "bg_color": "white",
            "plot_bg_color": "white",
            "grid_color": "rgba(200,200,200,0.3)",
            "legend_bg": "rgba(240,240,240,0.7)",
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: str,
        colors: list[str],
        period_mapping: dict,
        theme: str = "dark",
        title: str = "",
        subtitle: str = "",
        height: int = 450,
        unit: str = "kWh",
        xaxis_title: str = "Mês",
        yaxis_title: str = "Energia Gerada (kWh)",
        legend_title: str = "Ano",
    ):
        """
        Inicializa o gráfico com configurações de tema

        Args:
            theme: 'dark' ou 'light' - define o esquema de cores
            ... outros parâmetros permanecem iguais ...
        """
        self.data = data
        self.x_col = x_col
        self.y_col = y_col
        self.color_col = color_col
        self.colors = colors
        self.period_mapping = period_mapping
        self.theme = theme.lower()
        self.title = title
        self.subtitle = subtitle
        self.height = height
        self.unit = unit
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.legend_title = legend_title

        # Validação do tema
        if self.theme not in self.THEME_SETTINGS:
            raise ValueError(f"Tema '{theme}' inválido. Use 'dark' ou 'light'")

        # Cria a figura imediatamente
        self._create_figure()

    def _create_figure(self):
        """Cria a figura do gráfico com as configurações iniciais"""
        self.THEME_SETTINGS[self.theme]

        self.fig = px.area(
            self.data,
            x=self.x_col,
            y=self.y_col,
            color=self.color_col,
            color_discrete_sequence=self.colors,
            height=self.height,
            labels={self.y_col: f"{self.y_col} ({self.unit})"},
            template="plotly_dark" if self.theme == "dark" else None,
        )

        # Aplica configurações iniciais de tema
        self._apply_theme_settings()

    def _apply_theme_settings(self):
        """Aplica as configurações visuais do tema selecionado"""
        theme = self.THEME_SETTINGS[self.theme]

        # Configuração padrão do título
        self.set_titles(
            title_font={"size": 22, "color": theme["title_color"], "family": "Arial"},
            subtitle_font={
                "size": 16,
                "color": theme["subtitle_color"],
                "family": "Arial",
            },
        )

        # Configuração do estilo base
        self.apply_style(
            bg_color=theme["bg_color"],
            plot_bg_color=theme["plot_bg_color"],
            axis_font={"size": 14, "color": theme["axis_color"]},
            grid_color=theme["grid_color"],
            legend_bg=theme["legend_bg"],
        )

    def set_titles(
        self,
        title: str = None,
        subtitle: str = None,
        title_font: dict = None,
        subtitle_font: dict = None,
    ) -> "AreaChart":
        """Configura título e subtítulo"""
        if title is not None:
            self.title = title
        if subtitle is not None:
            self.subtitle = subtitle

        self.fig.update_layout(
            title={
                "text": (
                    f"<b>{self.title}</b><br><span style='font-size:{subtitle_font['size'] if subtitle_font else 16}px;color:{subtitle_font['color'] if subtitle_font else self.THEME_SETTINGS[self.theme]['subtitle_color']}'>{self.subtitle}</span>"
                ),
                "font": (
                    title_font
                    or {
                        "size": 22,
                        "color": self.THEME_SETTINGS[self.theme]["title_color"],
                    }
                ),
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
            }
        )
        return self

    def apply_style(
        self,
        bg_color: str = None,
        plot_bg_color: str = None,
        axis_font: dict = None,
        grid_color: str = None,
        legend_bg: str = None,
        show_legend: bool = True,
        opacity: float = 0.7,
        line_width: float = 1.5,
    ) -> "AreaChart":
        """Aplica estilização ao gráfico"""
        theme = self.THEME_SETTINGS[self.theme]

        self.fig.update_layout(
            hoverlabel=dict(
                bgcolor="rgba(0, 0, 0, 0.8)",  # Fundo escuro semi-transparente
                bordercolor="rgba(255, 255, 255, 0.5)",  # Borda branca semi-transparente
                font_size=12,  # Tamanho da fonte
                font_color="white",  # Texto em branco para melhor contraste
            ),
            hovermode="x unified",
            legend=(
                {
                    "title": {"text": self.legend_title, "font": {"size": 12}},
                    "orientation": "h",
                    "y": -0.2,
                    "bgcolor": legend_bg or theme["legend_bg"],
                }
                if show_legend
                else None
            ),
            xaxis={
                "title": {
                    "text": self.xaxis_title,
                    "font": axis_font or {"size": 14, "color": theme["axis_color"]},
                },
                "tickvals": list(self.period_mapping.keys()),
                "ticktext": list(self.period_mapping.values()),
                "tickangle": 0,
                "gridcolor": grid_color or theme["grid_color"],
            },
            yaxis={
                "title": {
                    "text": f"{self.yaxis_title} ({self.unit})",
                    "font": axis_font or {"size": 14, "color": theme["axis_color"]},
                },
                "gridcolor": grid_color or theme["grid_color"],
            },
            margin=dict(l=30, r=40, t=70, b=60),
        )

        if bg_color:
            self.fig.update_layout(paper_bgcolor=bg_color)
        if plot_bg_color:
            self.fig.update_layout(plot_bgcolor=plot_bg_color)

        self.fig.update_traces(
            # marker=dict(
            #     size=6, line=dict(width=1, color="white")  # Borda branca nos marcadores
            # ),
            opacity=opacity,
            line=dict(width=line_width),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"  # Apenas o nome do grupo
                "Produção: %{y:,.0f} {self.unit}<br>"  # Formatação simplificada
                "<extra></extra>"
            ),
            mode="lines+markers",
        )
        return self

    def set_theme(self, theme: str) -> "AreaChart":
        """Altera o tema do gráfico (dark/light)"""
        if theme.lower() not in self.THEME_SETTINGS:
            raise ValueError(f"Tema '{theme}' inválido. Use 'dark' ou 'light'")

        self.theme = theme.lower()
        self._create_figure()  # Recria o gráfico com o novo tema
        return self

    def show(self, **kwargs) -> None:
        """Exibe o gráfico no Streamlit"""
        st.plotly_chart(self.fig, use_container_width=True, **kwargs)

    def add_peak_annotation(
        self,
        text: str = "Pico de Produção",
        showarrow: bool = True,
        arrowhead: int = 2,
        font_size: int = 12,
        x_offset: float = 0,
        y_offset: float = 0,
        **kwargs,
    ) -> "AreaChart":
        """
        Adiciona automaticamente uma anotação no ponto de pico de produção

        Args:
            text: Texto da anotação (default: "Pico de Produção")
            showarrow: Mostrar seta (default: True)
            arrowhead: Tipo de ponta de seta (0-7, default: 2)
            font_size: Tamanho da fonte (default: 12)
            x_offset: Ajuste horizontal da posição
            y_offset: Ajuste vertical da posição
            **kwargs: Outros parâmetros para a anotação
        """
        # Encontra o índice do valor máximo
        max_idx = self.data[self.y_col].idxmax()
        peak_data = self.data.loc[max_idx]

        # Obtém as configurações de tema
        theme = self.THEME_SETTINGS[self.theme]

        # Adiciona a anotação
        self.fig.add_annotation(
            text=text,
            x=peak_data[self.x_col] + x_offset,
            y=peak_data[self.y_col] + y_offset,
            showarrow=showarrow,
            arrowhead=arrowhead,
            font=dict(size=font_size, color=theme["axis_color"]),
            **kwargs,
        )
        return self

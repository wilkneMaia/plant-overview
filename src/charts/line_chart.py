import pandas as pd
import plotly.express as px
import streamlit as st
from plotly import graph_objects as go


class LineChart:
    """Classe para criação de gráficos de linha com suporte a temas dark/light"""

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
            "hover_bg": "rgba(30,30,30,0.9)",
            "hover_font_color": "white",
        },
        "light": {
            "title_color": "#333333",
            "subtitle_color": "#666666",
            "axis_color": "#333333",
            "bg_color": "white",
            "plot_bg_color": "white",
            "grid_color": "rgba(200,200,200,0.3)",
            "legend_bg": "rgba(240,240,240,0.7)",
            "hover_bg": "rgba(255,255,255,0.9)",
            "hover_font_color": "#333333",
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: str,
        colors: list[str],
        period_mapping: dict[int, str],
        theme: str = "dark",
        title: str = "",
        subtitle: str = "",
        xlabel: str = "Mês",
        ylabel: str = "Energia (kWh)",
        legend_title: str = "Ano",
        height: int = 550,
        unit: str = "kWh",
    ):
        """
        Inicializa o gráfico de linhas comparativo

        Args:
            data: DataFrame com os dados
            x_col: Coluna para eixo X
            y_col: Coluna para eixo Y
            color_col: Coluna para diferenciação
            colors: Lista de cores
            period_mapping: Dicionário de mapeamento de períodos
            theme: 'dark' ou 'light'
            title: Título principal
            subtitle: Subtítulo
            xlabel: Label eixo X
            ylabel: Label eixo Y
            legend_title: Título da legenda
            height: Altura do gráfico
            unit: Unidade de medida
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
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend_title = legend_title
        self.height = height
        self.unit = unit

        if self.theme not in self.THEME_SETTINGS:
            raise ValueError(f"Tema '{theme}' inválido. Use 'dark' ou 'light'")

        self.fig = self._create_figure()
        self._apply_theme_settings()

    def _create_figure(self) -> go.Figure:
        """Cria a figura base do gráfico de linhas"""
        return px.line(
            self.data,
            x=self.x_col,
            y=self.y_col,
            color=self.color_col,
            markers=True,
            color_discrete_sequence=self.colors,
            labels={self.y_col: f"{self.ylabel} ({self.unit})"},
            height=self.height,
        )

    def _apply_theme_settings(self):
        """Aplica as configurações visuais do tema selecionado"""
        theme = self.THEME_SETTINGS[self.theme]

        self.set_titles(
            title_font={"size": 22, "color": theme["title_color"], "family": "Arial"},
            subtitle_font={
                "size": 16,
                "color": theme["subtitle_color"],
                "family": "Arial",
            },
        )

        self.apply_style(
            bg_color=theme["bg_color"],
            plot_bg_color=theme["plot_bg_color"],
            axis_font={"size": 14, "color": theme["axis_color"]},
            grid_color=theme["grid_color"],
            legend_bg=theme["legend_bg"],
            hover_bg=theme["hover_bg"],
            hover_font_color=theme["hover_font_color"],
        )

    def set_titles(
        self,
        title: str = None,
        subtitle: str = None,
        title_font: dict = None,
        subtitle_font: dict = None,
    ) -> "LineChart":
        """Configura título e subtítulo do gráfico"""
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
        hover_bg: str = None,
        hover_font_color: str = None,
        show_legend: bool = True,
        line_width: float = 2.5,
        marker_size: int = 8,
        opacity: float = 0.8,
    ) -> "LineChart":
        """Aplica estilização ao gráfico"""
        theme = self.THEME_SETTINGS[self.theme]

        # Configurações do hover
        hoverlabel = {
            "bgcolor": hover_bg or theme["hover_bg"],
            "bordercolor": (
                f"rgba({'255,255,255' if self.theme == 'dark' else '0,0,0'},0.2)"
            ),
            "font_size": 12,
            "font_color": hover_font_color or theme["hover_font_color"],
        }

        self.fig.update_layout(
            plot_bgcolor=plot_bg_color or theme["plot_bg_color"],
            paper_bgcolor=bg_color or theme["bg_color"],
            hoverlabel=hoverlabel,
            hovermode="x unified",
            margin=dict(l=80, r=50, t=100, b=80),
            legend=(
                {
                    "title": {"text": self.legend_title, "font": {"size": 12}},
                    "orientation": "h",
                    "y": -0.25,
                    "bgcolor": legend_bg or theme["legend_bg"],
                }
                if show_legend
                else None
            ),
            xaxis={
                "title": {
                    "text": self.xlabel,
                    "font": axis_font or {"size": 14, "color": theme["axis_color"]},
                },
                "tickvals": list(self.period_mapping.keys()),
                "ticktext": [m.upper()[:3] for m in self.period_mapping.values()],
                "tickangle": 0,
                "gridcolor": grid_color or theme["grid_color"],
            },
            yaxis={
                "title": {
                    "text": f"{self.ylabel} ({self.unit})",
                    "font": axis_font or {"size": 14, "color": theme["axis_color"]},
                },
                "gridcolor": grid_color or theme["grid_color"],
            },
        )

        self.fig.update_traces(
            line=dict(width=line_width),
            marker=dict(size=marker_size, line=dict(width=1, color="white")),
            opacity=opacity,
            mode="lines+markers",
            hovertemplate=f"<b>%{{fullData.name}}</b><br>{self.xlabel}: %{{x}}<br>{self.ylabel}: <b>%{{y:,.0f}} {self.unit}</b><extra></extra>",
        )
        return self

    def add_peak_annotation(
        self, text: str = "Pico de Produção", x_offset: float = 0.5, y_offset: float = 0
    ) -> "LineChart":
        """Adiciona anotação no ponto de máximo"""
        max_idx = self.data[self.y_col].idxmax()
        peak_data = self.data.loc[max_idx]

        theme = self.THEME_SETTINGS[self.theme]

        self.fig.add_annotation(
            text=text,
            x=peak_data[self.x_col],
            y=peak_data[self.y_col],
            xshift=x_offset,
            yshift=y_offset,
            showarrow=True,
            arrowhead=2,
            font=dict(size=12, color=theme["axis_color"]),
        )
        return self

    def show(self, **kwargs) -> None:
        """Exibe o gráfico no Streamlit"""
        st.plotly_chart(self.fig, use_container_width=True, **kwargs)

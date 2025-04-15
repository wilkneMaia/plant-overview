import pandas as pd
import plotly.express as px
import streamlit as st
from plotly import graph_objects as go


class BarChart:
    """Classe para criação de gráficos de barras temáticos e reutilizáveis"""

    THEME_SETTINGS = {
        "dark": {
            "title_color": "white",
            "subtitle_color": "#AAAAAA",
            "axis_color": "white",
            "bg_color": "rgba(0,0,0,0)",
            "plot_bg_color": "rgba(0,0,0,0)",
            "grid_color": "rgba(80,80,80,0.3)",
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
            "hover_bg": "rgba(255,255,255,0.9)",
            "hover_font_color": "#333333",
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_scale: list[str],
        theme: str = "dark",
        unit: str = "kWh",
        height: int = 450,
        margin: dict | None = None,
        xaxis_title: str | None = None,
        yaxis_title: str | None = None,
    ):
        self.data = data
        self.x_col = x_col
        self.y_col = y_col
        self.color_scale = color_scale
        self.theme = theme.lower()
        self.unit = unit
        self.height = height
        self.margin = margin or dict(l=60, r=30, t=70, b=60)  # Adjusted top margin
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.fig = self._create_base_figure()
        self._apply_theme_settings()

    def _create_base_figure(self) -> go.Figure:
        """Cria a figura inicial com Plotly Express"""
        return px.bar(
            self.data,
            x=self.x_col,
            y=self.y_col,
            color=self.y_col,
            color_continuous_scale=self.color_scale,
            labels={self.y_col: self.yaxis_title} if self.yaxis_title else None,
            height=self.height,
        )

    def _apply_theme_settings(self):
        """Aplica as configurações visuais do tema selecionado"""
        theme = self.THEME_SETTINGS[self.theme]

        self.fig.update_traces(
            marker=dict(
                line=dict(width=1.5, color="rgba(255,255,255,0.7)"), opacity=0.85
            ),
            hovertemplate=(
                f"{(self.xaxis_title + ': ') if self.xaxis_title else ''}%{{x}}<br>"
                f"{(self.yaxis_title + ': ') if self.yaxis_title else ''}%{{y:,.0f}} {self.unit}<extra></extra>"
            ),
            texttemplate="%{y:,.0f}",
            textposition="outside",
            textfont=dict(color="white", size=11),
        )

        self.fig.update_layout(
            plot_bgcolor=theme["plot_bg_color"],
            paper_bgcolor=theme["bg_color"],
            margin=self.margin,
            xaxis=dict(
                title=self.xaxis_title if self.xaxis_title else None,
                tickmode="array",
                tickvals=self.data[self.x_col],
                gridcolor=theme["grid_color"],
                title_font=dict(size=14) if self.xaxis_title else None,
                tickangle=0,
                showgrid=False,
                zeroline=True,
                zerolinecolor=theme["grid_color"],
                zerolinewidth=2,
                showline=True,
                linecolor=theme["axis_color"],
            ),
            yaxis=dict(
                title=self.yaxis_title if self.yaxis_title else None,
                gridcolor=theme["grid_color"],
                zerolinecolor=theme["grid_color"],
                title_font=dict(size=14) if self.yaxis_title else None,
                showgrid=False,
                zeroline=True,
                zerolinewidth=2,
                showline=True,
                linecolor=theme["axis_color"],
            ),
            hoverlabel=dict(
                bgcolor=theme["hover_bg"],
                font_size=12,
                font_color=theme["hover_font_color"],
            ),
            coloraxis_showscale=False,
            showlegend=False,
        )

    def set_titles(
        self,
        title: str,
        subtitle: str,
        title_font: dict | None = None,
        subtitle_font: dict | None = None,
    ) -> "BarChart":
        """
        Configura títulos com suporte a formatação HTML

        Args:
            title: Título principal com tags HTML
            subtitle: Subtítulo com tags HTML
            title_font: Configurações de fonte para título
            subtitle_font: Configurações de fonte para subtítulo
        """
        theme = self.THEME_SETTINGS[self.theme]

        self.fig.update_layout(
            title={
                "text": (
                    f"<b>{title}</b><br><span style='font-size:{subtitle_font['size'] if subtitle_font else 16}px;color:{subtitle_font['color'] if subtitle_font else theme['subtitle_color']}'>{subtitle}</span>"
                ),
                "font": title_font or {"size": 22, "color": theme["title_color"]},
                "y": 0.95,  # Ajuste a posição para reduzir o espaço superior
                "x": 0.04,  # Alinhando o título à esquerda
                "xanchor": "left",  # Alinha à esquerda
            },
            margin=dict(t=80),
        )
        return self

    def apply_customizations(
        self,
        line_width: float = 1.5,
        opacity: float = 0.85,
        text_position: str = "outside",
        text_color: str = "white",
    ) -> "BarChart":
        """Permite personalizações adicionais nas barras"""
        self.fig.update_traces(
            marker_line_width=line_width,
            opacity=opacity,
            textposition=text_position,
            textfont_color=text_color,
        )
        return self

    def show(self) -> None:
        """Exibe o gráfico no Streamlit"""
        # Adicionando o estilo CSS para remover as bordas e padding do gráfico
        st.markdown(
            """
            <style>
                .stPlotlyChart {
                    border: none !important;
                    padding: 0 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(self.fig, use_container_width=True)

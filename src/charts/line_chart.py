import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.colors import qualitative


class LineChart:
    """Classe para criação de gráficos de linha com suporte a temas dark/light"""

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
            "highlight_color": "#00FF88",
            "dimmed_color": "#555555",
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
            "highlight_color": "#008000",
            "dimmed_color": "#CCCCCC",
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: str,
        colors: list[str] = None,
        period_mapping: dict[int, str] = None,
        theme: str = "dark",
        title: str = "",
        subtitle: str = "",
        xlabel: str = "Mês",
        ylabel: str = "Energia",
        legend_title: str = "Ano",
        height: int = 450,
        unit: str = "kWh",
    ):
        self.data = data
        self.x_col = x_col
        self.y_col = y_col
        self.color_col = color_col
        self.colors = colors or qualitative.Plotly
        self.period_mapping = period_mapping or {}
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

        self._validate_columns()
        self.fig = self._create_figure()
        self._apply_theme_settings()
        self._add_inline_labels()
        self._hide_legend()

    def _validate_columns(self):
        required_cols = [self.x_col, self.y_col, self.color_col]
        for col in required_cols:
            if col not in self.data.columns:
                raise ValueError(
                    f"Coluna obrigatória '{col}' não encontrada no DataFrame."
                )

    def _create_figure(self) -> go.Figure:
        fig = px.line(
            self.data,
            x=self.x_col,
            y=self.y_col,
            color=self.color_col,
            markers=True,
            color_discrete_sequence=self.colors,
            labels={self.y_col: f"{self.ylabel} ({self.unit})"},
            height=self.height,
            template="plotly_dark" if self.theme == "dark" else "plotly_white",
        )
        return fig

    def _apply_theme_settings(self):
        """
        Aplica as configurações de tema (cores, fontes, etc.) ao gráfico com base no tema especificado.

        O tema pode ser 'dark' ou 'light'. Dependendo do tema escolhido, as cores do título, do subtítulo,
        dos eixos e do fundo do gráfico serão ajustadas.
        """
        theme = self.THEME_SETTINGS[self.theme]
        self.set_titles(
            title_font={"size": 22, "color": theme["title_color"], "family": "Arial"},
            subtitle_font={
                "size": 16,
                "color": theme["subtitle_color"],
                "family": "Arial",
            },
        )

    def _add_inline_labels(self):
        for trace in self.fig.data:
            if trace.mode and "lines" in trace.mode:
                x_end = trace.x[-1]
                y_end = trace.y[-1]
                self.fig.add_annotation(
                    x=x_end,
                    y=y_end,
                    text=trace.name,
                    showarrow=False,
                    font=dict(size=12, color=trace.line.color),
                    xanchor="left",
                    xshift=10,
                    yshift=10,
                )

    def _hide_legend(self):
        self.fig.update_layout(showlegend=False)

    def set_titles(
        self,
        title: str = None,
        subtitle: str = None,
        title_font: dict = None,
        subtitle_font: dict = None,
    ) -> "LineChart":
        if title:
            self.title = title
        if subtitle:
            self.subtitle = subtitle

        default_subtitle_font = {
            "size": 12,
            "color": self.THEME_SETTINGS[self.theme]["subtitle_color"],
            "family": "Arial",
        }
        subtitle_font = subtitle_font or default_subtitle_font

        self.fig.update_layout(
            title={
                "text": (
                    f"<b>{self.title}</b><br><span style='font-size:{subtitle_font['size']}px;color:{subtitle_font['color']}'>{self.subtitle}</span>"
                ),
                "font": (
                    title_font
                    or {
                        "size": 22,
                        "color": self.THEME_SETTINGS[self.theme]["title_color"],
                        "family": "Arial",
                    }
                ),
                "y": 0.95,  # Ajuste do espaço entre o subtítulo e o gráfico
                "x": 0.03,
                "xanchor": "left",
            },
            margin=dict(t=70),  # Aumenta a margem superior para criar mais espaço
        )
        return self

    def apply_style(self, **kwargs) -> "LineChart":
        theme = self.THEME_SETTINGS[self.theme]

        layout_updates = {
            "plot_bgcolor": kwargs.get(
                "plot_bg_color", self.THEME_SETTINGS[self.theme]["plot_bg_color"]
            ),
            "paper_bgcolor": kwargs.get(
                "bg_color", self.THEME_SETTINGS[self.theme]["bg_color"]
            ),
            "hovermode": kwargs.get("hovermode", "x unified"),
            "hoverlabel": {
                "bgcolor": kwargs.get(
                    "hover_bg", self.THEME_SETTINGS[self.theme]["hover_bg"]
                ),
                "font_color": kwargs.get(
                    "hover_font_color",
                    self.THEME_SETTINGS[self.theme]["hover_font_color"],
                ),
            },
            "xaxis": {
                "title": kwargs.get("xlabel", self.xlabel),
                "showgrid": False,  # Remove as linhas de grade horizontais
                "zeroline": True,  # Exibe a linha principal do eixo X
                "zerolinecolor": "white",  # Cor da linha principal do eixo X
                "zerolinewidth": 2,  # Espessura da linha
                "showline": True,  # Exibe a linha principal do eixo X
                "linecolor": theme["axis_color"],  # Cor da linha principal do eixo X
                "tickvals": list(
                    self.period_mapping.keys()
                ),  # Define os valores do eixo X
                "ticktext": [
                    m.upper()[:3] for m in self.period_mapping.values()
                ],  # Exibe os valores com a abreviação
            },
            "yaxis": {
                "title": kwargs.get("ylabel", f"{self.ylabel} ({self.unit})"),
                "showgrid": False,  # Remove as linhas de grade verticais
                "zeroline": True,  # Exibe a linha principal do eixo Y
                "zerolinecolor": "white",  # Cor da linha principal do eixo Y
                "zerolinewidth": 2,  # Espessura da linha
                "showline": True,  # Exibe a linha principal do eixo Y
                "linecolor": theme["axis_color"],  # Cor da linha principal do eixo Y
            },
            "margin": {
                "l": 0,  # Remove a margem esquerda
                "r": 0,  # Remove a margem direita
                "t": 90,  # Mantém a margem superior para o título
                "b": 60,  # Ajusta a margem inferior
            },
            "xaxis_showgrid": False,
            "yaxis_showgrid": False,
            "showlegend": False,  # Opcional: Remover a legenda se não for necessária
        }

        self.fig.update_layout(layout_updates)
        return self

    def add_peaks_per_group(self, label_col="Year") -> "LineChart":
        for name, group in self.data.groupby(label_col):
            peak = group.loc[group[self.y_col].idxmax()]
            self.fig.add_trace(
                go.Scatter(
                    x=[peak[self.x_col]],
                    y=[peak[self.y_col]],
                    mode="markers+text",
                    name=f"Pico {name}",
                    marker=dict(
                        color=self.THEME_SETTINGS[self.theme]["highlight_color"],
                        size=12,
                    ),
                    # text=[f"Pico {name}"],
                    text=["P"],
                    textposition="top center",
                )
            )
        return self

    def show(self, **kwargs) -> None:
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

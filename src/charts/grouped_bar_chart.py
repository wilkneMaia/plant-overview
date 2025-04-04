import pandas as pd
import plotly.express as px
import streamlit as st


class GroupedBarChart:
    """Classe para criar gráficos de barras agrupadas com temas e personalizações."""

    THEME_SETTINGS = {
        "dark": {
            "title_color": "white",
            "axis_color": "white",
            "bg_color": "rgba(0,0,0,0)",
            "grid_color": "rgba(80,80,80,0.3)",
            "legend_bg": "rgba(40,40,40,0.7)",
            "hover_bg": "rgba(30,30,30,0.9)",
            "hover_font_color": "white",
            "bar_line_color": "rgba(80,80,80,0.8)",  # Cor da linha das barras
        },
        "light": {
            "title_color": "#333333",
            "axis_color": "#333333",
            "bg_color": "white",
            "grid_color": "rgba(200,200,200,0.3)",
            "legend_bg": "rgba(240,240,240,0.7)",
            "hover_bg": "rgba(255,255,255,0.9)",
            "hover_font_color": "#333333",
            "bar_line_color": "rgba(200,200,200,0.8)",  # Cor da linha das barras
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: str,
        colors: list[str],
        theme: str = "light",
        title: str = "",
        xlabel: str = "Categoria",
        ylabel: str = "Valor",
        height: int = 500,
        text_auto: bool = True,
        barmode: str = "group",
        legend_title: str = "Legenda",
    ):
        """
        Inicializa o gráfico de barras agrupadas.

        Args:
            data: DataFrame com os dados.
            x_col: Coluna para eixo X.
            y_col: Coluna para diferenciação.
            colors: Lista de cores para as barras.
            theme: 'dark' ou 'light' - define o esquema de cores.
            title: Título do gráfico.
            xlabel: Rótulo do eixo X.
            ylabel: Rótulo do eixo Y.
            height: Altura do gráfico.
            text_auto: Se True, exibe os valores nas barras automaticamente.
            barmode: Modo de exibição das barras ('group', 'stack', etc.).
            legend_title: Título da legenda.
        """
        self.data = data
        self.x_col = x_col
        self.y_col = y_col
        self.color_col = color_col
        self.colors = colors
        self.theme = theme
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.height = height
        self.text_auto = text_auto
        self.barmode = barmode
        self.legend_title = legend_title
        self.theme_settings = self.THEME_SETTINGS.get(
            theme, self.THEME_SETTINGS["dark"]
        )
        self.fig = None
        self.create_chart()
        self.set_layout()
        self.apply_style()
        self.add_average_lines()
        # self.add_trend_annotations()
        self.add_legend()
        self.add_tooltips()
        self.add_custom_data()

    def create_chart(self):
        """Cria o gráfico de barras agrupadas."""
        self.fig = px.bar(
            self.data,
            x=self.x_col,
            y=self.y_col,
            color=self.color_col,
            color_discrete_sequence=self.colors,
            height=self.height,
            text_auto=self.text_auto,
            barmode=self.barmode,
        )

    def set_layout(self):
        """Define o layout do gráfico."""
        self.fig.update_layout(
            title=self.title,
            xaxis_title=self.xlabel,
            yaxis_title=self.ylabel,
            plot_bgcolor=self.theme_settings["bg_color"],
            paper_bgcolor=self.theme_settings["bg_color"],
            font=dict(color=self.theme_settings["title_color"]),
            xaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor=self.theme_settings["grid_color"],
            ),
            yaxis=dict(
                title_font=dict(size=14),
                tickfont=dict(size=12),
                gridcolor=self.theme_settings["grid_color"],
                tickformat=".2f",  # Formatar os valores do eixo Y com duas casas decimais
            ),
        )

    def apply_style(self):
        """Aplica o estilo ao gráfico."""
        self.fig.update_traces(
            marker=dict(
                line=dict(width=1, color=self.theme_settings["bar_line_color"])
            ),
            hovertemplate="%{x}: %{y:.2f}<extra></extra>",  # Tooltip com duas casas decimais
            texttemplate="%{y:.2f}",  # Formatar os valores no topo das barras com duas casas decimais
            textposition="outside",
        )

    def add_average_lines(self):
        """Adiciona linhas médias ao gráfico."""
        averages = self.data.groupby(self.x_col)[self.y_col].mean().reset_index()
        for i, row in averages.iterrows():
            # Adiciona a linha média
            self.fig.add_shape(
                type="line",
                x0=row[self.x_col],
                y0=0,
                x1=row[self.x_col],
                y1=row[self.y_col],
                line=dict(color="red", width=2, dash="dash"),
            )
            # Adiciona a anotação abaixo da linha
            self.fig.add_annotation(
                x=row[self.x_col],
                y=0,  # Posição no valor 0 para ficar abaixo da linha
                text=f"Média: {row[self.y_col]:.2f}",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=40,  # Ajuste a posição vertical (positivo para baixo)
                bgcolor=self.theme_settings["hover_bg"],
                bordercolor=self.theme_settings["grid_color"],
                font=dict(color=self.theme_settings["hover_font_color"]),
            )

    def add_legend(self):
        """Adiciona a legenda ao gráfico."""
        self.fig.update_layout(
            legend=dict(
                title=self.legend_title,
                font=dict(color=self.theme_settings["title_color"]),
                bgcolor=self.theme_settings["legend_bg"],
                bordercolor=self.theme_settings["grid_color"],
            )
        )

    def show(self, **kwargs):
        """Exibe o gráfico no Streamlit."""
        st.plotly_chart(self.fig, use_container_width=True, **kwargs)

    def add_tooltips(self):
        """Adiciona tooltips personalizados ao gráfico."""
        self.fig.update_traces(hovertemplate="%{x}: %{y}<extra></extra>")

    def add_custom_data(self):
        """Adiciona dados personalizados ao gráfico."""
        self.fig.update_traces(
            customdata=self.data[self.color_col],
            hovertemplate="%{x}: %{y}<br>%{customdata}<extra></extra>",
        )

    # def add_trend_annotations(self):
    #     """Adiciona anotações de tendência ao gráfico."""
    #     trends = self.data.groupby(self.x_col)[self.y_col].agg(['min', 'max']).reset_index()
    #     for i, row in trends.iterrows():
    #         # Adiciona a anotação de tendência
    #         self.fig.add_annotation(
    #             x=row[self.x_col],
    #             y=row['max'],
    #             text="Tendência",
    #             showarrow=True,
    #             arrowhead=2,
    #             ax=0,
    #             ay=-40,
    #             bgcolor=self.theme_settings['hover_bg'],
    #             bordercolor=self.theme_settings['grid_color'],
    #             font=dict(color=self.theme_settings['hover_font_color'])
    #         )

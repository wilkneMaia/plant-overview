import plotly.express as px
import streamlit as st


class Heatmap:
    """Classe para criar heatmaps com temas e personalizações."""

    THEME_SETTINGS = {
        "dark": {
            "title_color": "white",
            "axis_color": "white",
            "bg_color": "rgba(0,0,0,0)",
            "grid_color": "rgba(80,80,80,0.3)",
            "legend_bg": "rgba(40,40,40,0.7)",
            "hover_bg": "rgba(30,30,30,0.9)",
            "hover_font_color": "white",
        },
        "light": {
            "title_color": "#333333",
            "axis_color": "#333333",
            "bg_color": "white",
            "grid_color": "rgba(200,200,200,0.3)",
            "legend_bg": "rgba(240,240,240,0.7)",
            "hover_bg": "rgba(255,255,255,0.9)",
            "hover_font_color": "#333333",
        },
    }

    def __init__(
        self,
        data_values: list,
        x_labels: list,
        y_labels: list,
        color_scale: list,
        theme: str = "light",
        title: str = "",
        subtitle: str = "",
        xlabel: str = None,  # Tornando opcional
        ylabel: str = None,  # Tornando opcional
        height: int = 600,
        width: int = None,  # Novo parâmetro para controlar a largura
        title_font: dict = None,
        subtitle_font: dict = None,
        unit: str = "kWh",
        margin: dict = None,
        show_colorbar: bool = True,  # add parameter
    ):
        """
        Inicializa o heatmap.

        Args:
            data_values: Valores do heatmap.
            x_labels: Rótulos para o eixo x.
            y_labels: Rótulos para o eixo y.
            color_scale: Escala de cores para o heatmap.
            theme: 'dark' ou 'light' - define o esquema de cores.
            title: Título do gráfico.
            subtitle: Subtítulo do gráfico.
            xlabel: Rótulo do eixo x.
            ylabel: Rótulo do eixo y.
            height: Altura do gráfico.
            width: Largura do gráfico.
            title_font: Configurações de fonte para o título.
            subtitle_font: Configurações de fonte para o subtítulo.
            unit: Unidade de medida.
            margin: Margens personalizadas.
            show_colorbar: Show or hide colorbar
        """
        self.data_values = data_values
        self.x_labels = x_labels
        self.y_labels = y_labels
        self.color_scale = color_scale
        self.theme = theme
        self.title = title
        self.subtitle = subtitle
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.height = height
        self.width = width if width else 1200  # Definir uma largura padrão se None
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.unit = unit
        self.margin = (
            margin if margin else {"l": 40, "r": 40, "t": 40, "b": 40}
        )  # Ajustar margens
        self.show_colorbar = show_colorbar  # assign to self
        self.theme_settings = self.THEME_SETTINGS.get(
            theme, self.THEME_SETTINGS["dark"]
        )
        self.fig = None
        self.process_data()
        self.create_chart()
        self.set_layout()
        self.apply_style()

    def process_data(self):
        """Divide os valores por 100 para transformar de kWh para MWh."""
        self.data_values = [[value / 100 for value in row] for row in self.data_values]

    def create_chart(self):
        """Cria o heatmap."""
        self.fig = px.imshow(
            self.data_values,
            labels=dict(x=self.xlabel, y=self.ylabel, color=f"Valor ({self.unit})"),
            color_continuous_scale=self.color_scale,
            aspect="auto",
            text_auto=".2f",  # Mostra duas casas decimais
            x=self.x_labels,
            y=self.y_labels,
        )

    def set_layout(self):
        """Define o layout do heatmap."""
        layout_config = {
            "title": {
                "text": (
                    f"<b>{self.title}</b><br><span style='font-size:{self.subtitle_font['size'] if self.subtitle_font else 16}px;color:{self.subtitle_font['color'] if self.subtitle_font else self.theme_settings['title_color']}'>{self.subtitle}</span>"
                ),
                "font": (
                    self.title_font
                    or {"size": 22, "color": self.theme_settings["title_color"]}
                ),
                "y": 0.95,
                "x": 0.06,
                "xanchor": "left",  # Alinhado à esquerda
            },
            "plot_bgcolor": self.theme_settings["bg_color"],
            "paper_bgcolor": self.theme_settings["bg_color"],
            "font": {"color": self.theme_settings["axis_color"]},
            "height": self.height,
            "width": self.width,  # Ajustando a largura do gráfico
            "margin": {
                "l": 40,
                "r": 40,
                "t": 100,
                "b": 40,
            },  # Aumenta a margem superior para espaçar o título do gráfico
            "coloraxis_showscale": False,  # Remove a legenda do lado direito
        }

        # Remover linhas horizontais e mostrar apenas as linhas base dos eixos
        layout_config["xaxis"] = {
            "title": (
                {"text": f"<b>{self.xlabel}</b>", "font": {"size": 14}}
                if self.xlabel
                else None
            ),
            "tickfont": {"size": 12, "color": self.theme_settings["axis_color"]},
            "gridcolor": "rgba(0,0,0,0)",  # Remove as linhas horizontais
            "zerolinecolor": self.theme_settings["grid_color"],  # Linha base X
            "zerolinewidth": 2,
            "showline": True,
            "linecolor": self.theme_settings["axis_color"],
        }

        layout_config["yaxis"] = {
            "title": (
                {"text": f"<b>{self.ylabel}</b>", "font": {"size": 14}}
                if self.ylabel
                else None
            ),
            "tickfont": {"size": 12, "color": self.theme_settings["axis_color"]},
            "gridcolor": "rgba(0,0,0,0)",  # Remove as linhas horizontais
            "zerolinecolor": self.theme_settings["grid_color"],  # Linha base Y
            "zerolinewidth": 2,
            "showline": True,
            "linecolor": self.theme_settings["axis_color"],
        }

        # Aplica as configurações
        self.fig.update_layout(layout_config)

    def apply_style(self):
        """Aplica o estilo ao heatmap."""
        self.fig.update_traces(
            hovertemplate=f"<b>{self.xlabel}: %{{x}}<br>{self.ylabel}: %{{y}}<br>Valor: %{{z:.2f}} {self.unit}</b><extra></extra>"
        )

    def set_titles(
        self,
        title: str = None,
        subtitle: str = None,
        title_font: dict = None,
        subtitle_font: dict = None,
    ):
        """Configura título e subtítulo do gráfico"""
        if title is not None:
            self.title = title
        if subtitle is not None:
            self.subtitle = subtitle
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.set_layout()
        return self

    def show(self):
        """Exibe o heatmap no Streamlit."""
        st.plotly_chart(self.fig, use_container_width=True)

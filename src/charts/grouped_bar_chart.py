import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


class GroupedBarChart:
    THEME_SETTINGS = {
        "dark": {
            "title_color": "white",
            "subtitle_color": "#AAAAAA",
            "axis_color": "white",
            "bg_color": "rgba(0,0,0,0)",
            "grid_color": "rgba(80,80,80,0.3)",
            "legend_bg": "rgba(40,40,40,0.7)",
            "hover_bg": "rgba(30,30,30,0.9)",
            "hover_font_color": "white",
            "bar_line_color": "rgba(80,80,80,0.8)",
        },
        "light": {
            "title_color": "#333333",
            "subtitle_color": "#666666",
            "axis_color": "#333333",
            "bg_color": "white",
            "grid_color": "rgba(200,200,200,0.3)",
            "legend_bg": "rgba(240,240,240,0.7)",
            "hover_bg": "rgba(255,255,255,0.9)",
            "hover_font_color": "#333333",
            "bar_line_color": "rgba(200,200,200,0.8)",
        },
    }

    def __init__(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        color_col: str,
        colors: list[str],
        theme: str = "dark",
        title: str = None,
        subtitle: str = None,
        xlabel: str = None,
        ylabel: str = None,
        height: int = 450,
        text_auto: bool = True,
        barmode: str = "group",
        legend_title: str = "Legenda",
    ):
        self.data = data.copy()
        self.x_col = x_col
        self.y_col = y_col
        self.color_col = color_col
        self.colors = colors
        self.theme = theme.lower()
        self.title = title
        self.subtitle = subtitle
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

        # ✅ Converte os valores do eixo X para string
        self.data[self.x_col] = self.data[self.x_col].astype(str)

        self.create_chart()
        self.set_layout()
        self.add_styles_and_averages()

    def create_chart(self):
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
        self.fig.update_layout(
            title={
                "text": (
                    f"<b>{self.title or 'Produção Anual por Microinversor'}</b><br>"
                    f"<span style='font-size:14px;color:gray'>{self.subtitle or 'Comparativo da geração de energia entre microinversores nos anos de 2021 a 2025, com destaque para a média anual consolidada.'}</span>"
                ),
                "font": {
                    "size": 22,
                    "color": self.theme_settings["title_color"],
                    "family": "Arial",
                },
                "y": 0.95,
                "x": 0.03,
                "xanchor": "left",
            },
            plot_bgcolor=self.theme_settings["bg_color"],
            paper_bgcolor=self.theme_settings["bg_color"],
            font=dict(color=self.theme_settings["title_color"]),
            margin=dict(l=40, r=30, t=100, b=40),
            xaxis=dict(
                title=self.xlabel if self.xlabel else None,
                showgrid=False,
                zeroline=True,
                zerolinecolor=self.theme_settings["grid_color"],
                zerolinewidth=2,
                showline=True,
                linecolor=self.theme_settings["axis_color"],
                title_font=dict(size=14) if self.xlabel else None,
            ),
            yaxis=dict(
                title=self.ylabel if self.ylabel else None,
                showgrid=False,
                zeroline=True,
                zerolinecolor=self.theme_settings["grid_color"],
                zerolinewidth=2,
                showline=True,
                linecolor=self.theme_settings["axis_color"],
                title_font=dict(size=14) if self.ylabel else None,
            ),
            legend=dict(
                title=dict(
                    text=self.legend_title,
                    font=dict(size=12, color=self.theme_settings["title_color"]),
                ),
                bgcolor=self.theme_settings["legend_bg"],
                bordercolor=self.theme_settings["grid_color"],
                font=dict(color=self.theme_settings["title_color"], size=11),
                orientation="h",
                x=0,
                y=-0.25,
                xanchor="left",
                yanchor="top",
            ),
        )

    def add_styles_and_averages(self):
        self.fig.update_traces(
            marker_line=dict(width=1, color=self.theme_settings["bar_line_color"]),
            hovertemplate=(
                f"{(self.xlabel + ': ') if self.xlabel else ''}%{{x}}<br>"
                f"{(self.ylabel + ': ') if self.ylabel else ''}%{{y:,.2f}} kWh<extra></extra>"
            ),
            texttemplate="%{y:.2f}",
            textposition="outside",
        )

        # ✅ Garante eixo X categórico (strings) nas médias
        self.data[self.x_col] = self.data[self.x_col].astype(str)
        averages = self.data.groupby(self.x_col)[self.y_col].mean().reset_index()
        averages[self.x_col] = averages[self.x_col].astype(str)

        for _, row in averages.iterrows():
            x_val = row[self.x_col]
            self.fig.add_trace(
                go.Scatter(
                    x=[x_val, x_val],
                    y=[0, row[self.y_col]],
                    mode="lines",
                    line=dict(color="red", width=2, dash="dash"),
                    showlegend=False,
                )
            )
            self.fig.add_annotation(
                x=x_val,
                y=0,
                text=f"Média: {row[self.y_col]:.2f}",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=40,
                bgcolor=self.theme_settings["hover_bg"],
                bordercolor=self.theme_settings["grid_color"],
                font=dict(color=self.theme_settings["hover_font_color"]),
            )

    def show(self, **kwargs):
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
        st.plotly_chart(self.fig, use_container_width=True, **kwargs)

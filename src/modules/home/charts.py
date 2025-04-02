import pandas as pd
import plotly.express as px
import streamlit as st

from config.constants import Colors


# --- Gráficos ---
# Gráficos de energia gerada por microinversor
def plot_energy_heatmap_by_microinverter(data):
    """
    Cria um heatmap com anos inteiros no eixo X e melhor legibilidade
    """
    try:
        # Verificação e pré-processamento
        required = ["Microinversor", "Year", "Energy"]
        if not all(col in data.columns for col in required):
            raise ValueError(f"Colunas necessárias: {required}")

        # Garante que Year seja tratado como inteiro
        df = data.copy()
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").dropna().astype(int)

        # Agregação
        df_agg = df.groupby(["Microinversor", "Year"])["Energy"].sum().unstack()

        # Heatmap
        fig = px.imshow(
            df_agg,
            labels=dict(x="Ano", y="Microinversor", color="Energia (kWh)"),
            color_continuous_scale=Colors.GREEN_SEQUENTIAL,
            aspect="auto",
            text_auto=".1f",
        )

        # Formatação do eixo X (principal mudança)
        fig.update_xaxes(
            tickmode="array",
            tickvals=df_agg.columns,  # Valores originais
            ticktext=[str(int(year)) for year in df_agg.columns],  # Labels formatados
            tickangle=0,
        )

        # Layout final
        fig.update_layout(
            title="Energia por Ano e Microinversor",
            xaxis_title="Ano",
            yaxis_title="Microinversor",
            height=max(400, len(df_agg) * 25),
        )

        return fig

    except Exception as e:
        st.error(f"Erro ao criar heatmap: {e!s}")
        return None


def plot_line_comparison_by_year(df):
    """Exibe um gráfico de linhas comparativo com marcadores para análise mensal por ano"""
    try:
        # Prepara os dados
        monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

        # Cria o gráfico
        fig = px.line(
            monthly_comparison,
            x="Month",
            y="Energy",
            color="Year",
            markers=True,
            title="Comparativo de Geração por Mês e Ano",
            labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
            template="plotly_dark",
            color_discrete_sequence=Colors.GREEN_DISCRETE,  # Alterado para nossa paleta de verdes
        )

        # Customiza aparência
        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(size=8),
            hovertemplate="<b>%{fullData.name}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
        )

        # Adiciona linha de média anual para referência
        for i, year in enumerate(monthly_comparison["Year"].unique()):
            year_data = monthly_comparison[monthly_comparison["Year"] == year]
            year_avg = year_data["Energy"].mean()

            fig.add_shape(
                type="line",
                x0=1,
                y0=year_avg,
                x1=12,
                y1=year_avg,
                line=dict(
                    color=Colors.GREEN_DISCRETE[
                        i % len(Colors.GREEN_DISCRETE)
                    ],  # Usa nossa paleta de verdes
                    width=1.5,
                    dash="dash",
                ),
                opacity=0.7,
                name=f"Média {year}",
            )

        # Layout aprimorado
        fig.update_layout(
            title={
                "text": "Comparativo de Energia por Mês e Ano",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
            },
            xaxis={
                "title": {"text": "Mês", "font": {"size": 14, "color": "white"}},
                "tickvals": list(range(1, 13)),
                "ticktext": [
                    "Jan",
                    "Fev",
                    "Mar",
                    "Abr",
                    "Mai",
                    "Jun",
                    "Jul",
                    "Ago",
                    "Set",
                    "Out",
                    "Nov",
                    "Dez",
                ],
                "tickangle": 0,
                "gridcolor": "rgba(80, 80, 80, 0.3)",
                "tickangle": -45,
            },
            yaxis={
                "title": {
                    "text": "Energia Gerada (kWh)",
                    "font": {"size": 14, "color": "white"},
                },
                "gridcolor": "rgba(80, 80, 80, 0.3)",
                "zeroline": True,
                "zerolinecolor": "rgba(255, 255, 255, 0.2)",
            },
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="#181818",
            hovermode="x unified",
            legend={
                "title": "Ano",
                "orientation": "h",
                "y": -0.2,
                "bgcolor": "rgba(0,0,0,0.3)",
                "bordercolor": "rgba(255,255,255,0.2)",
                "borderwidth": 1,
            },
            margin=dict(l=50, r=30, t=80, b=50),
        )

        # Adiciona anotações de tendência (opcional)
        for year in monthly_comparison["Year"].unique():
            year_data = monthly_comparison[monthly_comparison["Year"] == year]
            year_trend = year_data["Energy"].iloc[-1] - year_data["Energy"].iloc[0]
            if abs(year_trend) > (
                year_data["Energy"].max() * 0.2
            ):  # Se a tendência for significativa
                trend_color = "green" if year_trend > 0 else "red"
                fig.add_annotation(
                    x=12,
                    y=year_data["Energy"].iloc[-1],
                    text=f"{'↑' if year_trend > 0 else '↓'} {abs(year_trend):.0f} kWh",
                    showarrow=False,
                    font=dict(color=trend_color, size=12),
                    xshift=15,
                )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e!s}")


def plot_energy_trend_by_year(df):
    """Exibe um gráfico de área comparativo dos meses por ano (não empilhado)"""
    try:
        # Prepara os dados
        monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
        # Cria o gráfico base
        fig = px.area(
            monthly_comparison,
            x="Month",
            y="Energy",
            color="Year",
            title="Comparativo de Energia por Mês e Ano",
            labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
            template="plotly_dark",
            color_discrete_sequence=Colors.GREEN_DISCRETE,  # Alterado para nossa paleta de verdes
        )
        # Aplica as customizações
        fig.update_traces(
            opacity=0.5,  # Transparência aqui
            line=dict(width=1),
            hovertemplate="<b>Ano %{color}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
        )
        # Layout aprimorado
        fig.update_layout(
            title={
                "text": "Comparativo de Energia por Mês e Ano",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",  # Adicione esta linha para centralizar o título
                "font": {"size": 18, "color": "white"},
            },
            xaxis={
                "title": {"text": "Mês", "font": {"size": 14, "color": "white"}},
                "tickvals": list(range(1, 13)),
                "ticktext": [
                    "Jan",
                    "Fev",
                    "Mar",
                    "Abr",
                    "Mai",
                    "Jun",
                    "Jul",
                    "Ago",
                    "Set",
                    "Out",
                    "Nov",
                    "Dez",
                ],
                "tickangle": 0,
                "tickangle": -45,
            },
            yaxis={
                "title": {
                    "text": "Energia Gerada (kWh)",
                    "font": {"size": 14, "color": "white"},
                },
                "gridcolor": "#404040",
            },
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="#181818",
            hovermode="x unified",
            legend={
                "title": "Ano",
                "orientation": "h",
                "y": -0.2,
                "bgcolor": "rgba(0,0,0,0.5)",
            },
            margin=dict(l=50, r=30, t=80, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e!s}")


def plot_microinverter_year_barchart(data):
    """
    Gráfico de barras agrupadas que:
    - Remove automaticamente barras com valor zero
    - Mantém a legenda apenas para microinversores com dados
    - Ordenação cronológica inteligente
    - Tooltips detalhados
    """
    try:
        # 1. VALIDAÇÃO INICIAL
        required_cols = {"Microinversor", "Year", "Energy"}
        if not required_cols.issubset(data.columns):
            missing = required_cols - set(data.columns)
            raise ValueError(f"Colunas faltando: {missing}")

        if data.empty:
            raise ValueError("DataFrame vazio")

        # 2. PRÉ-PROCESSAMENTO
        df = data.copy()
        # Limpeza de anos e conversão para inteiro
        df["Year"] = df["Year"].astype(str).str.extract(r"(\d+)")[0].astype(int)

        # Filtro crítico: remove registros com Energy <= 0
        df = df[df["Energy"] > 0].copy()

        if df.empty:
            raise ValueError("Nenhum dado positivo encontrado")

        # 3. AGREGAÇÃO E ORDENAÇÃO
        df_agg = (
            df.groupby(["Year", "Microinversor"], as_index=False)["Energy"]
            .sum()
            .sort_values(["Year", "Microinversor"])
        )

        # 4. CRIAÇÃO DO GRÁFICO
        fig = px.bar(
            df_agg,
            x="Year",
            y="Energy",
            color="Microinversor",
            barmode="group",
            title="<b>Distribuição de Energia por Ano</b><br><sup>Microinversores com produção > 0</sup>",
            color_discrete_sequence=Colors.GREEN_DISCRETE,
            text_auto=".2s",
            labels={"Energy": "Energia (kWh)", "Year": "Ano"},
            category_orders={"Year": sorted(df_agg["Year"].unique())},
        )

        # 5. CUSTOMIZAÇÃO AVANÇADA
        fig.update_layout(
            xaxis={
                "type": "category",
                "tickvals": sorted(df_agg["Year"].unique()),
                "ticktext": [
                    f"<b>{year}</b>" for year in sorted(df_agg["Year"].unique())
                ],
                "title": {"text": "<b>Ano</b>", "font": {"size": 14}},
            },
            yaxis={
                "title": {"text": "<b>Energia (kWh)</b>", "font": {"size": 14}},
                "gridcolor": "rgba(200,200,200,0.2)",
            },
            bargap=0.3,
            bargroupgap=0.1,
            hovermode="x unified",
            height=650,
            plot_bgcolor="rgba(0,0,0,0)",
            legend={
                "title": {
                    "text": "<b>Microinversores Ativos</b>",
                    "font": {"size": 12},
                },
                "orientation": "h",
                "y": -0.25,
            },
            margin={"t": 100, "b": 100},
        )

        fig.update_traces(
            marker_line_width=1,
            marker_line_color="white",
            opacity=0.9,
            textposition="outside",
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Ano: %{x}<br>"
                "Produção: %{y:,.2f} kWh<br>"
                "<extra></extra>"
            ),
            customdata=df_agg[["Microinversor"]],
        )

        # 6. ADICIONA ANOTAÇÃO EXPLICATIVA
        fig.add_annotation(
            text="*Barras com valor zero são omitidas automaticamente",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.35,
            showarrow=False,
            font={"size": 10, "color": "gray"},
        )

        return fig

    except Exception as e:
        st.error(f"Erro na geração do gráfico: {e!s}")
        if not data.empty:
            st.warning("Visualização parcial dos dados recebidos:")
            st.dataframe(data.head(3))
        return None


def create_bar_chart(
    data,
    *,
    x: str,
    y: str,
    title: str = "",
    xlabel: str = None,
    ylabel: str = None,
    template: str = "plotly_dark",
    margin: dict = None,
    color: str = Colors.PRIMARY_GREEN,
    show_values: bool = True,
    **layout_kwargs,
):
    """Cria um gráfico de barras altamente customizável com melhorias visuais."""
    # Valores padrão inteligentes
    xlabel = xlabel or x
    ylabel = ylabel or y
    margin = margin or dict(l=50, r=50, t=80, b=50)

    # Criação do gráfico base
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels={x: xlabel, y: ylabel},
        template=template,
        color_discrete_sequence=[color],
        text_auto=".2s" if show_values else False,
    )

    # Customização do layout
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
        },
        xaxis={
            "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
            "showgrid": False,
            "tickmode": "linear",
            "ticks": "outside",
            "tickwidth": 2,
            "tickangle": -45,  # Ângulo melhorado
            "tickfont": {"color": "#ffffff", "size": 12},
            "automargin": True,  # Previne corte de labels
        },
        yaxis={
            "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
            "showgrid": True,
            "gridcolor": "#404040",
            "zeroline": True,
            "zerolinewidth": 1,
            "zerolinecolor": "gray",
            "tickfont": {"color": "#ffffff", "size": 12},
            "automargin": True,
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        margin=margin,
        hovermode="x unified",  # Tooltips unificados
        hoverlabel={"bgcolor": "#2a2a2a", "font_size": 12, "font_family": "Arial"},
        uniformtext={"mode": "hide", "minsize": 10} if show_values else {},
        **layout_kwargs,
    )

    # Melhorias nas barras
    fig.update_traces(
        marker={
            "line": {"width": 1, "color": "#ffffff"},  # Borda branca nas barras
            "opacity": 0.9,  # Transparência leve
        },
        hovertemplate=(
            f"<b>{xlabel}:</b> %{{x}}<br>"
            f"<b>{ylabel}:</b> %{{y:,.2f}}<extra></extra>"
        ),
        textposition="outside",  # Posição dos valores
        textfont={"color": "white", "size": 12},
    )

    return fig


def plot_energy_production_by_year(df: pd.DataFrame) -> None:
    """Exibe o total de energia gerada por ano com cores gradientes de verde."""
    try:
        if not {"Year", "Energy"}.issubset(df.columns):
            st.error("Dados incompletos: faltam colunas 'Year' ou 'Energy'")
            return

        total_data = df.groupby("Year")["Energy"].sum().reset_index()
        colorscale = Colors.GREEN_SEQUENTIAL

        # Normaliza os valores para a escala de cores
        min_energy = total_data["Energy"].min()
        max_energy = total_data["Energy"].max()
        normalized = (total_data["Energy"] - min_energy) / (max_energy - min_energy)

        # Mapeia para cores
        color_indices = (normalized * (len(colorscale) - 1)).astype(int)
        colors = [colorscale[i] for i in color_indices]

        fig = create_bar_chart(
            data=total_data,
            x="Year",
            y="Energy",
            title="Produção Anual (kWh)",
            color=colors,
            show_values=True,
            margin=dict(l=60, r=30, t=100, b=70),
        )

        # Remove a legenda de cores (opcional)
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e!s}")

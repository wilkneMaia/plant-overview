import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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
    color: str = "#4ECDC4",  # Nova: cor das barras
    show_values: bool = True,  # Nova: exibir valores nas barras
    **layout_kwargs,
):
    """Cria um gráfico de barras altamente customizável com melhorias visuais."""
    # Valores padrão inteligentes
    xlabel = xlabel or x
    ylabel = ylabel or y
    margin = margin or dict(l=50, r=50, t=80, b=50)  # Margens aumentadas

    # Criação do gráfico base
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels={x: xlabel, y: ylabel},
        template=template,
        color_discrete_sequence=[color],  # Cor personalizada
        text_auto=".2s" if show_values else False,  # Mostra valores formatados
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


def plot_total_by_year(df: pd.DataFrame) -> None:
    """Exibe o total de energia gerada por ano com cores gradientes."""
    try:
        if not {"Year", "Energy"}.issubset(df.columns):
            st.error("Dados incompletos: faltam colunas 'Year' ou 'Energy'")
            return

        total_data = df.groupby("Year")["Energy"].sum().reset_index()
        colorscale = px.colors.sequential.Greens

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


def create_line_chart(
    df,
    *,
    x: str = "Month",
    y: str = "Energy",
    color_col: str = "Year",
    title: str = "Comparativo Mensal por Ano",
    xlabel: str = "Mês",
    ylabel: str = "Energia Gerada (kWh)",
    color_sequence: list = None,
    template: str = "plotly_dark",
    show_legend: bool = True,
    show_markers: bool = True,
    **layout_kwargs,
):
    """
    Cria um gráfico de linhas comparativo com múltiplas melhorias visuais.

    Args:
        df: DataFrame com os dados
        x: Coluna para eixo X (padrão: "Month")
        y: Coluna para eixo Y (padrão: "Energy")
        color_col: Coluna para diferenciação por cor (padrão: "Year")
        title: Título do gráfico
        xlabel: Label do eixo X
        ylabel: Label do eixo Y
        color_sequence: Lista de cores personalizadas
        template: Template do Plotly
        show_legend: Mostrar legenda
        show_markers: Mostrar marcadores nas linhas
        **layout_kwargs: Argumentos adicionais para update_layout()

    Returns:
        plotly.graph_objects.Figure
    """
    # Agregação dos dados
    monthly_comparison = df.groupby([color_col, x])[y].sum().reset_index()

    # Configuração de cores
    color_sequence = color_sequence or px.colors.qualitative.Plotly

    # Criação do gráfico
    fig = px.line(
        monthly_comparison,
        x=x,
        y=y,
        color=color_col,
        title=title,
        labels={x: xlabel, y: ylabel, color_col: "Ano"},
        template=template,
        markers=show_markers,
        color_discrete_sequence=color_sequence,
        line_shape="spline",  # Linhas suavizadas
        hover_data={color_col: True, x: True, y: ":.2f"},
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
            "tickmode": "array",
            "tickvals": list(range(1, 13)),  # Garante todos os meses
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
            "tickfont": {"color": "#ffffff", "size": 12},
            "automargin": True,
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
        legend={
            "title_text": "Ano",
            "bgcolor": "rgba(0,0,0,0.5)",
            "font": {"color": "white"},
            "orientation": "h",
            "y": -0.2,  # Posiciona a legenda abaixo
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#181818",
        margin={"l": 60, "r": 40, "t": 80, "b": 60},
        hovermode="x unified",
        hoverlabel={"bgcolor": "#2a2a2a", "font_size": 12, "font_family": "Arial"},
        **layout_kwargs,
    )

    # Melhorias nas linhas
    fig.update_traces(
        line={"width": 2.5},
        marker={"size": 8, "line": {"width": 1, "color": "DarkSlateGrey"}},
        hovertemplate=(
            f"<b>Ano:</b> %{{customdata[0]}}<br>"
            f"<b>{xlabel}:</b> %{{customdata[1]}}<br>"
            f"<b>{ylabel}:</b> %{{customdata[2]:,.2f}}<extra></extra>"
        ),
    )

    return fig


def plot_comparative_months_by_year_line(df):
    """Exibe um gráfico de linha comparativo dos meses por ano"""
    try:
        monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

        fig = create_line_chart(  # Corrigido: chamando create_line_chart em vez de si mesma
            monthly_comparison,
            title="Produção Mensal Comparativa",
            color_sequence=px.colors.qualitative.Vivid,
            show_markers=True,
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Ocorreu um erro ao exibir o gráfico: {e}")


def create_area_chart(
    df,
    *,
    x: str = "Month",
    y: str = "Energy",
    color_col: str = "Year",
    title: str = "Comparativo Mensal por Ano",
    xlabel: str = "Mês",
    ylabel: str = "Energia Gerada (kWh)",
    color_sequence: list = None,
    template: str = "plotly_dark",
    show_legend: bool = True,
    stacked: bool = True,  # Novo: controle booleano para empilhamento
    **layout_kwargs,
):
    """
    Cria um gráfico de área empilhada com correção do parâmetro stackgroup.

    Args:
        df: DataFrame com os dados
        stacked: Se True, áreas serão empilhadas (default)
        ... (outros parâmetros permanecem iguais)
    """
    # Configuração de cores
    color_sequence = color_sequence or px.colors.qualitative.Plotly

    # Criação do gráfico base
    fig = px.area(
        df,
        x=x,
        y=y,
        color=color_col,
        title=title,
        labels={x: xlabel, y: ylabel, color_col: "Ano"},
        template=template,
        color_discrete_sequence=color_sequence,
        hover_data={color_col: True, x: True, y: ":.2f"},
        line_shape="spline",
    )

    # Aplica empilhamento se necessário
    if stacked:
        fig.update_traces(stackgroup="stack")  # Nome arbitrário para o grupo

    # Restante da configuração do layout (mantido igual)
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
            "tickmode": "array",
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
            "tickfont": {"color": "#ffffff", "size": 12},
            "automargin": True,
        },
        # ... (restante do layout permanece igual)
    )

    return fig


def plot_area_stack_by_year(df):
    """Exibe um gráfico de área empilhada comparativo dos meses por ano"""
    try:
        monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

        fig = create_area_chart(
            monthly_comparison,
            title="Produção Mensal Comparativa (Área Empilhada)",
            color_sequence=px.colors.qualitative.Vivid,
            stackgroup="year",
        )

        # Aplica as customizações
        fig.update_traces(
            opacity=0.5,  # Transparência aqui
            line=dict(width=1),
            hovertemplate="<b>Ano %{color}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Ocorreu um erro ao exibir o gráfico: {e}")


def plot_area_overlay_by_year(df):
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
            color_discrete_sequence=px.colors.qualitative.Vivid,
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
                "text": "Comparativo de Energia por Mês e Ano (Áreas Sobrepostas)",
                "y": 0.95,
                "x": 0.5,
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


def plot_scatter_by_year(df):
    """Exibe um gráfico de dispersão comparativo dos meses por ano"""
    monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
    fig = px.scatter(
        monthly_comparison,
        x="Month",
        y="Energy",
        color="Year",
        title="Comparativo de Energia Gerada por Mês e Ano (Dispersão)",
        labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
        template="plotly_dark",
    )
    fig.update_layout(
        title=dict(
            text="Comparativo de Energia Gerada por Mês e Ano",
            x=0.5,
            font=dict(size=16, color="white"),
        ),
        xaxis=dict(
            title="Mês",
            showgrid=False,
            tickmode="linear",
            ticks="outside",
            tickwidth=2,
            tickangle=45,
            tickfont=dict(color="#ffffff"),
        ),
        yaxis=dict(
            title="Energia Gerada (kWh)",
            showgrid=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="gray",
            tickfont=dict(color="#ffffff"),
        ),
        plot_bgcolor="#181818",
        paper_bgcolor="#181818",
        margin=dict(l=40, r=40, t=40, b=40),
    )
    st.plotly_chart(fig)


def plot_candlestick_by_month(df):
    """Exibe um gráfico Candlestick comparativo dos meses por ano"""
    monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
    fig_data = []
    for year in monthly_comparison["Year"].unique():
        year_data = monthly_comparison[monthly_comparison["Year"] == year]
        fig_data.append(
            go.Candlestick(
                x=year_data["Month"],
                open=[year_data["Energy"].iloc[0]]
                * len(
                    year_data
                ),  # Energia do primeiro mês do ano repetida para todos os meses
                high=[year_data["Energy"].max()]
                * len(year_data),  # Energia máxima repetida para todos os meses
                low=[year_data["Energy"].min()]
                * len(year_data),  # Energia mínima repetida para todos os meses
                close=[year_data["Energy"].iloc[-1]]
                * len(year_data),  # Energia do último mês repetida para todos os meses
                name=str(year),
            )
        )

    fig = go.Figure(fig_data)
    fig.update_layout(
        title=dict(
            text="Comparativo de Energia Gerada por Mês e Ano (Candlestick)",
            x=0.5,
            font=dict(size=16, color="white"),
        ),
        xaxis=dict(
            title="Mês",
            tickmode="linear",
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            showgrid=False,
            ticks="outside",
            tickwidth=2,
            tickangle=45,
            tickfont=dict(color="#ffffff"),
        ),
        yaxis=dict(
            title="Energia Gerada (kWh)",
            showgrid=True,
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="gray",
            tickfont=dict(color="#ffffff"),
        ),
        plot_bgcolor="#181818",
        paper_bgcolor="#181818",
        margin=dict(l=40, r=40, t=40, b=40),
    )
    st.plotly_chart(fig)

import plotly.express as px
import streamlit as st

# Paleta principal verde para séries individuais
PRIMARY_GREEN = "#00A878"  # Verde vibrante principal

# Paleta de verdes sequenciais para gradientes
GREEN_SEQUENTIAL = [
    "#e0f5ee",
    "#c1e9db",
    "#a2dec9",
    "#83d3b6",
    "#64c8a4",
    "#45bd91",
    "#26b27f",
    "#07a76c",
    "#059059",
    "#047a47",
]

# Paleta para múltiplas séries (discretas) com variações de verde e cores complementares
GREEN_DISCRETE = [
    "#00A878",  # Verde principal (mais vibrante)
    "#004B49",  # Verde profundo (contraste máximo)
    "#7DCD85",  # Verde claro
    "#027357",  # Verde escuro
    "#C6EBBE",  # Verde pálido
    "#36877A",  # Verde-petróleo
    "#4ECDC4",  # Verde-água
    "#87D37C",  # Verde médio
    "#B5EAD7",  # Verde menta
    "#C4E0B0",  # Verde pastel
]


# def create_bar_chart(
#     data,
#     *,
#     x: str,
#     y: str,
#     title: str = "",
#     xlabel: str = None,
#     ylabel: str = None,
#     template: str = "plotly_dark",
#     margin: dict = None,
#     color: str = PRIMARY_GREEN,
#     show_values: bool = True,
#     **layout_kwargs,
# ):
#     """Cria um gráfico de barras altamente customizável com melhorias visuais."""
#     # Valores padrão inteligentes
#     xlabel = xlabel or x
#     ylabel = ylabel or y
#     margin = margin or dict(l=50, r=50, t=80, b=50)

#     # Criação do gráfico base
#     fig = px.bar(
#         data,
#         x=x,
#         y=y,
#         title=title,
#         labels={x: xlabel, y: ylabel},
#         template=template,
#         color_discrete_sequence=[color],
#         text_auto=".2s" if show_values else False,
#     )

#     # Customização do layout
#     fig.update_layout(
#         title={
#             "text": title,
#             "y": 0.95,
#             "x": 0.5,
#             "xanchor": "center",
#             "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
#         },
#         xaxis={
#             "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
#             "showgrid": False,
#             "tickmode": "linear",
#             "ticks": "outside",
#             "tickwidth": 2,
#             "tickangle": -45,  # Ângulo melhorado
#             "tickfont": {"color": "#ffffff", "size": 12},
#             "automargin": True,  # Previne corte de labels
#         },
#         yaxis={
#             "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
#             "showgrid": True,
#             "gridcolor": "#404040",
#             "zeroline": True,
#             "zerolinewidth": 1,
#             "zerolinecolor": "gray",
#             "tickfont": {"color": "#ffffff", "size": 12},
#             "automargin": True,
#         },
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="#181818",
#         margin=margin,
#         hovermode="x unified",  # Tooltips unificados
#         hoverlabel={"bgcolor": "#2a2a2a", "font_size": 12, "font_family": "Arial"},
#         uniformtext={"mode": "hide", "minsize": 10} if show_values else {},
#         **layout_kwargs,
#     )

#     # Melhorias nas barras
#     fig.update_traces(
#         marker={
#             "line": {"width": 1, "color": "#ffffff"},  # Borda branca nas barras
#             "opacity": 0.9,  # Transparência leve
#         },
#         hovertemplate=(
#             f"<b>{xlabel}:</b> %{{x}}<br>"
#             f"<b>{ylabel}:</b> %{{y:,.2f}}<extra></extra>"
#         ),
#         textposition="outside",  # Posição dos valores
#         textfont={"color": "white", "size": 12},
#     )

#     return fig


# def plot_energy_production_by_year(df: pd.DataFrame) -> None:
#     """Exibe o total de energia gerada por ano com cores gradientes de verde."""
#     try:
#         if not {"Year", "Energy"}.issubset(df.columns):
#             st.error("Dados incompletos: faltam colunas 'Year' ou 'Energy'")
#             return

#         total_data = df.groupby("Year")["Energy"].sum().reset_index()
#         colorscale = GREEN_SEQUENTIAL  # Usando nossa paleta verde sequencial

#         # Normaliza os valores para a escala de cores
#         min_energy = total_data["Energy"].min()
#         max_energy = total_data["Energy"].max()
#         normalized = (total_data["Energy"] - min_energy) / (max_energy - min_energy)

#         # Mapeia para cores
#         color_indices = (normalized * (len(colorscale) - 1)).astype(int)
#         colors = [colorscale[i] for i in color_indices]

#         fig = create_bar_chart(
#             data=total_data,
#             x="Year",
#             y="Energy",
#             title="Produção Anual (kWh)",
#             color=colors,
#             show_values=True,
#             margin=dict(l=60, r=30, t=100, b=70),
#         )

#         # Remove a legenda de cores (opcional)
#         fig.update_layout(showlegend=False)

#         st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

#     except Exception as e:
#         st.error(f"Erro ao gerar gráfico: {e!s}")


# def plot_energy_heatmap_by_microinverter(data):
#     """
#     Cria um heatmap com anos inteiros no eixo X e melhor legibilidade
#     """
#     try:
#         # Verificação e pré-processamento
#         required = ["Microinversor", "Year", "Energy"]
#         if not all(col in data.columns for col in required):
#             raise ValueError(f"Colunas necessárias: {required}")

#         # Garante que Year seja tratado como inteiro
#         df = data.copy()
#         df["Year"] = pd.to_numeric(df["Year"], errors="coerce").dropna().astype(int)

#         # Agregação
#         df_agg = df.groupby(["Microinversor", "Year"])["Energy"].sum().unstack()

#         # Heatmap
#         fig = px.imshow(
#             df_agg,
#             labels=dict(x="Ano", y="Microinversor", color="Energia (kWh)"),
#             color_continuous_scale=GREEN_SEQUENTIAL,
#             aspect="auto",
#             text_auto=".1f",
#         )

#         # Formatação do eixo X (principal mudança)
#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=df_agg.columns,  # Valores originais
#             ticktext=[str(int(year)) for year in df_agg.columns],  # Labels formatados
#             tickangle=0,
#         )

#         # Layout final
#         fig.update_layout(
#             title="Energia por Ano e Microinversor",
#             xaxis_title="Ano",
#             yaxis_title="Microinversor",
#             height=max(400, len(df_agg) * 25),
#         )

#         return fig

#     except Exception as e:
#         st.error(f"Erro ao criar heatmap: {e!s}")
#         return None


# def create_microinverter_year_barchart(data):
    # """
    # Gráfico de barras agrupadas que:
    # - Remove automaticamente barras com valor zero
    # - Mantém a legenda apenas para microinversores com dados
    # - Ordenação cronológica inteligente
    # - Tooltips detalhados
    # """
    # try:
    #     # 1. VALIDAÇÃO INICIAL
    #     required_cols = {"Microinversor", "Year", "Energy"}
    #     if not required_cols.issubset(data.columns):
    #         missing = required_cols - set(data.columns)
    #         raise ValueError(f"Colunas faltando: {missing}")

    #     if data.empty:
    #         raise ValueError("DataFrame vazio")

    #     # 2. PRÉ-PROCESSAMENTO
    #     df = data.copy()
    #     # Limpeza de anos e conversão para inteiro
    #     df["Year"] = df["Year"].astype(str).str.extract(r"(\d+)")[0].astype(int)

    #     # Filtro crítico: remove registros com Energy <= 0
    #     df = df[df["Energy"] > 0].copy()

    #     if df.empty:
    #         raise ValueError("Nenhum dado positivo encontrado")

    #     # 3. AGREGAÇÃO E ORDENAÇÃO
    #     df_agg = (
    #         df.groupby(["Year", "Microinversor"], as_index=False)["Energy"]
    #         .sum()
    #         .sort_values(["Year", "Microinversor"])
    #     )

    #     # 4. CRIAÇÃO DO GRÁFICO
    #     fig = px.bar(
    #         df_agg,
    #         x="Year",
    #         y="Energy",
    #         color="Microinversor",
    #         barmode="group",
    #         title="<b>Distribuição de Energia por Ano</b><br><sup>Microinversores com produção > 0</sup>",
    #         color_discrete_sequence=GREEN_DISCRETE,
    #         text_auto=".2s",
    #         labels={"Energy": "Energia (kWh)", "Year": "Ano"},
    #         category_orders={"Year": sorted(df_agg["Year"].unique())},
    #     )

    #     # 5. CUSTOMIZAÇÃO AVANÇADA
    #     fig.update_layout(
    #         xaxis={
    #             "type": "category",
    #             "tickvals": sorted(df_agg["Year"].unique()),
    #             "ticktext": [
    #                 f"<b>{year}</b>" for year in sorted(df_agg["Year"].unique())
    #             ],
    #             "title": {"text": "<b>Ano</b>", "font": {"size": 14}},
    #         },
    #         yaxis={
    #             "title": {"text": "<b>Energia (kWh)</b>", "font": {"size": 14}},
    #             "gridcolor": "rgba(200,200,200,0.2)",
    #         },
    #         bargap=0.3,
    #         bargroupgap=0.1,
    #         hovermode="x unified",
    #         height=650,
    #         plot_bgcolor="rgba(0,0,0,0)",
    #         legend={
    #             "title": {
    #                 "text": "<b>Microinversores Ativos</b>",
    #                 "font": {"size": 12},
    #             },
    #             "orientation": "h",
    #             "y": -0.25,
    #         },
    #         margin={"t": 100, "b": 100},
    #     )

    #     fig.update_traces(
    #         marker_line_width=1,
    #         marker_line_color="white",
    #         opacity=0.9,
    #         textposition="outside",
    #         hovertemplate=(
    #             "<b>%{customdata[0]}</b><br>"
    #             "Ano: %{x}<br>"
    #             "Produção: %{y:,.2f} kWh<br>"
    #             "<extra></extra>"
    #         ),
    #         customdata=df_agg[["Microinversor"]],
    #     )

    #     # 6. ADICIONA ANOTAÇÃO EXPLICATIVA
    #     fig.add_annotation(
    #         text="*Barras com valor zero são omitidas automaticamente",
    #         xref="paper",
    #         yref="paper",
    #         x=0.5,
    #         y=-0.35,
    #         showarrow=False,
    #         font={"size": 10, "color": "gray"},
    #     )

    #     return fig

    # except Exception as e:
    #     st.error(f"Erro na geração do gráfico: {e!s}")
    #     if not data.empty:
    #         st.warning("Visualização parcial dos dados recebidos:")
    #         st.dataframe(data.head(3))
    #     return None


# def plot_energy_trend_by_year(df):
#     """Exibe um gráfico de área comparativo dos meses por ano (não empilhado)"""
#     try:
#         # Prepara os dados
#         monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
#         # Cria o gráfico base
#         fig = px.area(
#             monthly_comparison,
#             x="Month",
#             y="Energy",
#             color="Year",
#             title="Comparativo de Energia por Mês e Ano",
#             labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
#             template="plotly_dark",
#             color_discrete_sequence=GREEN_DISCRETE,  # Alterado para nossa paleta de verdes
#         )
#         # Aplica as customizações
#         fig.update_traces(
#             opacity=0.5,  # Transparência aqui
#             line=dict(width=1),
#             hovertemplate="<b>Ano %{color}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
#         )
#         # Layout aprimorado
#         fig.update_layout(
#             title={
#                 "text": "Comparativo de Energia por Mês e Ano",
#                 "y": 0.95,
#                 "x": 0.5,
#                 "xanchor": "center",  # Adicione esta linha para centralizar o título
#                 "font": {"size": 18, "color": "white"},
#             },
#             xaxis={
#                 "title": {"text": "Mês", "font": {"size": 14, "color": "white"}},
#                 "tickvals": list(range(1, 13)),
#                 "ticktext": [
#                     "Jan",
#                     "Fev",
#                     "Mar",
#                     "Abr",
#                     "Mai",
#                     "Jun",
#                     "Jul",
#                     "Ago",
#                     "Set",
#                     "Out",
#                     "Nov",
#                     "Dez",
#                 ],
#                 "tickangle": 0,
#                 "tickangle": -45,
#             },
#             yaxis={
#                 "title": {
#                     "text": "Energia Gerada (kWh)",
#                     "font": {"size": 14, "color": "white"},
#                 },
#                 "gridcolor": "#404040",
#             },
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="#181818",
#             hovermode="x unified",
#             legend={
#                 "title": "Ano",
#                 "orientation": "h",
#                 "y": -0.2,
#                 "bgcolor": "rgba(0,0,0,0.5)",
#             },
#             margin=dict(l=50, r=30, t=80, b=50),
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     except Exception as e:
#         st.error(f"Erro ao gerar gráfico: {e!s}")


# def plot_line_comparison_by_year(df):
#     """Exibe um gráfico de linhas comparativo com marcadores para análise mensal por ano"""
#     try:
#         # Prepara os dados
#         monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

#         # Cria o gráfico
#         fig = px.line(
#             monthly_comparison,
#             x="Month",
#             y="Energy",
#             color="Year",
#             markers=True,
#             title="Comparativo de Geração por Mês e Ano",
#             labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
#             template="plotly_dark",
#             color_discrete_sequence=GREEN_DISCRETE,  # Alterado para nossa paleta de verdes
#         )

#         # Customiza aparência
#         fig.update_traces(
#             line=dict(width=2.5),
#             marker=dict(size=8),
#             hovertemplate="<b>%{fullData.name}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
#         )

#         # Adiciona linha de média anual para referência
#         for i, year in enumerate(monthly_comparison["Year"].unique()):
#             year_data = monthly_comparison[monthly_comparison["Year"] == year]
#             year_avg = year_data["Energy"].mean()

#             fig.add_shape(
#                 type="line",
#                 x0=1,
#                 y0=year_avg,
#                 x1=12,
#                 y1=year_avg,
#                 line=dict(
#                     color=GREEN_DISCRETE[
#                         i % len(GREEN_DISCRETE)
#                     ],  # Usa nossa paleta de verdes
#                     width=1.5,
#                     dash="dash",
#                 ),
#                 opacity=0.7,
#                 name=f"Média {year}",
#             )

#         # Layout aprimorado
#         fig.update_layout(
#             title={
#                 "text": "Comparativo de Energia por Mês e Ano",
#                 "y": 0.95,
#                 "x": 0.5,
#                 "xanchor": "center",
#                 "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
#             },
#             xaxis={
#                 "title": {"text": "Mês", "font": {"size": 14, "color": "white"}},
#                 "tickvals": list(range(1, 13)),
#                 "ticktext": [
#                     "Jan",
#                     "Fev",
#                     "Mar",
#                     "Abr",
#                     "Mai",
#                     "Jun",
#                     "Jul",
#                     "Ago",
#                     "Set",
#                     "Out",
#                     "Nov",
#                     "Dez",
#                 ],
#                 "tickangle": 0,
#                 "gridcolor": "rgba(80, 80, 80, 0.3)",
#                 "tickangle": -45,
#             },
#             yaxis={
#                 "title": {
#                     "text": "Energia Gerada (kWh)",
#                     "font": {"size": 14, "color": "white"},
#                 },
#                 "gridcolor": "rgba(80, 80, 80, 0.3)",
#                 "zeroline": True,
#                 "zerolinecolor": "rgba(255, 255, 255, 0.2)",
#             },
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="#181818",
#             hovermode="x unified",
#             legend={
#                 "title": "Ano",
#                 "orientation": "h",
#                 "y": -0.2,
#                 "bgcolor": "rgba(0,0,0,0.3)",
#                 "bordercolor": "rgba(255,255,255,0.2)",
#                 "borderwidth": 1,
#             },
#             margin=dict(l=50, r=30, t=80, b=50),
#         )

#         # Adiciona anotações de tendência (opcional)
#         for year in monthly_comparison["Year"].unique():
#             year_data = monthly_comparison[monthly_comparison["Year"] == year]
#             year_trend = year_data["Energy"].iloc[-1] - year_data["Energy"].iloc[0]
#             if abs(year_trend) > (
#                 year_data["Energy"].max() * 0.2
#             ):  # Se a tendência for significativa
#                 trend_color = "green" if year_trend > 0 else "red"
#                 fig.add_annotation(
#                     x=12,
#                     y=year_data["Energy"].iloc[-1],
#                     text=f"{'↑' if year_trend > 0 else '↓'} {abs(year_trend):.0f} kWh",
#                     showarrow=False,
#                     font=dict(color=trend_color, size=12),
#                     xshift=15,
#                 )

#         st.plotly_chart(fig, use_container_width=True)
#     except Exception as e:
#         st.error(f"Erro ao gerar gráfico: {e!s}")


# def plot_grouped_bar_comparison(df):
#     """Exibe um gráfico de barras agrupadas para comparação mensal por ano"""
#     try:
#         # Prepara os dados
#         monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
#         current_year = pd.Timestamp.now().year

#         # Garante que os anos estão ordenados
#         years = sorted(monthly_comparison["Year"].unique())

#         # Mapeamento fixo de cores por ano
#         color_map = {
#             str(year): GREEN_DISCRETE[i % len(GREEN_DISCRETE)]
#             for i, year in enumerate(years)
#         }

#         # Destaque para o ano atual (sobrescreve se existir)
#         if current_year in years:
#             color_map[str(current_year)] = GREEN_DISCRETE[0]

#         # Cria o gráfico com cores mapeadas
#         fig = px.bar(
#             monthly_comparison,
#             x="Month",
#             y="Energy",
#             color="Year",
#             barmode="group",
#             title="Comparativo de Energia por Mês e Ano",
#             labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
#             template="plotly_dark",
#             color_discrete_map=color_map,  # Usa o mapeamento fixo
#             text_auto=".1f",
#         )

#         # Layout (mantido igual)
#         fig.update_layout(
#             title={
#                 "text": (
#                     f"Comparativo de Energia por Mês e Ano ({current_year} destacado)"
#                     if current_year in years
#                     else "Comparativo de Energia por Mês e Ano"
#                 ),
#                 "y": 0.95,
#                 "x": 0.5,
#                 "font": {"size": 18, "color": "white"},
#             },
#             xaxis={
#                 "title": {"text": "Mês", "font": {"size": 14, "color": "white"}},
#                 "tickvals": list(range(1, 13)),
#                 "ticktext": [
#                     "Jan",
#                     "Fev",
#                     "Mar",
#                     "Abr",
#                     "Mai",
#                     "Jun",
#                     "Jul",
#                     "Ago",
#                     "Set",
#                     "Out",
#                     "Nov",
#                     "Dez",
#                 ],
#                 "tickangle": 0,
#             },
#             yaxis={
#                 "title": {
#                     "text": "Energia Gerada (kWh)",
#                     "font": {"size": 14, "color": "white"},
#                 },
#                 "gridcolor": "rgba(80, 80, 80, 0.3)",
#             },
#             plot_bgcolor="rgba(0,0,0,0)",
#             paper_bgcolor="#181818",
#             hovermode="x unified",
#             bargap=0.15,
#             bargroupgap=0.1,
#             legend={
#                 "title": {"text": "Ano", "font": {"color": "white"}},
#                 "bgcolor": "rgba(0,0,0,0.5)",
#             },
#         )

#         # Ajustes finais
#         fig.update_traces(
#             textfont_color="white",
#             textposition="outside",
#             hovertemplate="<b>%{fullData.name}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
#             marker_line_width=0.5,
#             marker_line_color="white",
#         )

#         st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

#     except Exception as e:
#         st.error(f"Erro ao gerar gráfico: {e!s}")


# def create_line_chart(
#     df,
#     *,
#     x: str = "Month",
#     y: str = "Energy",
#     color_col: str = "Year",
#     title: str = "Comparativo Mensal por Ano",
#     xlabel: str = "Mês",
#     ylabel: str = "Energia Gerada (kWh)",
#     color_sequence: list = None,
#     template: str = "plotly_dark",
#     show_legend: bool = True,
#     show_markers: bool = True,
#     **layout_kwargs,
# ):
#     """
#     Cria um gráfico de linhas comparativo com múltiplas melhorias visuais.

#     Args:
#         df: DataFrame com os dados
#         x: Coluna para eixo X (padrão: "Month")
#         y: Coluna para eixo Y (padrão: "Energy")
#         color_col: Coluna para diferenciação por cor (padrão: "Year")
#         title: Título do gráfico
#         xlabel: Label do eixo X
#         ylabel: Label do eixo Y
#         color_sequence: Lista de cores personalizadas
#         template: Template do Plotly
#         show_legend: Mostrar legenda
#         show_markers: Mostrar marcadores nas linhas
#         **layout_kwargs: Argumentos adicionais para update_layout()

#     Returns:
#         plotly.graph_objects.Figure
#     """
#     # Agregação dos dados
#     monthly_comparison = df.groupby([color_col, x])[y].sum().reset_index()

#     # Configuração de cores
#     color_sequence = color_sequence or px.colors.qualitative.Plotly

#     # Criação do gráfico
#     fig = px.line(
#         monthly_comparison,
#         x=x,
#         y=y,
#         color=color_col,
#         title=title,
#         labels={x: xlabel, y: ylabel, color_col: "Ano"},
#         template=template,
#         markers=show_markers,
#         color_discrete_sequence=color_sequence,
#         line_shape="spline",  # Linhas suavizadas
#         hover_data={color_col: True, x: True, y: ":.2f"},
#     )

#     # Customização do layout
#     fig.update_layout(
#         title={
#             "text": title,
#             "y": 0.95,
#             "x": 0.5,
#             "xanchor": "center",
#             "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
#         },
#         xaxis={
#             "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
#             "showgrid": False,
#             "tickmode": "array",
#             "tickvals": list(range(1, 13)),  # Garante todos os meses
#             "ticktext": [
#                 "Jan",
#                 "Fev",
#                 "Mar",
#                 "Abr",
#                 "Mai",
#                 "Jun",
#                 "Jul",
#                 "Ago",
#                 "Set",
#                 "Out",
#                 "Nov",
#                 "Dez",
#             ],
#             "tickangle": 0,
#             "tickfont": {"color": "#ffffff", "size": 12},
#             "automargin": True,
#         },
#         yaxis={
#             "title": {"text": ylabel, "font": {"size": 14, "color": "white"}},
#             "showgrid": True,
#             "gridcolor": "#404040",
#             "zeroline": True,
#             "zerolinewidth": 1,
#             "zerolinecolor": "gray",
#             "tickfont": {"color": "#ffffff", "size": 12},
#             "automargin": True,
#         },
#         legend={
#             "title_text": "Ano",
#             "bgcolor": "rgba(0,0,0,0.5)",
#             "font": {"color": "white"},
#             "orientation": "h",
#             "y": -0.2,  # Posiciona a legenda abaixo
#         },
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="#181818",
#         margin={"l": 60, "r": 40, "t": 80, "b": 60},
#         hovermode="x unified",
#         hoverlabel={"bgcolor": "#2a2a2a", "font_size": 12, "font_family": "Arial"},
#         **layout_kwargs,
#     )

#     # Melhorias nas linhas
#     fig.update_traces(
#         line={"width": 2.5},
#         marker={"size": 8, "line": {"width": 1, "color": "DarkSlateGrey"}},
#         hovertemplate=(
#             f"<b>Ano:</b> %{{customdata[0]}}<br>"
#             f"<b>{xlabel}:</b> %{{customdata[1]}}<br>"
#             f"<b>{ylabel}:</b> %{{customdata[2]:,.2f}}<extra></extra>"
#         ),
#     )

#     return fig


# def plot_comparative_months_by_year_line(df):
#     """Exibe um gráfico de linha comparativo dos meses por ano"""
#     try:
#         monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

#         fig = create_line_chart(  # Corrigido: chamando create_line_chart em vez de si mesma
#             monthly_comparison,
#             title="Produção Mensal Comparativa",
#             color_sequence=px.colors.qualitative.Vivid,
#             show_markers=True,
#             height=500,
#         )

#         st.plotly_chart(fig, use_container_width=True)
#     except Exception as e:
#         st.error(f"Ocorreu um erro ao exibir o gráfico: {e}")


# def create_area_chart(
#     df,
#     *,
#     x: str = "Month",
#     y: str = "Energy",
#     color_col: str = "Year",
#     title: str = "Comparativo Mensal por Ano",
#     xlabel: str = "Mês",
#     ylabel: str = "Energia Gerada (kWh)",
#     color_sequence: list = None,
#     template: str = "plotly_dark",
#     show_legend: bool = True,
#     stacked: bool = True,  # Novo: controle booleano para empilhamento
#     **layout_kwargs,
# ):
#     """
#     Cria um gráfico de área empilhada com correção do parâmetro stackgroup.
#     Args:
#     df: DataFrame com os dados
#     stacked: Se True, áreas serão empilhadas (default)
#     ... (outros parâmetros permanecem iguais)
#     """
#     # Configuração de cores
#     color_sequence = color_sequence or px.colors.qualitative.Plotly
#     # Criação do gráfico base
#     fig = px.area(
#         df,
#         x=x,
#         y=y,
#         color=color_col,
#         title=title,
#         labels={x: xlabel, y: ylabel, color_col: "Ano"},
#         template=template,
#         color_discrete_sequence=color_sequence,
#         hover_data={color_col: True, x: True, y: ":.2f"},
#         line_shape="spline",
#     )
#     # Aplica empilhamento se necessário
#     if stacked:
#         fig.update_traces(stackgroup="stack")  # Nome arbitrário para o grupo

#     # Configuração do layout com título centralizado
#     fig.update_layout(
#         title={
#             "text": title,
#             "y": 0.95,
#             "x": 0.5,  # Garante que o título está centralizado horizontalmente
#             "xanchor": "center",  # Ancora o título no centro
#             "yanchor": "top",  # Ancora o título no topo
#             "font": {"size": 18, "color": "white", "family": "Arial, sans-serif"},
#         },
#         xaxis={
#             "title": {"text": xlabel, "font": {"size": 14, "color": "white"}},
#             "showgrid": False,
#             "tickmode": "array",
#             "tickvals": list(range(1, 13)),
#             "ticktext": [
#                 "Jan",
#                 "Fev",
#                 "Mar",
#                 "Abr",
#                 "Mai",
#                 "Jun",
#                 "Jul",
#                 "Ago",
#                 "Set",
#                 "Out",
#                 "Nov",
#                 "Dez",
#             ],
#             "tickangle": 0,
#             "tickfont": {"color": "#ffffff", "size": 12},
#             "automargin": True,
#         },
#         # ... (restante do layout permanece igual)
#         **layout_kwargs,  # Permite sobreescrever configurações com kwargs
#     )
#     return fig


# def plot_area_stack_by_year(df):
#     """Exibe um gráfico de área empilhada comparativo dos meses por ano"""
#     try:
#         monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()

#         fig = create_area_chart(
#             monthly_comparison,
#             title="Produção Mensal Comparativa (Área Empilhada)",
#             color_sequence=px.colors.qualitative.Vivid,
#             stackgroup="year",
#         )

#         # Aplica as customizações
#         fig.update_traces(
#             opacity=0.5,  # Transparência aqui
#             line=dict(width=1),
#             hovertemplate="<b>Ano %{color}:</b> %{y:,.2f} kWh<br>Mês: %{x}<extra></extra>",
#         )

#         st.plotly_chart(fig, use_container_width=True)
#     except Exception as e:
#         st.error(f"Ocorreu um erro ao exibir o gráfico: {e}")


# def plot_scatter_by_year(df):
#     """Exibe um gráfico de dispersão comparativo dos meses por ano"""
#     monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
#     fig = px.scatter(
#         monthly_comparison,
#         x="Month",
#         y="Energy",
#         color="Year",
#         title="Comparativo de Energia Gerada por Mês e Ano (Dispersão)",
#         labels={"Month": "Mês", "Energy": "Energia Gerada (kWh)", "Year": "Ano"},
#         template="plotly_dark",
#     )
#     fig.update_layout(
#         title=dict(
#             text="Comparativo de Energia Gerada por Mês e Ano",
#             x=0.5,
#             font=dict(size=16, color="white"),
#         ),
#         xaxis=dict(
#             title="Mês",
#             showgrid=False,
#             tickmode="linear",
#             ticks="outside",
#             tickwidth=2,
#             tickangle=45,
#             tickfont=dict(color="#ffffff"),
#         ),
#         yaxis=dict(
#             title="Energia Gerada (kWh)",
#             showgrid=True,
#             zeroline=True,
#             zerolinewidth=1,
#             zerolinecolor="gray",
#             tickfont=dict(color="#ffffff"),
#         ),
#         plot_bgcolor="#181818",
#         paper_bgcolor="#181818",
#         margin=dict(l=40, r=40, t=40, b=40),
#     )
#     st.plotly_chart(fig)


# def plot_candlestick_by_month(df):
#     """Exibe um gráfico Candlestick comparativo dos meses por ano"""
#     monthly_comparison = df.groupby(["Year", "Month"])["Energy"].sum().reset_index()
#     fig_data = []
#     for year in monthly_comparison["Year"].unique():
#         year_data = monthly_comparison[monthly_comparison["Year"] == year]
#         fig_data.append(
#             go.Candlestick(
#                 x=year_data["Month"],
#                 open=[year_data["Energy"].iloc[0]]
#                 * len(
#                     year_data
#                 ),  # Energia do primeiro mês do ano repetida para todos os meses
#                 high=[year_data["Energy"].max()]
#                 * len(year_data),  # Energia máxima repetida para todos os meses
#                 low=[year_data["Energy"].min()]
#                 * len(year_data),  # Energia mínima repetida para todos os meses
#                 close=[year_data["Energy"].iloc[-1]]
#                 * len(year_data),  # Energia do último mês repetida para todos os meses
#                 name=str(year),
#             )
#         )

#     fig = go.Figure(fig_data)
#     fig.update_layout(
#         title=dict(
#             text="Comparativo de Energia Gerada por Mês e Ano (Candlestick)",
#             x=0.5,
#             font=dict(size=16, color="white"),
#         ),
#         xaxis=dict(
#             title="Mês",
#             tickmode="linear",
#             tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
#             ticktext=[
#                 "Jan",
#                 "Feb",
#                 "Mar",
#                 "Apr",
#                 "May",
#                 "Jun",
#                 "Jul",
#                 "Aug",
#                 "Sep",
#                 "Oct",
#                 "Nov",
#                 "Dec",
#             ],
#             showgrid=False,
#             ticks="outside",
#             tickwidth=2,
#             tickangle=45,
#             tickfont=dict(color="#ffffff"),
#         ),
#         yaxis=dict(
#             title="Energia Gerada (kWh)",
#             showgrid=True,
#             zeroline=True,
#             zerolinewidth=1,
#             zerolinecolor="gray",
#             tickfont=dict(color="#ffffff"),
#         ),
#         plot_bgcolor="#181818",
#         paper_bgcolor="#181818",
#         margin=dict(l=40, r=40, t=40, b=40),
#     )
#     st.plotly_chart(fig)


# def select_optimal_colors(n_colors):
#     """Seleciona as cores com melhor contraste visual"""
#     priority_order = [0, 1, 2, 3, 4, 6, 5, 7, 8, 9]  # Ordem de prioridade de cores
#     return [GREEN_DISCRETE[i] for i in priority_order[:n_colors]]

import plotly.express as px


def temporal_value(stocks_data_frames, tab):
    analysis = [
        "iBovespa teve uma alta no período de cerca de 20 mil pontos.",
        "Quanto ao PagSeguro, percebe-se que a ação está lateralizada desde 2023.",
        "Bradesco também encontra-se lateralizado, ou seja, no mesmo patamar.",
        "A Cyrela teve uma grande alta de quase 80% desde janeiro de 2023.",
        "Ambev também praticamente lateralizada, dentro de 10% de variação.",
        "A Gol sofreu uma quebra e está em abaixo 1/12 do seu valor máximo no período.",
    ]
    # fig = px.line(title=titles[i])
    fig = px.line(title="Histórico de Valor das Ações")
    for i, col in enumerate(stocks_data_frames.columns[1:]):
        fig.add_scatter(
            x=stocks_data_frames["Date"], y=stocks_data_frames[col], name=col
        )
    tab.plotly_chart(fig)
    for i in range(6):
        tab.text(analysis[i])

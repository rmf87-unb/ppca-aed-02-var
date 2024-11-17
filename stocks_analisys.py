import pandas as pd
import yfinance as yf
import streamlit as st


from assets_evo import assets_evo
from temporal_return import temporal_return
from temporal_value import temporal_value
from markowitz import markowitz
from value_at_risk import value_at_risk


st.title("Análise de Portfólio de Ações")

st.markdown(
    """
    Partimos do iBovespa a do seguinte portfólio de ações, sobre as quais se analisa, inicialmente, a evolução de preço e de retorno de janeiro de 2023 a outubro de 2024:
    - PagSeguro Digital Ltd.
    - Banco Bradesco S.A.
    - Cyrela Brazil Realty S.A. Empreendimentos e Participações
    - Ambev S.A
    - Gol Linhas Aéreas Inteligentes S.A.
    
    Em seguida, por uma simulação de Monte Carlo, estimou-se a fronteira eficiente de Markowitz. Nesta simulação, escolheu-se a carteira com melhor índice de Sharpe (razão retorno/volatilidade).

    Para a melhor carteira, seguiu-se a apresentação da evolução do patrimônio para um investimento inicial de R$ 35.000,00.

    Por fim, foi feita outra simulação de Monte Carlo para se determinar o Value at Risk desta posição.
    """
)

titles = [
    "iBovespa",
    "PagSeguro Digital Ltd.",
    "Banco Bradesco S.A.",
    "Cyrela Brazil Realty S.A. Empreendimentos e Participações",
    "Ambev S.A.",
    "Gol Linhas Aéreas Inteligentes S.A. ",
]
tickers = ["^BVSP", "PAGS", "BBDC4.SA", "CYRE3.SA", "ABEV3.SA", "GOLL4.SA"]
stocks_data_frames = pd.DataFrame()
start = "2023-01-01"
end = "2024-10-31"


@st.cache_data(persist=True)
def download_tick(stock, start, end):
    return yf.download(stock, start, end)["Close"]


def load_stocks(stocks, stocks_data_frames, start, end):
    for stock in stocks:
        stocks_data_frames[stock] = download_tick(stock, start, end)
    stocks_data_frames.index = stocks_data_frames.index.strftime("%Y-%m-%d")
    stocks_data_frames.reset_index(inplace=True)
    stocks_data_frames.dropna(inplace=True)


load_stocks(tickers, stocks_data_frames, start, end)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Análise Temporal Valor",
        "Análise Temporal Retorno",
        "Fronteira de Markowitz",
        "Evolução e Retorno",
        "Value at Risk",
    ]
)

temporal_value(stocks_data_frames, tab1)
temporal_return(stocks_data_frames, tab2)
best_position, max_sharpe_vol, max_sharpe_ret = markowitz(
    stocks_data_frames, tab3, 50000, 100
)
assets_df = assets_evo(stocks_data_frames, best_position, 35000, tab4)
value_at_risk(assets_df, 0.9, max_sharpe_vol, max_sharpe_ret, tab5)

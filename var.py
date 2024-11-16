import pandas as pd
import yfinance as yf
import streamlit as st


from temporal_return import temporal_return
from temporal_value import temporal_value


st.title("Análise de Portfólio de Ações")

st.markdown(
    """
    Partimos do iBovespa a do seguinte portfólio de ações, sobre as quais se analisa, inicialmente, a evolução de preço e de retorno de janeiro de 2023 a outubro de 2024:
    - PagSeguro Digital Ltd.
    - Banco Bradesco S.A.
    - Vale S.A.
    - Ambev S.A
    - Gol Linhas Aéreas Inteligentes S.A.
    
    Em seguida, por uma simulação de Monte Carlo, estimou-se a fronteira eficiente de Markowitz.
    """
)

titles = [
    "iBovespa",
    "PagSeguro Digital Ltd.",
    "Banco Bradesco S.A.",
    "Vale S.A.",
    "Ambev S.A.",
    "Gol Linhas Aéreas Inteligentes S.A. ",
]
tickers = ["^BVSP", "PAGS", "BBDC4.SA", "VALE3.SA", "ABEV3.SA", "GOLL4.SA"]
stocks_data_frames = pd.DataFrame()
start = "2023-01-01"
end = "2024-10-31"


@st.cache_data
def download_tick(stock, start, end):
    return yf.download(stock, start, end)["Close"]


def load_stocks(stocks, stocks_data_frames, start, end):
    for stock in stocks:
        stocks_data_frames[stock] = download_tick(stock, start, end)
    stocks_data_frames.index = stocks_data_frames.index.strftime("%Y-%m-%d")
    stocks_data_frames.reset_index(inplace=True)


load_stocks(tickers, stocks_data_frames, start, end)

tab1, tab2, tab3 = st.tabs(
    ["Análise Temporal Valor", "Análise Temporal Retorno", "Fronteira de Markowitz"]
)

temporal_value(stocks_data_frames, tab1)
temporal_return(stocks_data_frames, tab2)

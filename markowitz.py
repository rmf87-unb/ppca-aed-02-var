import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
from stqdm import stqdm
import matplotlib.pyplot as plt
import locale

locale.setlocale(locale.LC_ALL, "pt_BR")


@st.cache_data
def port_ret_dfs(stocks_data_frames):
    # portfolio
    port_df = stocks_data_frames.filter(stocks_data_frames.columns[2:])
    tempo_df = stocks_data_frames.filter(["Date"], axis=1)
    tempo_df = tempo_df.apply(
        lambda x: pd.to_datetime(x, errors="coerce", format="%Y-%m-%d")
    )
    port_df = pd.concat([tempo_df, port_df], axis=1)

    # return
    ret_df = stocks_data_frames.filter(stocks_data_frames.columns[2:], axis=1)
    ret_df = np.log(ret_df / ret_df.shift(1))
    return port_df, ret_df


def monte_carlo_for_sharpe(num_runs, port_size, ret_df, bar):
    all_weights = np.zeros((num_runs, port_size))
    ret_arr = np.zeros(num_runs)
    vol_arr = np.zeros(num_runs)
    sharpe_arr = np.zeros(num_runs)
    for x in range(num_runs):
        weights = np.array(np.random.random(port_size))
        weights = weights / np.sum(weights)
        all_weights[x, :] = weights
        ret_arr[x] = np.sum((ret_df.mean() * weights))
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(ret_df.cov(), weights)))
        sharpe_arr[x] = ret_arr[x] / vol_arr[x]
        bar.update(1)

    return sharpe_arr, all_weights, ret_arr, vol_arr


def markowitz(
    stocks_data_frames,
    tab,
    num_runs,
):
    port_df, ret_df = port_ret_dfs(stocks_data_frames)
    bar = stqdm(total=num_runs)
    sharpe, weights, ret_arr, vol_arr = monte_carlo_for_sharpe(
        num_runs, len(port_df.columns[1:]), ret_df, bar
    )

    best_position = weights[sharpe.argmax(), :]
    weights_df = pd.DataFrame(columns=stocks_data_frames.columns[2:])
    weights_df.loc["best weights"] = best_position

    tab.markdown(
        f"""
        Com {num_runs} simulações, obteve-se o maior valor de Sharpe, razão entre retorno / volatilidade de: {sharpe.max():.5}.
       
        Os pesos para cada ação no melhor valor de Sharpe foram:
        """
    )
    tab.dataframe(weights_df)

    tab.markdown(
        f"""
        A fronteira de Markowitz tem o seguinte formato:
        """
    )

    fig = plt.figure(figsize=(12, 8))
    plt.scatter(vol_arr, ret_arr, c=sharpe)
    plt.colorbar(label="Sharpe Ratio")
    plt.xlabel("Volatilidade")
    plt.ylabel("Retorno")
    plt.scatter(vol_arr[sharpe.argmax()], ret_arr[sharpe.argmax()], c="red", s=200)
    tab.pyplot(fig)

    return best_position

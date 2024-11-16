import pandas as pd
import numpy as np
import streamlit as st
from stqdm import stqdm
import matplotlib.pyplot as plt
import locale
from scipy import optimize

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


def monte_carlo_for_sharpe(num_runs, port_size, ret_df):
    all_weights = np.zeros((num_runs, port_size))
    ret_arr = np.zeros(num_runs)
    vol_arr = np.zeros(num_runs)
    sharpe_arr = np.zeros(num_runs)
    bar = stqdm(total=num_runs)
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

    sharpe, weights, ret_arr, vol_arr = monte_carlo_for_sharpe(
        num_runs, len(port_df.columns[1:]), ret_df
    )

    best_position = weights[sharpe.argmax(), :]

    # frontier

    def get_ret_vol_sharpe(weights):
        weights = np.array(weights)
        ret = np.sum(ret_df.mean() * weights)
        vol = np.sqrt(np.dot(weights.T, np.dot(ret_df.cov(), weights)))
        sharpe = ret / vol
        return np.array([ret, vol, sharpe])

    def check_sum(weights):
        return np.sum(weights) - 1

    def minimize_volatility(weights):
        return get_ret_vol_sharpe(weights)[1]

    frontier_y = np.linspace(0.000, 0.0010, 100)
    frontier_x = []

    cons = {"type": "eq", "fun": check_sum}
    bounds = ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
    init_guess = ((0.2), (0.2), (0.2), (0.2), (0.2))
    bar2 = stqdm(total=len(frontier_y))
    for possible_return in frontier_y:
        cons = (
            {"type": "eq", "fun": check_sum},
            {"type": "eq", "fun": lambda w: get_ret_vol_sharpe(w)[0] - possible_return},
        )
        result = optimize.minimize(
            minimize_volatility,
            init_guess,
            method="SLSQP",
            bounds=bounds,
            constraints=cons,
        )
        frontier_x.append(result["fun"])
        bar2.update(1)

    # report

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
    plt.plot(frontier_x, frontier_y, "b--", linewidth=3)
    tab.pyplot(fig)

    return best_position

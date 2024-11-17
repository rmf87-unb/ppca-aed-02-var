import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def var(series, confidence_level):
    series = np.array(series)
    z_score = -norm.ppf(confidence_level)
    stdev = np.std(series)
    var = series.mean() + z_score * stdev
    return var


def value_at_risk(assets_df, confidence_level, max_sharpe_vol, max_sharpe_ret, tab):
    np.random.seed(10)

    # var return
    returns = assets_df.filter(["return"], axis=1)
    returns = np.random.normal(max_sharpe_ret * 100, max_sharpe_vol * 100, 100000)
    var_90 = var(returns, confidence_level)
    tab.markdown(
        f"""
        Distribuição do Retorno diário para um VaR em 90% de confiança:
        """
    )
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.hist(returns, bins=50, density=True, alpha=0.8)
    ax.axvline(
        x=var_90, color="r", linestyle="--", label=f"VaR de {confidence_level*100:.0f}%"
    )
    ax.legend()
    ax.set_xlabel("Retornos")
    ax.set_ylabel("Densidade")
    ax.set_title("Distribuição dos Retornos Diários. VaR em 90% de confiança.")
    tab.pyplot(fig)

    # var investment value
    value = assets_df.filter(["Total"], axis=1)
    mean = value["Total"].mean()
    std = value["Total"].std()
    values = np.random.normal(mean, std, 10000)
    var_90 = var(values, confidence_level)
    tab.markdown(
        f"""
        Distribuição do Valor Total do Portfólio com VaR em 90% de confiança:
        """
    )

    fig2, ax2 = plt.subplots(figsize=(12, 8))
    ax2.hist(values, bins=50, density=True, alpha=0.8)
    ax2.axvline(
        x=var_90,
        color="r",
        linestyle="--",
        label=f"VaR de {confidence_level*100:.0f}%",
    )
    ax2.legend()
    ax2.set_xlabel("Valor do Portfólio")
    ax2.set_ylabel("Densidade")
    ax2.set_title("Distribuição do Valor do Portfólio. VaR em 90% de confiança.")
    tab.pyplot(fig2)

    loss_rate = norm.cdf((35000 - mean) / std)
    tab.text(
        f"Este portfólio é enviesado pelo desempenho positivo de algumas de suas ações. Há {(1- loss_rate)*100:.2f}% de probabilidade de um retorno positivo nos R$ 35.000,00 investidos."
    )

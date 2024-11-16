import pandas as pd
import plotly.express as px
import numpy as np


def temporal_retorno(stocks_data_frames, tab):

    retorno_df = pd.DataFrame()
    tempo_df = stocks_data_frames.filter(["Date"], axis=1)
    tempo_df = tempo_df.apply(
        lambda x: pd.to_datetime(x, errors="coerce", format="%Y-%m-%d")
    )
    partial_df = stocks_data_frames.filter(stocks_data_frames.columns[1:], axis=1)
    retorno_df = np.log(partial_df / partial_df.shift(1))
    retorno_df = pd.concat([tempo_df, retorno_df], axis=1)

    fig = px.scatter(
        retorno_df,
        x=retorno_df["Date"],
        y=stocks_data_frames.columns[1:],
        trendline="ols",
        trendline_color_override="grey",
        title="Histórico de Retorno (t=1) das Ações",
    )

    tab.plotly_chart(fig)

    # value diff
    stocks_data_frames_on = stocks_data_frames.copy()
    stocks_data_frames_on.dropna(inplace=True)
    dif_df = pd.concat(
        [stocks_data_frames_on.head(1), stocks_data_frames_on.tail(1)],
        ignore_index=True,
    )
    dif_df.drop("Date", axis=1, inplace=True)
    dif_df.rename(index={0: "first", 1: "last"}, inplace=True)
    first = dif_df.loc["first"]
    last = dif_df.loc["last"]
    dif_df.loc["change"] = (last - first) / first
    dif_df.drop(["first", "last"], axis=0, inplace=True)

    # aggregate
    # agg_df = retorno_df.agg(["mean", "std", "max", "min"])
    agg_df = retorno_df.agg(["std"])
    agg_df.drop("Date", axis=1, inplace=True)

    # summary
    summary_df = pd.concat([dif_df, agg_df])
    summary_df.rename(
        index={
            "first": "initial val.",
            "last": "last val.",
            "change": "val. Δ%",
            "mean": "mean ret.",
            "std": "std ret.",
            "max": "max ret.",
            "min": "min ret.",
        },
        inplace=True,
    )

    tab.markdown("""O retorno foi calculado como:""")
    tab.latex(r"""E[R_i] = \log\left(\frac{P_t}{P_{t-1}}\right)""")
    tab.markdown(
        """
        Pode-se observar que os gráficos de dispersão dos retornos para o período de 1 dia apresentam linhas tendências (mínimos quadrados ordinários) muito próximas de zero no período observado.

        Apesar de haver diferenças significativas nos desvios padrão, não é possível associá-los ao retorno no período. 
    
        O que o std parece evidenciar é que as mudanças patamar nos preços parecem ocorrer em outliers de retorno, seja para mais ou para menos, ou seja, em dias específicos.
        """
    )

    tab.dataframe(summary_df)

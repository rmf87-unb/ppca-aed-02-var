import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

from helpers import diff_df


@st.cache_data
def evo(stocks_data_frames, best_position, invested_value):
    # values
    tempo_df = stocks_data_frames.filter(["Date"], axis=1)
    tempo_df = tempo_df.apply(
        lambda x: pd.to_datetime(x, errors="coerce", format="%Y-%m-%d")
    )
    values_df = stocks_data_frames.filter(stocks_data_frames.columns[2:], axis=1)

    # assets
    investment = invested_value * best_position
    shares = investment / values_df.iloc[0]
    assets_df = shares * values_df
    assets_df["Total"] = assets_df[assets_df.columns].sum(axis=1)
    assets_df = pd.concat([tempo_df, assets_df], axis=1)

    return assets_df


def assets_evo(stocks_data_frames, best_position, invested_value, tab):
    assets_df = evo(stocks_data_frames, best_position, invested_value)
    fig = px.line(title="Evolução do Patrimônio")
    for col in assets_df.columns[1:]:
        fig.add_scatter(x=assets_df["Date"], y=assets_df[col], name=col)
    dif_df = diff_df(assets_df)
    dif_df["^BVSP"] = diff_df(stocks_data_frames).filter(["^BVSP"], axis=1)
    dif_df.rename(
        index={
            "change": "val. Δ%",
        },
        inplace=True,
    )

    tab.markdown(
        f"""
        Evolução do patrimônio para a carteira de melhor Sharp:
        """
    )
    tab.plotly_chart(fig)
    tab.markdown(
        f"""
        Ao final do período, a evolução do patrimônio pode ser comparada ao o índice Bovespa:
        """
    )
    tab.dataframe(dif_df)

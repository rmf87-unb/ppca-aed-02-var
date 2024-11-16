import pandas as pd
import streamlit as st


def diff_df(df):
    # value diff
    diff_df = df.copy()
    dif_df = pd.concat(
        [diff_df.head(1), diff_df.tail(1)],
        ignore_index=True,
    )
    dif_df.drop("Date", axis=1, inplace=True)
    dif_df.rename(index={0: "first", 1: "last"}, inplace=True)
    first = dif_df.loc["first"]
    last = dif_df.loc["last"]
    dif_df.loc["change"] = (last - first) / first
    dif_df.drop(["first", "last"], axis=0, inplace=True)

    return dif_df

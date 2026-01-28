import pandas as pd
import streamlit as st

SHEET_ID = "1ZK56ftUfmoisT78rDt8RakdsrlKveIvyl1azRrkvwfU"
SHEET_NAME = "TWITCH_STAT"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
)

@st.cache_data(ttl=300)
def load_twitch_data():
    df = pd.read_csv(CSV_URL)

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    df = df.dropna(subset=["date"])

    df["raid"] = (
        df["raid"]
        .astype(str)
        .str.lower()
        .isin(["true", "yes", "1", "oui"])
    )

    return df.sort_values("date")

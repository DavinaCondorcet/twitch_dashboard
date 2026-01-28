import streamlit as st
import pandas as pd

from twitch.data_loader import load_twitch_data
from twitch.plots import (
    evolution_viewers,
    tendance_viewers,
    viewers_par_jour,
    impact_raids
)

st.set_page_config(page_title="Twitch Analytics", layout="wide")
st.title("📺 Dashboard Twitch")

df = load_twitch_data()

# ======================
# SIDEBAR – FILTRES
# ======================
st.sidebar.header("🎛️ Filtres")

periode = st.sidebar.date_input(
    "Période",
    value=(df["date"].min(), df["date"].max())
)

if not isinstance(periode, tuple) or len(periode) != 2:
    st.stop()

date_debut, date_fin = periode

raid_only = st.sidebar.checkbox("Streams avec raid uniquement")

# ======================
# FILTRAGE
# ======================
filtre = df[
    (df["date"] >= pd.to_datetime(date_debut)) &
    (df["date"] <= pd.to_datetime(date_fin))
]

if raid_only:
    filtre = filtre[filtre["raid"]]

# ======================
# KPI
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("📺 Streams", len(filtre))
col2.metric("👥 Avg viewers", round(filtre["avg"].mean(), 1))
col3.metric("🚀 Record", int(filtre["max"].max()))
col4.metric("⚡ % raids", f"{filtre['raid'].mean() * 100:.1f}%")

# ======================
# GRAPHS
# ======================
st.plotly_chart(evolution_viewers(filtre), use_container_width=True)
st.plotly_chart(tendance_viewers(filtre), use_container_width=True)
st.plotly_chart(viewers_par_jour(filtre), use_container_width=True)

fig_raid, impact = impact_raids(filtre)
st.plotly_chart(fig_raid, use_container_width=True)

# ======================
# INSIGHT RAID
# ======================
if True in impact["raid"].values and False in impact["raid"].values:
    avg_raid = impact.loc[impact["raid"], "mean"].values[0]
    avg_no_raid = impact.loc[~impact["raid"], "mean"].values[0]

    uplift = ((avg_raid - avg_no_raid) / avg_no_raid) * 100
    st.metric("📈 Gain moyen grâce aux raids", f"{uplift:.1f} %")

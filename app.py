import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Twitch Stats Dashboard",
    layout="wide"
)

SHEET_ID = "1ZK56ftUfmoisT78rDt8RakdsrlKveIvyl1azRrkvwfU"
SHEET_NAME = "TWITCH_STAT"

CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# ======================
# DATA LOADING
# ======================
@st.cache_data(ttl=300)  # auto-refresh every 5 min
def load_data():
    df = pd.read_csv(CSV_URL)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    df["raid"] = df["raid"].astype(str).str.lower().isin(["true", "yes", "1"])
    return df.sort_values("date")

df = load_data()

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("Filters")

start_date, end_date = st.sidebar.date_input(
    "Date range",
    [df["date"].min(), df["date"].max()]
)

raid_only = st.sidebar.checkbox("Only raided streams")

filtered = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

if raid_only:
    filtered = filtered[filtered["raid"]]

# ======================
# KPIs
# ======================
st.title("🎮 Twitch Streaming Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Streams", len(filtered))
col2.metric("Avg Viewers", round(filtered["avg"].mean(), 1))
col3.metric("Max Viewers Ever", int(filtered["max"].max()))
col4.metric("Raid Rate", f"{filtered['raid'].mean() * 100:.1f}%")

# ======================
# VIEWERS OVER TIME
# ======================
fig_time = px.line(
    filtered,
    x="date",
    y="avg_viewers",
    title="Average Viewers Over Time",
    markers=True
)

st.plotly_chart(fig_time, use_container_width=True)

# ======================
# ROLLING AVERAGES
# ======================
rolling = filtered.copy()
rolling["7d_avg"] = rolling["avg"].rolling(7).mean()
rolling["30d_avg"] = rolling["avg"].rolling(30).mean()

fig_roll = px.line(
    rolling,
    x="date",
    y=["avg", "7d_avg", "30d_avg"],
    title="Growth & Trends"
)

st.plotly_chart(fig_roll, use_container_width=True)

# ======================
# DAY OF WEEK ANALYSIS
# ======================
filtered["weekday"] = filtered["date"].dt.day_name()

dow = (
    filtered.groupby("weekday")["avg_viewers"]
    .mean()
    .reindex([
        "Lundi", "Mardi", "Mercredi",
        "Jeudi", "Vendredi", "Samedi", "Dimanche"
    ])
)

fig_dow = px.bar(
    dow,
    title="Average Viewers by Day of Week",
    labels={"value": "Avg Viewers", "weekday": "Day"}
)

st.plotly_chart(fig_dow, use_container_width=True)

# ======================
# RAID IMPACT
# ======================
fig_raid = px.box(
    filtered,
    x="raid",
    y="avg",
    title="Impact of Raids on Viewership",
    labels={"raided": "Raid"}
)

st.plotly_chart(fig_raid, use_container_width=True)

# ======================
# STREAKS
# ======================
filtered = filtered.sort_values("date")
filtered["gap"] = filtered["date"].diff().dt.days
filtered["new_streak"] = filtered["gap"] > 1
filtered["streak_id"] = filtered["new_streak"].cumsum()

streaks = (
    filtered.groupby("streak_id")
    .size()
    .max()
)

st.success(f"🔥 Longest streaming streak: **{streaks} days**")

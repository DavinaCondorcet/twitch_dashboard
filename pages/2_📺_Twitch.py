import streamlit as st
from twitch.database import init_db
from twitch.updater import update_streams
from twitch.plots import viewers_over_time

st.title("📺 Twitch Analytics")

init_db()

with st.spinner("Sync Twitch data…"):
    update_streams()

st.plotly_chart(viewers_over_time(), use_container_width=True)

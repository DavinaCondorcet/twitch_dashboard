import streamlit as st
from ..valorant.database import init_db
from ..valorant.updater import update_matches, update_rank
from ..valorant.plots import kda_over_time, winrate_by_agent

RIOT_ID = "YukiBloo"
TAG = "EUW"

st.title("🎮 Valorant Tracker")

init_db()

with st.spinner("Sync Valorant data…"):
    update_matches(RIOT_ID, TAG)
    update_rank(RIOT_ID, TAG)

st.plotly_chart(kda_over_time(), use_container_width=True)
st.plotly_chart(winrate_by_agent(), use_container_width=True)

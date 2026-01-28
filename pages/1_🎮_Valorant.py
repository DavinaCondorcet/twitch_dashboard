import sys
from pathlib import Path

# ajoute le dossier racine au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# maintenant les imports absolus depuis la racine fonctionnent
from valorant.database import init_db
from valorant.updater import update_matches, update_rank

# test
init_db()
update_matches()
update_rank()

RIOT_ID = "YukiBloo"
TAG = "EUW"

st.title("🎮 Valorant Tracker")

with st.spinner("Sync Valorant data…"):
    update_matches(RIOT_ID, TAG)
    update_rank(RIOT_ID, TAG)

st.plotly_chart(kda_over_time(), use_container_width=True)
st.plotly_chart(winrate_by_agent(), use_container_width=True)

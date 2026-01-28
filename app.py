import streamlit as st

# ======================
# CONFIG GLOBALE
# ======================
st.set_page_config(
    page_title="Gaming Analytics Dashboard",
    layout="wide"
)

# ======================
# PAGE D’ACCUEIL
# ======================
st.title("🎯 Gaming Analytics Dashboard")

st.markdown(
    """
Bienvenue 👋  

Ce dashboard regroupe **toutes tes données de performance gaming** :

### 🎮 Valorant
- Suivi du KDA, HS%, ACS
- Winrate par agent et par map
- Évolution du rank et des RR
- Analyse des sessions & détection du tilt

### 📺 Twitch
- Évolution de l’audience
- Impact des raids
- Analyse par jour de la semaine
- Tendances de croissance

➡️ Utilise le **menu à gauche** pour naviguer entre les sections.
"""
)

# ======================
# SIDEBAR INFO
# ======================
st.sidebar.title("ℹ️ À propos")
st.sidebar.info(
    """
📊 Données mises à jour automatiquement  
🚀 Dashboard personnel  
⚙️ Streamlit Cloud compatible
"""
)

st.sidebar.markdown("---")
st.sidebar.markdown("🛠️ **Tech stack**")
st.sidebar.markdown("- Streamlit")
st.sidebar.markdown("- Plotly")
st.sidebar.markdown("- Pandas")
st.sidebar.markdown("- SQLite / Google Sheets")


import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIGURATION
# ======================
st.set_page_config(
    page_title="Dashboard Twitch",
    layout="wide"
)

SHEET_ID = "1ZK56ftUfmoisT78rDt8RakdsrlKveIvyl1azRrkvwfU"
SHEET_NAME = "TWITCH_STAT"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
)

# ======================
# CHARGEMENT DES DONNÉES
# ======================
@st.cache_data(ttl=300)
def charger_donnees():
    df = pd.read_csv(CSV_URL)

    # Conversion des dates JJ/MM/AAAA
    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    # Suppression des jours sans stream
    df = df.dropna(subset=["date"])

    # Conversion raid → booléen
    df["raid"] = (
        df["raid"]
        .astype(str)
        .str.lower()
        .isin(["true", "yes", "1", "oui"])
    )

    return df.sort_values("date")

df = charger_donnees()

# ======================
# BARRE LATÉRALE – FILTRES
# ======================
st.sidebar.header("🎛️ Filtres")

periode = st.sidebar.date_input(
    "Période",
    value=(df["date"].min(), df["date"].max())
)

# Sécurité : attendre que les deux dates soient sélectionnées
if not isinstance(periode, tuple) or len(periode) != 2:
    st.info("📅 Sélectionne une date de début et une date de fin")
    st.stop()

date_debut, date_fin = periode

streams_raids_uniquement = st.sidebar.checkbox(
    "Afficher uniquement les streams avec raid"
)

# ======================
# FILTRAGE DES DONNÉES
# ======================
filtre = df[
    (df["date"] >= pd.to_datetime(date_debut)) &
    (df["date"] <= pd.to_datetime(date_fin))
].copy()

if streams_raids_uniquement:
    filtre = filtre[filtre["raid"]]
# ======================
# TITRE
# ======================
st.title("🎮 Dashboard Twitch")

# ======================
# KPI
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("📺 Nombre de streams", len(filtre))
col2.metric("👥 Moyenne viewers", round(filtre["avg"].mean(), 1))
col3.metric("🚀 Record viewers", int(filtre["max"].max()))
col4.metric("⚡ % streams avec raid", f"{filtre['raid'].mean() * 100:.1f}%")

# ======================
# ÉVOLUTION DES VIEWERS
# ======================
fig_evolution = px.line(
    filtre,
    x="date",
    y="avg",
    markers=True,
    title="📈 Évolution de la moyenne de viewers"
)

st.plotly_chart(fig_evolution, use_container_width=True)

# ======================
# MOYENNES GLISSANTES
# ======================
filtre["moyenne_7j"] = filtre["avg"].rolling(7).mean()
filtre["moyenne_30j"] = filtre["avg"].rolling(30).mean()

fig_tendance = px.line(
    filtre,
    x="date",
    y=["avg", "moyenne_7j", "moyenne_30j"],
    title="📊 Tendance & croissance",
    labels={"value": "Viewers", "variable": "Type"}
)

st.plotly_chart(fig_tendance, use_container_width=True)

# ======================
# ANALYSE PAR JOUR
# ======================
jours_fr = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
}

filtre["jour_semaine"] = (
    filtre["date"]
    .dt.day_name()
    .map(jours_fr)
)

ordre_jours = [
    "lundi", "mardi", "mercredi",
    "jeudi", "vendredi", "samedi", "dimanche"
]

stats_jour = (
    filtre.groupby("jour_semaine")["avg"]
    .mean()
    .reindex(ordre_jours)
)

fig_jours = px.bar(
    stats_jour,
    title="📅 Moyenne de viewers par jour de la semaine",
    labels={"value": "Viewers", "jour_semaine": "Jour"}
)

st.plotly_chart(fig_jours, use_container_width=True)

# ======================
# IMPACT DES RAIDS
# ======================
impact_raid = (
    filtre.groupby("raid")["avg"]
    .agg(["mean", "median", "count"])
    .reset_index()
)

fig_raid = px.bar(
    impact_raid,
    x="raid",
    y="mean",
    text="count",
    title="⚔️ Impact moyen des raids sur l’audience",
    labels={
        "raid": "Raid",
        "mean": "Viewers moyens",
        "count": "Nombre de streams"
    }
)

st.plotly_chart(fig_raid, use_container_width=True)

# ======================
# STREAKS (SÉRIES DE STREAM)
# ======================
filtre = filtre.sort_values("date")
filtre["ecart"] = filtre["date"].diff().dt.days
filtre["nouvelle_serie"] = filtre["ecart"] > 1
filtre["id_serie"] = filtre["nouvelle_serie"].cumsum()

longest_streak = (
    filtre.groupby("id_serie")
    .size()
    .max()
)

st.success(f"🔥 Plus longue série de streams : **{longest_streak} jours consécutifs**")



if True in impact_raid["raid"].values and False in impact_raid["raid"].values:
    avg_raid = impact_raid.loc[impact_raid["raid"] == True, "mean"].values[0]
    avg_no_raid = impact_raid.loc[impact_raid["raid"] == False, "mean"].values[0]

    uplift = ((avg_raid - avg_no_raid) / avg_no_raid) * 100

    st.metric(
        "📈 Gain moyen grâce aux raids",
        f"{uplift:.1f} %"
    )

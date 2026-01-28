import plotly.express as px

JOURS_FR = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
}

ORDRE_JOURS = [
    "Lundi", "Mardi", "Mercredi",
    "Jeudi", "Vendredi", "Samedi", "Dimanche"
]

def evolution_viewers(df):
    return px.line(
        df,
        x="date",
        y="avg",
        markers=True,
        title="📈 Évolution de la moyenne de viewers"
    )

def tendance_viewers(df):
    df = df.copy()
    df["moyenne_7j"] = df["avg"].rolling(7).mean()
    df["moyenne_30j"] = df["avg"].rolling(30).mean()

    return px.line(
        df,
        x="date",
        y=["avg", "moyenne_7j", "moyenne_30j"],
        title="📊 Tendance & croissance",
        labels={"value": "Viewers", "variable": "Type"}
    )

def viewers_par_jour(df):
    df = df.copy()
    df["jour_semaine"] = (
        df["date"].dt.day_name().map(JOURS_FR)
    )

    stats = (
        df.groupby("jour_semaine")["avg"]
        .mean()
        .reindex(ORDRE_JOURS)
    )

    return px.bar(
        stats,
        title="📅 Moyenne de viewers par jour",
        labels={"value": "Viewers"}
    )

def impact_raids(df):
    impact = (
        df.groupby("raid")["avg"]
        .agg(["mean", "median", "count"])
        .reset_index()
    )

    fig = px.bar(
        impact,
        x="raid",
        y="mean",
        text="count",
        title="⚔️ Impact des raids",
        labels={
            "raid": "Raid",
            "mean": "Viewers moyens",
            "count": "Nombre de streams"
        }
    )

    return fig, impact

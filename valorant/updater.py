from tracker_api import fetch_matches, fetch_profile
from database import get_connection
from datetime import datetime

def get_existing_match_ids():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT match_id FROM matches")
        return {row[0] for row in c.fetchall()}

def update_matches(riot_id, tag):
    existing_ids = get_existing_match_ids()
    matches = fetch_matches(riot_id, tag)

    with get_connection() as conn:
        c = conn.cursor()

        for m in matches:
            match_id = m["metadata"]["id"]
            if match_id in existing_ids:
                continue

            stats = m["stats"]
            c.execute("""
            INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                match_id,
                m["metadata"]["timestamp"],
                stats["agent"]["name"],
                m["metadata"]["map"],
                int(stats["team"] == "Red"),
                stats["kills"],
                stats["deaths"],
                stats["assists"],
                stats["kills"] / max(1, stats["deaths"]),
                stats["headshotsPercentage"],
                stats["score"]
            ))

        conn.commit()

def update_rank(riot_id, tag):
    profile = fetch_profile(riot_id, tag)
    rank = profile["segments"][0]["stats"]["rank"]["metadata"]["tierName"]
    rr = profile["segments"][0]["stats"]["rank"]["value"]

    with get_connection() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO rank_history VALUES (?,?,?)",
            (datetime.now().isoformat(), rank, rr)
        )
        conn.commit()

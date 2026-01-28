import requests
from datetime import datetime

API_KEY = "eb225e5d-1a95-4143-a3a0-7c0ae7529215"
BASE_URL = "https://public-api.tracker.gg/v2/valorant/standard"

HEADERS = {
    "TRN-Api-Key": API_KEY
}

def fetch_matches(riot_id, tag):
    url = f"{BASE_URL}/matches/riot/{riot_id}%23{tag}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["data"]["matches"]

def fetch_profile(riot_id, tag):
    url = f"{BASE_URL}/profile/riot/{riot_id}%23{tag}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["data"]

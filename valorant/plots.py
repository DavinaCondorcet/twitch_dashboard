import pandas as pd
import plotly.express as px
from database import get_connection

def load_matches():
    return pd.read_sql("SELECT * FROM matches", get_connection(), parse_dates=["date"])

def kda_over_time():
    df = load_matches().sort_values("date")
    df["rolling_kda"] = df["kda"].rolling(7).mean()
    return px.line(df, x="date", y="rolling_kda", title="KDA (rolling 7 games)")

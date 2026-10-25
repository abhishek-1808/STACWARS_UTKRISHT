"""Shared loading / cleaning helpers for STAC WARS PS2."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
OUT_DIR = ROOT / "outputs"
DEFAULT_CSV = ROOT / "data" / "SolarPrediction.csv"

ENV_COLS = ["Temperature", "Pressure", "Humidity", "WindDirection(Degrees)", "Speed"]


def load_data(path=DEFAULT_CSV) -> pd.DataFrame:
    """Read the CSV, build a proper Datetime column, sort and add helper columns."""
    df = pd.read_csv(path)

    # 'Data' holds the date (its time part is a dummy 12:00:00 AM), 'Time' the clock time.
    date_part = pd.to_datetime(df["Data"], errors="coerce").dt.normalize()
    df["Datetime"] = date_part + pd.to_timedelta(df["Time"].astype(str))
    df = df.dropna(subset=["Datetime", "Radiation"])
    df = df.drop(columns=["Data", "Time", "UNIXTime"], errors="ignore")
    df = df.sort_values("Datetime").reset_index(drop=True)

    df["Date"] = df["Datetime"].dt.date
    df["Month"] = df["Datetime"].dt.month_name()
    df["MinuteOfDay"] = df["Datetime"].dt.hour * 60 + df["Datetime"].dt.minute

    # sunrise / sunset strings -> minutes since midnight
    for src, dst in [("TimeSunRise", "SunriseMin"), ("TimeSunSet", "SunsetMin")]:
        df[dst] = pd.to_timedelta(df[src].astype(str)).dt.total_seconds() / 60
    df["MinSinceSunrise"] = df["MinuteOfDay"] - df["SunriseMin"]
    df["MinToSunset"] = df["SunsetMin"] - df["MinuteOfDay"]
    df["DayLengthMin"] = df["SunsetMin"] - df["SunriseMin"]
    return df

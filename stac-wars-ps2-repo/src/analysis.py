"""Parts A (visualisation) and C (solar-day report) of STAC WARS PS2.

Usage:  python src/analysis.py [--csv data/SolarPrediction.csv]
"""
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import load_data, FIG_DIR, OUT_DIR, ENV_COLS, DEFAULT_CSV

MONTHS = ["September", "October", "November", "December"]
TICKS = range(0, 1440, 120)
TICK_LABELS = [f"{h:02d}:00" for h in range(0, 24, 2)]


# ----------------------------------------------------------------- Part A
def plot_weekly(df):
    (FIG_DIR / "weekly").mkdir(parents=True, exist_ok=True)
    days = sorted(df["Date"].unique())
    for i in range(0, len(days), 7):
        sel = days[i:i + 7]
        wk = df[df["Date"].isin(sel)]
        plt.figure(figsize=(12, 5))
        sns.lineplot(data=wk, x="MinuteOfDay", y="Radiation", hue="Date",
                     palette="tab10", errorbar=None)
        plt.xticks(TICKS, TICK_LABELS)
        plt.xlabel("Time of Day"); plt.ylabel("Solar Radiation")
        plt.title(f"Solar Radiation: {sel[0]} to {sel[-1]}")
        plt.grid(alpha=0.25)
        plt.legend(title="Date", bbox_to_anchor=(1.02, 1), loc="upper left")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "weekly" / f"Solar_Radiation_vs_Days_{sel[0]}_to_{sel[-1]}.png", dpi=100)
        plt.close()


def plot_monthly_profiles(df):
    fig, axes = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=True)
    for ax, m in zip(axes.flatten(), MONTHS):
        d = df[df["Month"] == m]
        if d.empty:
            ax.set_visible(False)
            continue
        sns.lineplot(data=d, x="MinuteOfDay", y="Radiation", errorbar=None,
                     color="#E69F00", linewidth=2, ax=ax)
        ax.set_title(f"{m} (n={d['Date'].nunique()} days)", fontweight="bold")
        ax.set_xticks(TICKS); ax.set_xticklabels(TICK_LABELS, rotation=45)
        ax.set_xlabel("Time of Day"); ax.set_ylabel("Solar Radiation"); ax.grid(alpha=0.25)
    fig.suptitle("Monthly Average Daily Solar Radiation Profiles (2016)", fontsize=17, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "Monthly_Average_Daily_Solar_Radiation_Profiles__2016_.png", dpi=100)
    plt.close()


def plot_scatter(df):
    for col in ENV_COLS:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=col, y="Radiation", hue="Month", hue_order=MONTHS,
                        palette="turbo", alpha=0.5, s=25)
        plt.title(f"Solar Radiation vs {col}"); plt.grid(alpha=0.25); plt.tight_layout()
        safe = col.replace("(", "_").replace(")", "_")
        plt.savefig(FIG_DIR / f"Solar_Radiation_vs_{safe}.png", dpi=100)
        plt.close()


def plot_heatmap(df):
    corr = df[["Radiation"] + ENV_COLS].corr()
    plt.figure(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0,
                fmt=".2f", square=True, linewidths=0.5)
    plt.title("Correlation Between Solar Radiation and Weather Variables")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "Correlation_Between_Solar_Radiation_and_Weather_Variables.png", dpi=100)
    plt.close()
    return corr


def plot_bonus_sunstep(df):
    """Bonus: mean radiation vs minutes after listed sunrise, by month.
    Shows strong sun only appears some time after the official sunrise."""
    d = df[(df["MinSinceSunrise"] >= -30) & (df["MinSinceSunrise"] <= 240)]
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=d, x="MinSinceSunrise", y="Radiation", hue="Month",
                 hue_order=MONTHS, errorbar=None)
    plt.xlabel("Minutes after listed sunrise"); plt.ylabel("Mean solar radiation")
    plt.title("Bonus: delayed 'step' in radiation after sunrise"); plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "bonus_sunrise_step.png", dpi=100)
    plt.close()


# ----------------------------------------------------------------- Part C
def daily_report(df):
    return df.groupby("Date").agg(Max_Radiation=("Radiation", "max"),
                                  Avg_Radiation=("Radiation", "mean"))


def peak_day_analysis(df, daily):
    peak_date = daily["Max_Radiation"].idxmax()
    day = df[df["Date"] == peak_date]
    row = day.loc[day["Radiation"].idxmax()]
    solar_noon = (row["SunriseMin"] + row["SunsetMin"]) / 2
    hhmm = lambda m: f"{int(m // 60):02d}:{int(m % 60):02d}"
    near_peak = day[day["MinuteOfDay"].between(row["MinuteOfDay"] - 30, row["MinuteOfDay"] + 30)]
    return {
        "date": peak_date,
        "max_radiation": row["Radiation"],
        "peak_time": row["Datetime"].strftime("%H:%M:%S"),
        "temperature": row["Temperature"],
        "humidity": row["Humidity"],
        "wind_speed": row["Speed"],
        "sunrise": row["TimeSunRise"],
        "sunset": row["TimeSunSet"],
        "minutes_after_sunrise": row["MinSinceSunrise"],
        "minutes_before_sunset": row["MinToSunset"],
        "day_length_min": row["DayLengthMin"],
        "solar_noon": hhmm(solar_noon),
        "minutes_from_solar_noon": row["MinuteOfDay"] - solar_noon,
        "median_radiation_within_30min_of_peak": near_peak["Radiation"].median(),
    }


def main(csv):
    FIG_DIR.mkdir(exist_ok=True); OUT_DIR.mkdir(exist_ok=True)
    df = load_data(csv)

    plot_weekly(df); plot_monthly_profiles(df); plot_scatter(df)
    corr = plot_heatmap(df); plot_bonus_sunstep(df)
    print("Correlation with Radiation:\n", corr["Radiation"].sort_values(ascending=False).round(2))

    daily = daily_report(df)
    daily.to_csv(OUT_DIR / "daily_report.csv")
    print("\nDaily report (head):\n", daily.head())

    res = peak_day_analysis(df, daily)
    print("\nPeak-day analysis:")
    for k, v in res.items():
        print(f"  {k}: {v}")
    pd.Series(res).to_csv(OUT_DIR / "peak_day.csv", header=["value"])

    top5 = daily.nlargest(5, "Avg_Radiation")
    top5.to_csv(OUT_DIR / "top5_avg_days.csv")
    print("\nTop 5 days by average radiation:\n", top5)

    counts = df.groupby("Date").size().rename("n_obs")   # gaps show up as low counts
    counts.to_csv(OUT_DIR / "observations_per_day.csv")
    print("\nDays with fewest observations:\n", counts.nsmallest(5))
    print("\nDays per month:\n", df.groupby("Month")["Date"].nunique())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    main(ap.parse_args().csv)

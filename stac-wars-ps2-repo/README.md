# STAC WARS · PS2 — Solar Radiation Analysis and Prediction

Voyage-123 solar observation data: exploratory visualisation, inference, a day-wise
solar report, and a bonus regression model for predicting radiation.

## Repository layout

```
.
├── README.md
├── requirements.txt
├── data/                  # put SolarPrediction.csv here (git-ignored) – see data/README.md
├── notebooks/
│   └── stacwars.ipynb     # original exploratory notebook
├── src/
│   ├── common.py          # loading, datetime construction, sunrise/sunset features
│   ├── analysis.py        # Part A (plots) + Part C (daily report, peak day, top 5)
│   └── model.py           # Bonus: regression, RMSE / R², feature importance
├── figures/               # all plots (weekly/ holds one plot per 7-day window)
├── outputs/               # CSVs written by the scripts (daily report, scores, ...)
└── report/
    ├── STACWARS_PS2_Report.pdf
    └── problem_statement.pdf
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# put SolarPrediction.csv in data/
python src/analysis.py     # figures/ + outputs/daily_report.csv, peak_day.csv, top5_avg_days.csv
python src/model.py        # outputs/model_scores.csv, feature_importance.csv
```

## Task → file map

| Task | Marks | Where |
|---|---|---|
| A. Data visualisation | 4 | `src/analysis.py` (`plot_*`), `figures/` |
| B. Inferences | 5 | `report/STACWARS_PS2_Report.pdf` §3 |
| C. Solar day analysis | 5 | `src/analysis.py` (`daily_report`, `peak_day_analysis`), `outputs/` |
| Bonus: prediction | 6 | `src/model.py`, report §5 |

## Headline results

* Peak radiation: **1601.26** on **2016-09-04 at 12:15:04** (T = 61, humidity = 93, wind = 9.0),
  **367 min (6 h 07 min) after sunrise**, 380 min before sunset.
* Top-5 days by mean radiation: 09-19, 09-02, 09-22, 09-25, 09-28 (all September).
* Temperature has the strongest correlation with radiation (r = 0.73).
* Model scores: see `outputs/model_scores.csv` after running `src/model.py`.

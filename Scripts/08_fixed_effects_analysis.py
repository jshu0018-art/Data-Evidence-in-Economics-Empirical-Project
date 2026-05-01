"""08_fixed_effects_analysis.py

Build a panel dataset and estimate a two-way fixed effects model for fertility
as a function of female secondary enrollment.

This script uses the cleaned World Bank data in Data.clean and saves a
wide-format panel file at Data.clean/panel_fixed_effects_data.csv.
"""

from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "Data.clean"
OUTPUT_DIR = ROOT / "Outputs" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILES = [
    DATA_DIR / "Malawi_cleaned.csv",
    DATA_DIR / "Rwanda_cleaned.csv",
    DATA_DIR / "Burkina_Faso_cleaned.csv",
    DATA_DIR / "Mali_cleaned.csv",
]
PANEL_PATH = DATA_DIR / "panel_fixed_effects_data.csv"
RESULTS_PATH = OUTPUT_DIR / "fixed_effects_results.txt"


def build_panel(files):
    df = pd.concat([pd.read_csv(path) for path in files], ignore_index=True)
    panel = (
        df.pivot_table(
            index=["Country Name", "Country Code", "Year"],
            columns="Indicator",
            values="Value",
        )
        .reset_index()
        .rename_axis(None, axis=1)
        .rename(columns={"Country Name": "Country_Name"})
    )
    panel.to_csv(PANEL_PATH, index=False)
    return panel


def estimate_fixed_effects(panel):
    panel = panel.dropna(subset=["Female_Secondary_Enrollment_Rate", "Fertility_Rate"]).copy()
    model = smf.ols(
        "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
        data=panel,
    ).fit(cov_type="cluster", cov_kwds={"groups": panel["Country_Name"]})
    return model, panel


def save_results(model):
    with RESULTS_PATH.open("w", encoding="utf-8") as out:
        out.write(model.summary().as_text())


if __name__ == "__main__":
    panel_data = build_panel(INPUT_FILES)
    model, panel_data = estimate_fixed_effects(panel_data)

    print("Panel saved to:", PANEL_PATH)
    print("Number of observations after dropping missing values:", int(model.nobs))
    print("Regression R-squared:", round(model.rsquared, 4))
    print("Female_Secondary_Enrollment_Rate coefficient:", round(model.params["Female_Secondary_Enrollment_Rate"], 6))
    print("Clustered standard error:", round(model.bse["Female_Secondary_Enrollment_Rate"], 6))
    print("Results saved to:", RESULTS_PATH)

    save_results(model)

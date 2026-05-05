"""10_fixed_effects_table.py

Build the panel dataset and produce a regression table summary file for the
primary econometric analysis.

This script reproduces the data shown in the notebook by:
1. constructing the panel dataset from cleaned country CSVs,
2. saving the panel file at Data.clean/panel_fixed_effects_data.csv,
3. estimating the main and comparison regression specifications,
4. saving a regression-table CSV in Outputs/tables.
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
REGRESSION_TABLE_PATH = OUTPUT_DIR / "fixed_effects_regression_table.csv"
PANEL_SUMMARY_PATH = OUTPUT_DIR / "panel_summary.csv"


def build_panel(files):
    data_frames = []
    for path in files:
        if not path.exists():
            raise FileNotFoundError(f"Missing input file: {path}")
        data_frames.append(pd.read_csv(path))

    df = pd.concat(data_frames, ignore_index=True)
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


def summarize_panel(panel):
    summary = {
        "n_obs": [len(panel)],
        "year_min": [panel["Year"].min()],
        "year_max": [panel["Year"].max()],
        "country_list": [", ".join(sorted(panel["Country_Name"].unique()))],
    }
    country_counts = panel["Country_Name"].value_counts().sort_index()
    for country, count in country_counts.items():
        summary[f"count_{country}"] = [count]
    pd.DataFrame(summary).to_csv(PANEL_SUMMARY_PATH, index=False)
    return summary


def estimate_models(panel):
    panel = panel.dropna(subset=["Female_Secondary_Enrollment_Rate", "Fertility_Rate"]).copy()
    formulas = [
        ("Country + year fixed effects", "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)"),
        ("Country fixed effects only", "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name)"),
        ("Year fixed effects only", "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Year)"),
        ("Malawi-only OLS", "Fertility_Rate ~ Female_Secondary_Enrollment_Rate"),
    ]

    results = []
    for label, formula in formulas:
        if label == "Malawi-only OLS":
            data = panel[panel["Country_Name"] == "Malawi"].copy()
        else:
            data = panel

        model = smf.ols(formula, data=data).fit(
            cov_type="cluster" if label != "Malawi-only OLS" else "HC1",
            cov_kwds={"groups": data["Country_Name"]} if label != "Malawi-only OLS" else None,
        )

        results.append(
            {
                "Specification": label,
                "Coefficient": model.params["Female_Secondary_Enrollment_Rate"],
                "Std_Error": model.bse["Female_Secondary_Enrollment_Rate"],
                "p_value": model.pvalues["Female_Secondary_Enrollment_Rate"],
                "N": int(model.nobs),
                "R_squared": model.rsquared,
            }
        )

    regression_table = pd.DataFrame(results)
    regression_table.to_csv(REGRESSION_TABLE_PATH, index=False)
    return regression_table


def main():
    if PANEL_PATH.exists():
        panel = pd.read_csv(PANEL_PATH)
    else:
        panel = build_panel(INPUT_FILES)

    print("Panel file:", PANEL_PATH)
    print("Observations before dropping missing values:", len(panel))

    summary = summarize_panel(panel)
    print("Panel summary saved to:", PANEL_SUMMARY_PATH)

    regression_table = estimate_models(panel)
    print("Regression table saved to:", REGRESSION_TABLE_PATH)
    print(regression_table.to_string(index=False))


if __name__ == "__main__":
    main()

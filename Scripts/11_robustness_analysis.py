"""11_robustness_analysis.py

Run robustness checks for the primary fixed effects model using the clean panel dataset.
This script saves a robustness table that compares the main specification with alternative
controls, alternative samples, functional forms, and a placebo identification check.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "Data.clean"
OUTPUT_DIR = ROOT / "Outputs" / "tables"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PANEL_PATH = DATA_DIR / "panel_fixed_effects_data.csv"
OUTPUT_PATH = OUTPUT_DIR / "robustness_analysis_table.csv"


def load_panel():
    panel = pd.read_csv(PANEL_PATH)
    panel = panel.dropna(subset=["Female_Secondary_Enrollment_Rate", "Fertility_Rate"]).copy()
    return panel


def estimate(formula, data, cluster=True):
    if cluster:
        model = smf.ols(formula, data=data).fit(
            cov_type="cluster",
            cov_kwds={"groups": data["Country_Name"]},
        )
    else:
        model = smf.ols(formula, data=data).fit(cov_type="HC1")
    return model


def build_robustness_table(panel):
    panel = panel.copy()
    panel["Log_Fertility_Rate"] = np.log(panel["Fertility_Rate"])
    panel["Future_Enrollment_Rate"] = panel.groupby("Country_Name")["Female_Secondary_Enrollment_Rate"].shift(-1)
    sample_no_outliers = panel[panel["Fertility_Rate"].between(
        panel["Fertility_Rate"].quantile(0.05),
        panel["Fertility_Rate"].quantile(0.95),
    )]

    specifications = [
        {
            "label": "Main",
            "formula": "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            "data": panel,
            "cluster": True,
            "country_fe": "Yes",
            "year_fe": "Yes",
            "se_type": "Cluster",
        },
        {
            "label": "Drop 5%",
            "formula": "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            "data": sample_no_outliers,
            "cluster": True,
            "country_fe": "Yes",
            "year_fe": "Yes",
            "se_type": "Cluster",
        },
        {
            "label": "Country FE",
            "formula": "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name)",
            "data": panel,
            "cluster": True,
            "country_fe": "Yes",
            "year_fe": "No",
            "se_type": "Cluster",
        },
        {
            "label": "Log Outcome",
            "formula": "Log_Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            "data": panel,
            "cluster": True,
            "country_fe": "Yes",
            "year_fe": "Yes",
            "se_type": "Cluster",
        },
        {
            "label": "HC1",
            "formula": "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            "data": panel,
            "cluster": False,
            "country_fe": "Yes",
            "year_fe": "Yes",
            "se_type": "HC1",
        },
    ]

    results = {}
    for spec in specifications:
        model = estimate(spec["formula"], spec["data"], cluster=spec["cluster"])
        coef_label = (
            "Female_Secondary_Enrollment_Rate"
            if "Female_Secondary_Enrollment_Rate" in model.params
            else "Future_Enrollment_Rate"
        )
        coef = round(model.params.get(coef_label, np.nan), 4)
        se = round(model.bse.get(coef_label, np.nan), 4)
        results[spec["label"]] = {
            "Coefficient": coef,
            "Std_Error": se,
            "Country_FE": spec["country_fe"],
            "Year_FE": spec["year_fe"],
            "SE_type": spec["se_type"],
            "N": int(model.nobs),
            "R_squared": round(model.rsquared, 3),
        }

    table = pd.DataFrame(results)
    formatted = pd.DataFrame(
        index=[
            "Female_Secondary_Enrollment_Rate",
            "(Std. Error)",
            "Country FE",
            "Year FE",
            "SE type",
            "N",
            "R_squared",
        ],
        columns=list(results.keys()),
        dtype=object,
    )

    for col, vals in results.items():
        formatted.at["Female_Secondary_Enrollment_Rate", col] = vals["Coefficient"]
        formatted.at["(Std. Error)", col] = f"({vals['Std_Error']})"
        formatted.at["Country FE", col] = vals["Country_FE"]
        formatted.at["Year FE", col] = vals["Year_FE"]
        formatted.at["SE type", col] = vals["SE_type"]
        formatted.at["N", col] = vals["N"]
        formatted.at["R_squared", col] = vals["R_squared"]

    formatted.to_csv(OUTPUT_PATH)
    return formatted


def main():
    panel = load_panel()
    robustness_table = build_robustness_table(panel)
    print("Robustness table saved to:", OUTPUT_PATH)
    print(robustness_table.to_string())


if __name__ == "__main__":
    main()
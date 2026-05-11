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

    specifications = [
        (
            "Main: TWFE (cluster)",
            "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            panel,
            True,
            "Fertility_Rate",
            "Main country and year fixed effects estimate with clustered SEs.",
        ),
        (
            "Country FE only",
            "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name)",
            panel,
            True,
            "Fertility_Rate",
            "Alternative control set with country fixed effects only.",
        ),
        (
            "Year FE only",
            "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Year)",
            panel,
            True,
            "Fertility_Rate",
            "Alternative control set with year fixed effects only.",
        ),
        (
            "Log Fertility (TWFE)",
            "Log_Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            panel,
            True,
            "Log_Fertility_Rate",
            "Alternative functional form using the log of fertility.",
        ),
        (
            "No Mali",
            "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            panel[panel["Country_Name"] != "Mali"],
            True,
            "Fertility_Rate",
            "Alternative sample excluding Mali to test sample sensitivity.",
        ),
        (
            "Future Enrollment Placebo",
            "Fertility_Rate ~ Future_Enrollment_Rate + C(Country_Name) + C(Year)",
            panel.dropna(subset=["Future_Enrollment_Rate"]),
            True,
            "Fertility_Rate",
            "Identification-relevant placebo test using next-year enrollment.",
        ),
        (
            "Main: TWFE (HC1)",
            "Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)",
            panel,
            False,
            "Fertility_Rate",
            "Alternative inference using heteroskedasticity-robust SEs instead of clustering.",
        ),
    ]

    rows = []
    for label, formula, data, cluster, outcome, note in specifications:
        model = estimate(formula, data, cluster=cluster)
        coef_label = (
            "Female_Secondary_Enrollment_Rate"
            if "Female_Secondary_Enrollment_Rate" in model.params
            else "Future_Enrollment_Rate"
        )
        rows.append(
            {
                "Specification": label,
                "Outcome": outcome,
                "Coefficient": model.params.get(coef_label, np.nan),
                "Std_Error": model.bse.get(coef_label, np.nan),
                "p_value": model.pvalues.get(coef_label, np.nan),
                "N": int(model.nobs),
                "R_squared": model.rsquared,
                "Note": note,
            }
        )

    long_table = pd.DataFrame(rows).set_index("Specification")
    long_table["Coefficient"] = long_table["Coefficient"].round(4)
    long_table["Std_Error"] = long_table["Std_Error"].round(4)
    long_table["p_value"] = long_table["p_value"].apply(lambda x: "<0.001" if x < 0.001 else round(x, 3))
    long_table["R_squared"] = long_table["R_squared"].round(3)

    wide_table = long_table.T.loc[
        ["Outcome", "Coefficient", "Std_Error", "p_value", "N", "R_squared", "Note"]
    ]
    wide_table.to_csv(OUTPUT_PATH)
    return wide_table


def main():
    panel = load_panel()
    robustness_table = build_robustness_table(panel)
    print("Robustness table saved to:", OUTPUT_PATH)
    print(robustness_table.to_string())


if __name__ == "__main__":
    main()

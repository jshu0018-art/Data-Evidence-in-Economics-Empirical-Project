"""Run the full data extraction, cleaning, and fixed effects pipeline.

This script executes the updated scripts in sequence:
1. Extract raw World Bank ZIP files for Rwanda and Burkina Faso
2. Clean Malawi, Rwanda, Burkina Faso, and Mali data
3. Build the panel dataset and estimate the fixed effects model
4. Generate regression tables and robustness checks
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "Scripts"

SCRIPT_ORDER = [
    SCRIPTS_DIR / "02_extract_rwanda_burkina_data.py",
    SCRIPTS_DIR / "02_clean_wb_data.py",
    SCRIPTS_DIR / "04_clean_rwanda_data.py",
    SCRIPTS_DIR / "05_clean_burkina_faso_data.py",
    SCRIPTS_DIR / "06_clean_mali_data.py",
    SCRIPTS_DIR / "08_fixed_effects_analysis.py",
    SCRIPTS_DIR / "10_fixed_effects_table.py",
    SCRIPTS_DIR / "11_robustness_analysis.py",
]


def run_script(script_path: Path) -> None:
    print(f"Running {script_path.name}...")
    completed = subprocess.run([sys.executable, str(script_path)], cwd=ROOT)
    if completed.returncode != 0:
        raise subprocess.CalledProcessError(completed.returncode, completed.args)


def main() -> None:
    for script in SCRIPT_ORDER:
        if not script.exists():
            raise FileNotFoundError(f"Required script not found: {script}")
        run_script(script)
    print("All steps completed successfully.")


if __name__ == "__main__":
    main()
"""Run the full data extraction, cleaning, and fixed effects pipeline.

This script executes the updated scripts in sequence:
1. Extract raw World Bank ZIP files for Rwanda, Burkina Faso, and Mali
2. Clean Rwanda data
3. Clean Burkina Faso data
4. Clean Mali data
5. Build the panel dataset and estimate the fixed effects model
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "Scripts"

SCRIPT_ORDER = [
    SCRIPTS_DIR / "02_extract_rwanda_burkina_data.py",
    SCRIPTS_DIR / "04_clean_rwanda_data.py",
    SCRIPTS_DIR / "05_clean_burkina_faso_data.py",
    SCRIPTS_DIR / "06_clean_mali_data.py",
    SCRIPTS_DIR / "08_fixed_effects_analysis.py",
]


def run_script(script_path):
    print(f"Running {script_path.name}...")
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT))
    if result.returncode != 0:
        raise SystemExit(f"Script failed: {script_path.name} (exit code {result.returncode})")
    print(f"Completed {script_path.name}\n")


def main():
    for script in SCRIPT_ORDER:
        if not script.exists():
            raise FileNotFoundError(f"Required script not found: {script}")
        run_script(script)
    print("All steps completed successfully.")


if __name__ == "__main__":
    main()

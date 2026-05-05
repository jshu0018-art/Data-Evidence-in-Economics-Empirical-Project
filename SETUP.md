# Quick Start Guide

## For First-Time Users

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Data-Evidence-in-Economics-Empirical-Project
```

### 2. Set Up Your Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify Python and pip
python --version
pip --version
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Data Processing Pipeline
The cleaned datasets already exist in `Data.clean/`, but to regenerate them from raw data:

```bash
# First, extract Rwanda and Burkina Faso data from ZIP archives
python Scripts/02_extract_rwanda_burkina_data.py

# Then clean each country's data
python Scripts/02_clean_wb_data.py      # Malawi
python Scripts/04_clean_rwanda_data.py  # Rwanda
python Scripts/05_clean_burkina_faso_data.py  # Burkina Faso
python Scripts/06_clean_mali_data.py    # Mali (optional)
```

### 5. Verify Outputs
Check that the following files exist in `Data.clean/`:
- `Malawi_cleaned.csv`
- `Rwanda_cleaned.csv`
- `Burkina_Faso_cleaned.csv`
- `Mali_cleaned.csv`
- `panel_fixed_effects_data.csv`

### 6. Run the Primary Econometric Analysis (NEW!)

The repository now includes a complete, reproducible primary analysis notebook:

**Option A: View & Run the Analysis Notebook**
```bash
# With Jupyter installed (included in requirements.txt)
jupyter notebook Analysis/Primary_Econometric_Analysis.ipynb
```

This notebook contains:
- Declaration of causal vs. descriptive analysis
- Econometric specification (two-way fixed effects model)
- Identification strategy and assumptions
- Regression results table
- Interpretation of coefficients
- Threats to inference (OVB, reverse causality, measurement error)
- Reproducibility verification

**Option B: Regenerate from Raw Data (Full Pipeline)**
```bash
# Step 1: Clean all country data (if not already done)
python Scripts/06_clean_mali_data.py

# Step 2: Build panel dataset and run regression
python Scripts/08_fixed_effects_analysis.py

# Step 3: Open and run the analysis notebook
jupyter notebook Analysis/Primary_Econometric_Analysis.ipynb
```

**Expected Results:**
- Main coefficient: Female enrollment effect on fertility ≈ **-0.0015** (not significant, p ≈ 0.948)
- Sample size: **N = 70** country-year observations
- Model fit: **R² = 0.951**
- Conclusion: No statistically significant causal effect detected

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: Data.raw/...` | Ensure you're running scripts from the project root directory |
| `Permission denied` | Use `python` instead of `python.exe` on Windows |
| Script runs but no output file | Check `Data.clean/` folder permissions |

## Project Structure Explained

```
Data-Evidence-in-Economics-Empirical-Project/
├── Data.raw/           ← Raw World Bank data (don't modify)
├── Data.clean/         ← Cleaned, processed data (ready for analysis)
├── Scripts/            ← Data processing Python scripts
├── Outputs/            ← Analysis results (figures, tables)
├── Docs/               ← Research documentation
└── requirements.txt    ← Python dependencies
```

## Next Steps

1. **Explore the cleaned data**: Open `Data.clean/*.csv` files to examine the data structure
2. **Run analyses**: Use the cleaned datasets for statistical modeling and visualization
3. **Add new scripts**: Follow the naming convention: `02_`, `03_`, `04_` for extraction/cleaning steps
4. **Document findings**: Save results to `Outputs/figures/` and `Outputs/tables/`

## For Questions or Issues

- Check the main README.md for research context
- Review script comments and docstrings
- Verify you followed all setup steps above

# Data-Evidence-in-Economics-Empirical-Project

**🚀 Quick Start:** New to this project? See [SETUP.md](SETUP.md) for step-by-step installation and usage instructions.

## Research Question 
What is the effect of increases in female secondary school enrolment on fertility rates in Malawi between
2005–2025, compared with Sub-Saharan countries with declining or stagnating female enrolment?

**Countries Analyzed:** Malawi (primary), Rwanda, Burkina Faso, Mali (comparison countries)

Members: Scott (35101652) & Jethro (34932267)

1. Repository Structure 

Data-Evidence-in-Economics-Empirical-Project/
│
├── 📋 Project Setup Files
│   ├── README.md                         # This file - project overview and documentation
│   ├── SETUP.md                          # ⭐ Quick start guide for first-time users
│   ├── requirements.txt                  # Python dependencies (exact versions)
│   └── .gitignore                        # Files excluded from Git version control
│
├── 📊 Data Management (4 Countries)
│   ├── Data.raw/                         # ⚠️ Raw data files (original, untouched - DO NOT MODIFY)
│   │   ├── b43612c8-b13c-4b4e-89d2-2a8303a6a69e_Data.csv              # Malawi indicators
│   │   ├── b43612c8-b13c-4b4e-89d2-2a8303a6a69e_Series - Metadata.csv # Malawi metadata
│   │   ├── 6ad77ab6-1f20-4bba-b9a4-eb918e568cf6_Data.csv              # Rwanda indicators
│   │   ├── 6ad77ab6-1f20-4bba-b9a4-eb918e568cf6_Series - Metadata.csv # Rwanda metadata
│   │   ├── 9ec8500a-8dcf-47b3-9ac9-6c3a240f82d9_Data.csv              # Burkina Faso indicators
│   │   ├── 9ec8500a-8dcf-47b3-9ac9-6c3a240f82d9_Series - Metadata.csv # Burkina Faso metadata
│   │   ├── *Mali*Data.csv                                              # Mali indicators
│   │   ├── *Mali*Series - Metadata.csv                                 # Mali metadata
│   │   └── *.zip                                                        # Original ZIP archives
│   │
│   └── Data.clean/                       # ✅ Cleaned, analysis-ready datasets
│       ├── Malawi_cleaned.csv            # Long format: Country, Year, Indicator, Value
│       ├── Rwanda_cleaned.csv
│       ├── Burkina_Faso_cleaned.csv
│       └── mali_clean_data.csv           # Mali data (cleaned)
│
├── 🔧 Processing Scripts
│   └── Scripts/
│       ├── 01_get_wb_data.py                    # Fetch data from World Bank API (alternative)
│       ├── 02_clean_wb_data.py                  # Clean Malawi data → Data.clean/Malawi_cleaned.csv
│       ├── 02_extract_rwanda_burkina_data.py    # Extract Rwanda & Burkina ZIP files
│       ├── 04_clean_rwanda_data.py              # Clean Rwanda data → Data.clean/Rwanda_cleaned.csv
│       ├── 05_clean_burkina_faso_data.py        # Clean Burkina data → Data.clean/Burkina_Faso_cleaned.csv
│       └── 06_clean_mali_data.py                # Clean Mali data → Data.clean/mali_clean_data.csv
│
├── 📈 Analysis & Results
│   └── Outputs/
│       ├── figures/                      # Plots, visualizations, maps, comparative analysis
│       └── tables/                       # Regression tables, summary statistics (4 countries)
│
├── 📚 Documentation
│   └── Docs/
│       ├── research_proposal.md
│       ├── codebook.md                   # Data variable definitions
│       └── methodology.md                # Statistical methods & analysis approach
│
└── 💾 Version Control
    └── .git/                             # Git repository history


2. Software Information
To run this project, you will need Python 3.10+. The following packages are required:

- **pandas**: For data manipulation
- **wbgapi**: To pull live World Bank data
- **pyreadstat**: To read DHS .dta (Stata) files
- **statsmodels**: For running the regression analysis
- **matplotlib / seaborn**: For data visualization

### Installation & Setup

**Option 1: Using requirements.txt (Recommended for reproducibility)**
```bash
# Clone the repository
git clone <repository-url>
cd Data-Evidence-in-Economics-Empirical-Project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Option 2: Manual installation**
```bash
pip install pandas>=2.0.0 wbgapi>=1.0.12 pyreadstat>=1.2.0 statsmodels>=0.14.0 matplotlib>=3.8.0 seaborn>=0.13.0
```

### Verify Installation
Run this command to verify all packages are installed:
```bash
python -c "import pandas, wbgapi, statsmodels, matplotlib, seaborn; print('All packages installed successfully!')"
```

3. Data Acquisition and Processing

The project analyzes World Bank indicators for **female secondary school enrollment** and **fertility rates** across four Sub-Saharan African countries: Malawi (primary case), Rwanda, Burkina Faso, and Mali (comparison countries) for the period 2005-2024.

### Data Sources
World Bank Open Data - World Development Indicators
- **Indicator 1:** SE.SEC.ENRR.FE (School enrollment, secondary, female % gross)
- **Indicator 2:** SP.DYN.TFRT.IN (Fertility rate, total births per woman)

### Complete Data Processing Workflow

| Step | Script | Input | Output | Description |
|------|--------|-------|--------|-------------|
| 1 | `02_clean_wb_data.py` | `Data.raw/*Malawi*Data.csv` | `Data.clean/Malawi_cleaned.csv` | Transform Malawi data to long format |
| 2 | `02_extract_rwanda_burkina_data.py` | `Data.raw/*.zip` (Rwanda + Burkina) | Extracted CSVs in `Data.raw/` | Extract ZIP files containing Rwanda & Burkina data |
| 3 | `04_clean_rwanda_data.py` | `Data.raw/*Rwanda*Data.csv` | `Data.clean/Rwanda_cleaned.csv` | Transform Rwanda data to long format |
| 4 | `05_clean_burkina_faso_data.py` | `Data.raw/*Burkina*Data.csv` | `Data.clean/Burkina_Faso_cleaned.csv` | Transform Burkina Faso data to long format |
| 5 | `06_clean_mali_data.py` | `Data.raw/*Mali*Data.csv` | `Data.clean/mali_clean_data.csv` | Transform Mali data to long format |

### Run the Complete Pipeline

On first setup, run all scripts in order:
```bash
# Step 1: Clean Malawi
python Scripts/02_clean_wb_data.py

# Step 2: Extract Rwanda & Burkina ZIP files
python Scripts/02_extract_rwanda_burkina_data.py

# Step 3: Clean Rwanda
python Scripts/04_clean_rwanda_data.py

# Step 4: Clean Burkina Faso
python Scripts/05_clean_burkina_faso_data.py

# Step 5: Clean Mali
python Scripts/06_clean_mali_data.py

# Verify all output files exist
ls Data.clean/
# Should show: Malawi_cleaned.csv  Rwanda_cleaned.csv  Burkina_Faso_cleaned.csv  mali_clean_data.csv
```

### Data Format

All cleaned datasets follow the same **long format** structure:

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| Country Name | string | "Malawi" | Country name |
| Country Code | string | "MWI" | 3-letter ISO country code |
| Year | integer | 2020 | Year of measurement (2005-2024) |
| Indicator | string | "Fertility_Rate" | Either Female_Secondary_Enrollment_Rate or Fertility_Rate |
| Value | float | 3.72 | Numeric value for the indicator |

**Example:**
```
Country Name,Country Code,Year,Indicator,Value
Malawi,MWI,2005,Female_Secondary_Enrollment_Rate,24.858
Malawi,MWI,2005,Fertility_Rate,5.848
...
```

### Alternative: Fetch Latest Data from World Bank API

To download the most current data directly from the World Bank API (optional):
```bash
python Scripts/01_get_wb_data.py
```

### Optional: Add DHS Microdata

For Demographic and Health Survey (DHS) micro-level survey data:
1. Register at [The DHS Program](https://dhsprogram.com)
2. Request access to DHS datasets for Malawi, Rwanda, and Burkina Faso
3. Download Individual Recode (IR) files in Stata (.dta) format
4. Place downloaded files in `Data.raw/`
5. These files are excluded from GitHub tracking via `.gitignore` (respects DHS data use agreements)

### Troubleshooting Data Processing

| Issue | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: Data.raw/...` | Scripts not run from project root | Use `cd Data-Evidence-in...` to enter project directory |
| Empty output files | Data extraction failed | Re-run `02_extract_rwanda_burkina_data.py` |
| Missing indicators | Raw data format changed | Check World Bank data structure hasn't changed |

4. How to Verify Your Setup

Follow these steps to verify everything is working correctly:

**1. Verify Python Environment**
```bash
python --version        # Should be 3.10 or higher
pip --version          # Should match your Python version
```

**2. Verify Required Packages**
```bash
python -c "import pandas, wbgapi, statsmodels, matplotlib, seaborn; print('✅ All packages installed!')"
```

**3. Verify File Structure**
```bash
# Check all required folders exist
ls Data.raw/            # Should have CSV files
ls Data.clean/          # Should have *cleaned.csv files
ls Scripts/             # Should have .py scripts
```

**4. Run the Data Pipeline (if regenerating from scratch)**
```bash
# Run each script and verify output
python Scripts/02_clean_wb_data.py
python Scripts/02_extract_rwanda_burkina_data.py
python Scripts/04_clean_rwanda_data.py
python Scripts/05_clean_burkina_faso_data.py

# Verify output files
ls -lh Data.clean/       # Check file sizes are not zero
```

**5. Verify Data Quality**
```python
# Open Python and check data structure
python
>>> import pandas as pd
>>> df = pd.read_csv('Data.clean/Malawi_cleaned.csv')
>>> print(df.shape)         # Should show (21 or more rows, 5 columns)
>>> print(df.columns.tolist())  # Should have: Country Name, Country Code, Year, Indicator, Value
>>> print(df.head())
>>> exit()
```

5. Project Status

**Completed:**
- ✅ World Bank data extracted for Malawi, Rwanda, Burkina Faso, and Mali
- ✅ Data cleaning scripts for all four countries
- ✅ Clean datasets ready for analysis in Data.clean/

**In Progress:**
- 📊 Comparative analysis of female enrollment and fertility trends
- 📈 Regression models and statistical testing

**To Do:**
- Document research methodology in Docs/
- Create visualization notebooks
- Generate final regression tables and figures 

---

6. Getting Help

**For Setup Issues:**
→ See [SETUP.md](SETUP.md) for detailed step-by-step instructions and troubleshooting

**For Data Questions:**
- Check the data format tables in Section 3 of this README
- Review `Docs/codebook.md` for variable definitions (when available)

**For Script Errors:**
1. Verify you're in the project root directory: `pwd` or `cd` to the project folder
2. Check that all data files exist: `ls Data.raw/` and `ls Data.clean/`
3. Re-run the script with verbose output:
   ```bash
   python -u Scripts/02_clean_wb_data.py
   ```
4. Check `requirements.txt` package versions match installed packages: `pip list`

---

7. Data Sources & References

### World Bank Open Data
- **Source:** World Bank Data (https://data.worldbank.org)
- **License:** Creative Commons Attribution 4.0 International
- **Citation:** World Bank. (Year). World Development Indicators. Retrieved from https://data.worldbank.org

### Indicators Used
| Code | Name | Source |
|------|------|--------|
| SE.SEC.ENRR.FE | School enrollment, secondary, female (% gross) | UNESCO Institute for Statistics |
| SP.DYN.TFRT.IN | Fertility rate, total (births per woman) | UN World Population Prospects |

### Countries Analyzed
- 🇲🇼 **Malawi** - Primary case study (focus country for research question)
- 🇷🇼 **Rwanda** - Comparative country (growing female enrollment, declining fertility)
- 🇧🇫 **Burkina Faso** - Comparative country (lower/stagnating enrollment, high fertility)
- 🇲🇱 **Mali** - Comparative country (declining enrollment trends, high fertility rates)

**Data Coverage:** 2005-2024 for all four countries

---

## Questions or Issues?

- See [SETUP.md](SETUP.md) for installation help
- Review script comments for technical details
- Check the `/Docs` folder for additional documentation

**Last Updated:** March 31, 2026  
**Project Members:** Scott (35101652) & Jethro (34932267)
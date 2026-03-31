import wbgapi as wb
import pandas as pd

# Define World Bank indicators
# SE.SEC.ENRR.FE: School enrollment, secondary, female (% gross)
# SP.DYN.TFRT.IN: Fertility rate, total (births per woman)
indicators = ['SE.SEC.ENRR.FE', 'SP.DYN.TFRT.IN']

# Define countries: Malawi and selected Sub-Saharan African countries for comparison
# Malawi (MWI), South Africa (ZAF), Nigeria (NGA), Kenya (KEN), Tanzania (TZA)
countries = ['MWI', 'ZAF', 'NGA', 'KEN', 'TZA']

# Fetch data for the period 2005-2024 (latest available)
data = wb.data.DataFrame(indicators, countries, time=range(2005, 2025))

# Reset index to make country and year columns
data = data.reset_index()

# Check actual column names and rename appropriately
print("Columns in fetched data:", data.columns.tolist())

# Rename columns for clarity (adjust index names based on actual column names)
rename_cols = {
    'SE.SEC.ENRR.FE': 'Female_Secondary_Enrollment_Rate',
    'SP.DYN.TFRT.IN': 'Fertility_Rate'
}

# Handle index columns - they may be named differently
if 'economy' in data.columns:
    rename_cols['economy'] = 'Country'
if 'time' in data.columns:
    rename_cols['time'] = 'Year'
    
data = data.rename(columns=rename_cols)

# Save to CSV in the raw data folder
data.to_csv('Data.raw/wb_comparison_raw.csv', index=False)

print("World Bank data downloaded and saved to Data.raw/wb_comparison_raw.csv")
print(f"Data shape: {data.shape}")
print(data.head())
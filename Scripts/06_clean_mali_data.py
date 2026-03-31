"""
Script: 06_clean_mali_data.py
Purpose: Clean and transform Mali World Bank data
Author: Data-Evidence-in-Economics-Empirical-Project
Date: 2026

Description:
    Reads raw World Bank data for Mali from Data.raw/
    Filters for female secondary enrollment and fertility rates
    Transforms wide format (years as columns) to long format (years as rows)
    Handles missing values (represented as '..')
    Outputs clean, analysis-ready CSV to Data.clean/

Input:
    Data.raw/*Mali*Data.csv

Output:
    Data.clean/mali_clean_data.csv (long format with columns: Country, Year, Indicator, Value)

Dependencies:
    - pandas>=2.0.0
    - os (standard library)

Usage:
    python Scripts/06_clean_mali_data.py
"""

import pandas as pd
import os

# Define file paths (relative to project root)
raw_data_path = 'Data.raw/*Mali*Data.csv'
clean_data_path = 'Data.clean/mali_clean_data.csv'

# Find Mali data file
import glob
mali_files = glob.glob(raw_data_path)

if not mali_files:
    print(f"Error: No Mali data file found matching pattern '{raw_data_path}'")
    print("Available files in Data.raw/:")
    for f in os.listdir('Data.raw/'):
        if f.endswith('.csv'):
            print(f"  - {f}")
    exit(1)

raw_data_path = mali_files[0]
print(f"Using Mali data file: {raw_data_path}")

# Ensure Data.clean directory exists
os.makedirs('Data.clean', exist_ok=True)

# Read the raw data
print("Reading raw Mali data...")
df = pd.read_csv(raw_data_path)

# Filter for relevant indicators
# SE.SEC.ENRR.FE: School enrollment, secondary, female (% gross)
# SP.DYN.TFRT.IN: Fertility rate, total (births per woman)
relevant_series_codes = ['SE.SEC.ENRR.FE', 'SP.DYN.TFRT.IN']
df_filtered = df[df['Series Code'].isin(relevant_series_codes)].copy()

# Melt the data from wide to long format
# Identify year columns (they start with a digit)
year_columns = [col for col in df_filtered.columns if col[0].isdigit()]

# Melt
df_long = df_filtered.melt(
    id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
    value_vars=year_columns,
    var_name='Year_Column',
    value_name='Value'
)

# Extract year from column name (e.g., '2005 [YR2005]' -> 2005)
df_long['Year'] = df_long['Year_Column'].str.extract(r'(\d{4})').astype(int)

# Clean the value column: replace '..' with NaN and convert to float
df_long['Value'] = pd.to_numeric(df_long['Value'], errors='coerce')

# Rename series for clarity
series_rename = {
    'SE.SEC.ENRR.FE': 'Female_Secondary_Enrollment_Rate',
    'SP.DYN.TFRT.IN': 'Fertility_Rate'
}
df_long['Indicator'] = df_long['Series Code'].map(series_rename)

# Select and reorder columns
df_clean = df_long[['Country Name', 'Country Code', 'Year', 'Indicator', 'Value']].copy()

# Sort the data
df_clean = df_clean.sort_values(['Country Name', 'Year', 'Indicator'])

# Save to clean data folder
df_clean.to_csv(clean_data_path, index=False)

print(f"Cleaned data saved to {clean_data_path}")
print(f"Shape: {df_clean.shape}")
print(df_clean.head(10))

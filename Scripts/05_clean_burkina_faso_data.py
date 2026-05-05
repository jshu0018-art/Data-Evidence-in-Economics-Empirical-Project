import pandas as pd
import os

# Define paths
raw_data_path = 'Data.raw/6ad77ab6-1f20-4bba-b9a4-eb918e568cf6_Data.csv'
clean_data_path = 'Data.clean/Burkina_Faso_cleaned.csv'

# Ensure Data.clean directory exists
os.makedirs('Data.clean', exist_ok=True)

# Read the raw data
df = pd.read_csv(raw_data_path)

# Filter for relevant indicators
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

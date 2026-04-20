import csv

# Path to the original CSV file
file_path = r"c:\Users\Vei Ze\AppData\Local\Temp\f2bed5e3-7a30-40db-b363-d45d508ef168_P_Data_Extract_From_World_Development_Indicators Mali.zip.168\ac77fa85-ca9e-4cd7-ba66-42686c3899e3_Data.csv"

# Read the CSV
with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Find the relevant rows
fertility_row = None
secondary_row = None

for row in data:
    if row['Series Name'] == 'Fertility rate, total (births per woman)':
        fertility_row = row
    elif row['Series Name'] == 'School enrollment, secondary (% gross)':
        secondary_row = row

# Years from 2000, then 2016-2025
years = ['2000 [YR2000]'] + [f'{year} [YR{year}]' for year in range(2016, 2026)]

# Extract data
output_data = []
for year in years:
    year_clean = year.split(' ')[0]
    fert_value = fertility_row.get(year, '..') if fertility_row else '..'
    sec_value = secondary_row.get(year, '..') if secondary_row else '..'
    output_data.append({
        'Year': year_clean,
        'Fertility Rate': fert_value,
        'Secondary School Enrollment (%)': sec_value
    })

# Write to new CSV
output_path = r"c:\Users\Vei Ze\AppData\Local\Temp\mali_data_clean.csv"
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Year', 'Fertility Rate', 'Secondary School Enrollment (%)']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

print("New CSV created at:", output_path)

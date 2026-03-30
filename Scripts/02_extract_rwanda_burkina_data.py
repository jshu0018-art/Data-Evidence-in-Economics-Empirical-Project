import zipfile
import os

# Define paths for Rwanda and Burkina zip files
zip_files = [
    'Data.raw/P_Data_Extract_From_World_Development_Indicators Rwanda.zip',
    'Data.raw/P_Data_Extract_From_World_Development_Indicators  Burkina.zip'
]
extract_dir = 'Data.raw/'

# Extract both ZIP files
for zip_file in zip_files:
    if not os.path.exists(zip_file):
        print(f"Warning: {zip_file} not found.")
        continue
    
    print(f"Extracting {os.path.basename(zip_file)}...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"✓ Successfully extracted {os.path.basename(zip_file)}")
    except Exception as e:
        print(f"Error extracting {zip_file}: {e}")

# List all files in Data.raw
print("\n" + "="*60)
print("Files now in Data.raw/:")
print("="*60)
extracted_files = os.listdir(extract_dir)
for file in sorted(extracted_files):
    file_path = os.path.join(extract_dir, file)
    if os.path.isfile(file_path):
        size = os.path.getsize(file_path)
        print(f"  - {file} ({size} bytes)")
    else:
        print(f"  - {file}/ (folder)")

print("\nRwanda and Burkina Faso World Development Indicators data is now ready in Data.raw/")

import zipfile
import os
import glob

# Discover all World Development Indicators ZIP files in Data.raw
zip_files = sorted(glob.glob('Data.raw/*.zip'))
extract_dir = 'Data.raw/'

for zip_file in zip_files:
    name = os.path.basename(zip_file)
    print(f"Extracting {name}...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Successfully extracted {name}")
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

print("\nCountry World Development Indicators raw data is now ready in Data.raw/")

import pandas as pd
import requests
from urllib.parse import urlparse
import os

# Load the Excel file
file_path = 'Furniture.xlsx'  # Update with your file path
excel_data = pd.ExcelFile(file_path)

# Load the data from the first sheet (adjust sheet_name as needed)
df = pd.read_excel(excel_data, sheet_name=0)

# Ensure the 'Image Name' column exists and is correctly spelled
if 'Image Name' in df.columns:
    image_column = 'Image Name'
else:
    print("Error: 'Image Name' column not found in Excel file.")
    exit(1)

# Create a directory to save images (if it doesn't exist)
save_dir = 'downloaded_images'
os.makedirs(save_dir, exist_ok=True)

# Function to download and save image
def download_image(url, file_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Image saved: {file_name}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Exception occurred while downloading image: {e}")

# Iterate through each row in the dataframe
for index, row in df.iterrows():
    image_url = row[image_column]
    if pd.notna(image_url):
        # Extract file name from URL
        parsed_url = urlparse(image_url)
        image_name = os.path.basename(parsed_url.path)
        
        # Construct local file path to save the image
        save_path = os.path.join(save_dir, image_name)

        # Download and save the image
        download_image(image_url, save_path)
    else:
        print(f"Warning: Empty image URL found in row {index + 2}")

print("All images downloaded and saved successfully.")

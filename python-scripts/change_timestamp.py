import os
import csv
import re
from datetime import datetime

# Path to the CSV file
csv_file = "processed_data.csv"

# Path to the folder containing images
image_folder = "data/"

# Read the CSV and create a mapping of image_number to datetime
image_timestamps = {}
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        image_number = int(row["image_number"])
        datetime_str = row["datetime"]
        image_timestamps[image_number] = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

# Regex pattern to extract the number from the image filenames (with leading zeros)
filename_pattern = re.compile(r"r_u_cephei_(\d+)\.fit$")

# Iterate through the image files in the folder
for filename in os.listdir(image_folder):
    match = filename_pattern.match(filename)
    if match:
        image_number = int(match.group(1))  # Convert extracted number to integer to match CSV
        if image_number in image_timestamps:
            # Get the corresponding timestamp
            new_timestamp = image_timestamps[image_number]
            
            # Construct the full file path
            file_path = os.path.join(image_folder, filename)
            
            # Change the file's timestamp
            timestamp_unix = new_timestamp.timestamp()
            os.utime(file_path, (timestamp_unix, timestamp_unix))
            print(f"Updated timestamp for {filename} to {new_timestamp}")
        else:
            print(f"No matching timestamp found for {filename}")
    else:
        print(f"Filename does not match pattern: {filename}")

print("Timestamp update process complete.")

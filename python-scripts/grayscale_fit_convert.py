import os
from astropy.io import fits
import numpy as np
import csv
from datetime import datetime
import re

# Directories
input_dir = "./data/"
output_dir = "./grayscale/"
os.makedirs(output_dir, exist_ok=True)

# CSV file with timestamps
timestamp_csv = "processed_data.csv"

# Load timestamps from CSV into a dictionary
timestamps = {}
with open(timestamp_csv, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        image_number = int(row["image_number"])
        timestamps[image_number] = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")

# Process each FITS file
for filename in sorted(os.listdir(input_dir)):  # Sort to process frames in order
    if filename.endswith(".fit"):
        # Extract the image number from the filename
        match = re.match(r"r_u_cephei_(\d+)\.fit$", filename)
        if match:
            image_number = int(match.group(1))
            if image_number in timestamps:
                original_time = timestamps[image_number]
                filepath = os.path.join(input_dir, filename)

                # Open the FITS file
                with fits.open(filepath) as hdul:
                    data = hdul[0].data  # Assuming the image data is in the first HDU

                    # Print the shape of the data
                    print(f"Processing {filename}, data shape: {data.shape}")

                    # Handle 3D data by collapsing to 2D
                    if len(data.shape) == 3:
                        data = np.mean(data, axis=0)

                    # Replace NaN values with zero
                    data = np.nan_to_num(data)

                    # Normalize the data to 0-255 for image conversion
                    norm_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
                    norm_data = norm_data.astype(np.uint8)

                    # Create a new FITS file with the same data but with the original timestamp
                    output_path = os.path.join(output_dir, filename.replace(".fit", "_modified.fit"))

                    # Create a new HDU (Header Data Unit) with the image data
                    hdu = fits.PrimaryHDU(norm_data)

                    # Add the original timestamp to the header
                    hdu.header['DATE-OBS'] = original_time.isoformat()  # Standard date keyword
                    hdu.header['TIMESTAMP'] = original_time.isoformat()  # Custom timestamp keyword

                    # Write the new FITS file
                    hdu.writeto(output_path, overwrite=True)

                    # Set the file system timestamp
                    timestamp = original_time.timestamp()
                    os.utime(output_path, (timestamp, timestamp))

                    print(f"Converted {filename} to {output_path} with timestamp {original_time}.")
            else:
                print(f"No timestamp found for {filename}.")
        else:
            print(f"Filename does not match pattern: {filename}")

print("Conversion completed!")

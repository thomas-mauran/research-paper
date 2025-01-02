import os
from astropy.io import fits
import numpy as np
from datetime import datetime, timedelta
import csv

# Directories
input_dir = "./img/"
output_dir = "./grayscale"
os.makedirs(output_dir, exist_ok=True)

# Starting datetime: 24th December 2024, 18:30
start_time = datetime(2024, 12, 24, 18, 30)
frame_interval = timedelta(minutes=2)

# Calibration CSV file
calibration_file = os.path.join(output_dir, "timestamps.csv")

# Open the calibration file for writing
with open(calibration_file, mode='w', newline='') as file:

    # Process each FITS file
    for index, filename in enumerate(sorted(os.listdir(input_dir))):  # Sort to process frames in order
        if filename.endswith(".fit"):
            filepath = os.path.join(input_dir, filename)
            
            # Open the FITS file
            with fits.open(filepath) as hdul:
                data = hdul[0].data  # Assuming the image data is in the first HDU
                
                # Inspect the shape of the data
                print(f"Processing {filename}, data shape: {data.shape}")
                
                # Handle 3D data by collapsing to 2D
                if len(data.shape) == 3:
                    data = np.mean(data, axis=0)  # Take mean across the first dimension
                
                # Replace NaN values with zero
                data = np.nan_to_num(data)
                
                # Normalize the data to 0-255 for image conversion (optional if needed)
                norm_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
                norm_data = norm_data.astype(np.uint8)  # Convert to 8-bit integer
                
                # Calculate the target timestamp
                target_time = start_time + index * frame_interval
                
                # Create a new FITS file with the same data but with the timestamp in the header
                output_path = os.path.join(output_dir, filename.replace(".fit", "_modified.fit"))
                
                # Create a new HDU (Header Data Unit) with the image data
                hdu = fits.PrimaryHDU(norm_data)
                
                # Add timestamp to the header (using a custom keyword)
                hdu.header['DATE-OBS'] = target_time.isoformat()  # Standard date keyword
                hdu.header['TIMESTAMP'] = target_time.isoformat()  # Custom timestamp keyword
                
                # Write the new FITS file
                hdu.writeto(output_path, overwrite=True)
                
                # Optionally, set the file system timestamp (this is more for OS-level tracking)
                timestamp = target_time.timestamp()
                os.utime(output_path, (timestamp, timestamp))
                
                print(f"Converted {filename} to {output_path} with timestamp {target_time}.")

print(f"Conversion completed! Calibration file saved at {calibration_file}.")

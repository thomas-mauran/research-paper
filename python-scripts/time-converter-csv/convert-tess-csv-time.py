import pandas as pd
from astropy.time import Time
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Convert BJD time in a CSV file to Unix timestamp.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file')
parser.add_argument('output_file', type=str, help='Path to the output CSV file')
args = parser.parse_args()

# Load the data
input_file = args.input_file
output_file = args.output_file
data = pd.read_csv(input_file)

# Convert the BJD time to Julian Date
bjd_base = 2457000.0
data['JD'] = data['time'] + bjd_base

# Convert Julian Date to Unix timestamp
time_obj = Time(data['JD'], format='jd', scale='utc')
data['Unix_Timestamp'] = time_obj.unix  # Add new column with Unix timestamp

# Rearrange columns and drop the old JD column
data = data[['Unix_Timestamp', 'time', 'mag', 'mag_err']]

# Save to a new CSV file
data.to_csv(output_file, index=False)

print(f"Converted CSV saved as: {output_file}")

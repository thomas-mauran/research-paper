import pandas as pd
from astropy.time import Time
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Convert JD_UTC in a CSV file to UNIX timestamp.')
parser.add_argument('input_file', type=str, help='Path to the input CSV file')
parser.add_argument('output_file', type=str, help='Path to the output CSV file')
args = parser.parse_args()

# Load the data
input_file = args.input_file
output_file = args.output_file
data = pd.read_csv(input_file, delimiter=';')  # Adjust delimiter if needed

# Convert JD_UTC to UNIX timestamp
time_obj = Time(data['JD_UTC'], format='jd', scale='utc')
data['UNIX_Timestamp'] = time_obj.unix  # Add new column with UNIX timestamp

# Rearrange columns, placing UNIX_Timestamp before JD_UTC
cols = list(data.columns)
cols.insert(cols.index('JD_UTC'), 'UNIX_Timestamp')
data = data[cols]

# Save to a new CSV file
data.to_csv(output_file, index=False, sep=';')  # Use the same delimiter as the input

print(f"Converted CSV saved as: {output_file}")

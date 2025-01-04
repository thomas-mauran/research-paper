import re
import csv

# File containing the data
input_file = "conversion.txt"

# Read data from the file
with open(input_file, "r", encoding="utf-8") as file:
    data = file.read()

# Define a regular expression to extract the necessary fields
pattern = r"'(.*?)' -> '(.*?)' image (\d+)"

# Extract matches
matches = re.findall(pattern, data)

# Create a structured list for further processing
processed_data = []
for match in matches:
    file_path, sequence_file, image_number = match
    
    # Extract date and time from the file path (assumes format YYYY-MM-DD_HH-MM-SS exists in the path)
    date_time_match = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', file_path)
    if date_time_match:
        exact_date = date_time_match.group(1)  # Extract date (YYYY-MM-DD)
        exact_time = date_time_match.group(2).replace("-", ":")  # Extract time (HH:MM:SS)
        exact_datetime = f"{exact_date} {exact_time}"  # Combine date and time
    else:
        exact_datetime = "Unknown"

    processed_data.append({
        "datetime": exact_datetime,
        "sequence_file": sequence_file,
        "image_number": int(image_number)
    })

# Example output to verify results
for entry in processed_data[:10]:  # Print the first 10 entries as a sample
    print(entry)

# Save to a CSV file for analysis (optional)
output_file = "processed_data.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["datetime", "sequence_file", "image_number"])
    writer.writeheader()
    writer.writerows(processed_data)

print(f"Data saved to {output_file}")

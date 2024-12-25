import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV data into a DataFrame
data = pd.read_csv("data.csv")

# Display the first few rows
# print(data.head())

# Check for missing values
# print(data.isnull().sum())
# Count occurrences of each type
type_counts = data['type'].value_counts()

# Pie chart
plt.figure(figsize=(8, 6))
type_counts.plot.pie(autopct='%1.1f%%', startangle=140, cmap='Pastel1')
plt.ylabel("")
plt.title("Supernova Type Distribution")
plt.show()
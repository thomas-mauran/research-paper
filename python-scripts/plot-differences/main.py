import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
ucep = pd.read_csv('./Measurements.csv', delimiter=';')
ucep = ucep[0:263]

tess = pd.read_csv('./tess.csv')
# tess_trimmed = tess[38:102]
tess_trimmed = tess[3118:3192]


# Inspect the data
print(ucep.head())
print(ucep.columns)

# Extract relevant columns
ucep_time = ucep['JD_UTC']
for i in range(len(ucep_time)):
    ucep_time[i] = ucep_time[i] - 2460669

ucep_mag = ucep['Source_AMag_T1']

for i in range(len(ucep_mag)):
    ucep_mag[i] = ucep_mag[i] - 0.5

tess_time = tess['time']

for i in range(len(tess_time)):
    tess_time[i] = tess_time[i] - 2766.46

tess_mag = tess['mag']

# Trim TESS data to match U Cephei's timeframe
ucep_start = ucep_time.min()
ucep_end = ucep_time.max()

# Update TESS variables after trimming
tess_time = tess_trimmed['time']
tess_mag = tess_trimmed['mag']

# Convert U Cephei flux to magnitude
# ucep_mag = -2.5 * np.log10(ucep_flux) + 7

# Interpolate U Cephei data to match TESS times
ucep_interp_mag = np.interp(tess_time, ucep_time, ucep_mag)

# Calculate the difference in magnitude
mag_diff = ucep_interp_mag - tess_mag

# Plot the light curves and their difference
plt.figure(figsize=(12, 8))

# Split light curves in 2 graphs 
# Plot TESS light curve
# plt.subplot(3, 1, 1)
# plt.plot(tess_time, tess_mag, label='TESS Magnitude', color='blue')
# plt.gca().invert_yaxis()  # Magnitudes are inverted (brighter is lower)
# plt.ylabel('Magnitude')
# plt.title('TESS Light Curve')
# plt.legend()

# # Plot U Cephei light curve
# plt.subplot(3, 1, 2)
# plt.plot(ucep_time, ucep_mag, label='U Cephei Magnitude', color='orange')
# plt.gca().invert_yaxis()
# plt.ylabel('Magnitude')
# plt.title('U Cephei Light Curve')
# plt.legend()

plt.plot(tess_time, tess_mag, label='TESS Data', color='blue', linestyle='-', marker='o', markersize=4)
plt.plot(tess_time, ucep_interp_mag, label='Personnal data from Montpellier', color='orange', linestyle='--', marker='x', markersize=4)

# Customize plot
plt.gca().invert_yaxis()  # Magnitudes are inverted (brighter is lower)
plt.xlabel('Time')
plt.ylabel('Magnitude')
plt.title('U Cephei light curve comparaison from TESS and personal data')
plt.legend()

plt.tight_layout()
plt.show()

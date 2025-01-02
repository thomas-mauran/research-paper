import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
ucep = pd.read_csv('./ucep.csv', delimiter=';')
tess = pd.read_csv('./tess.csv')

# Inspect the data
print(ucep.head())  
print(ucep.columns)

# Extract relevant columns
ucep_time = ucep['JD_UTC']  # Time from ucep.csv
ucep_flux = ucep['rel_flux_T1']  # Relative flux for target star

tess_time = tess['time']  # Time from tess.csv
tess_mag = tess['mag']  # Magnitude from TESS

# Trim TESS data to match U Cephei's timeframe
ucep_start = ucep_time.min()
ucep_end = ucep_time.max()
tess_trimmed = tess[3130:3185]

# Update TESS variables after trimming
tess_time = tess_trimmed['time']
tess_mag = tess_trimmed['mag']

# Convert U Cephei flux to magnitude
ucep_mag = -2.5 * np.log10(ucep_flux)

# Interpolate U Cephei data to match TESS times
ucep_interp_mag = np.interp(tess_time, ucep_time, ucep_mag)

# Calculate the difference in magnitude
mag_diff = ucep_interp_mag - tess_mag

# Plot the light curves and their difference
plt.figure(figsize=(12, 8))

# Plot TESS light curve
plt.subplot(3, 1, 1)
plt.plot(tess_time, tess_mag, label='TESS Magnitude', color='blue')
plt.gca().invert_yaxis()  # Magnitudes are inverted (brighter is lower)
plt.ylabel('Magnitude')
plt.title('TESS Light Curve')
plt.legend()

# Plot U Cephei light curve
plt.subplot(3, 1, 2)
plt.plot(ucep_time, ucep_mag, label='U Cephei Magnitude', color='orange')
plt.gca().invert_yaxis()
plt.ylabel('Magnitude')
plt.title('U Cephei Light Curve')
plt.legend()

# Plot the difference
plt.subplot(3, 1, 3)
plt.plot(tess_time, mag_diff, label='Difference (U Cephei - TESS)', color='green')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Magnitude Difference')
plt.title('Difference Between Light Curves')
plt.legend()

plt.tight_layout()
plt.show()

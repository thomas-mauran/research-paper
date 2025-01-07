import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
ucep = pd.read_csv('./Measurements-good-time.csv', delimiter=';')
ucep = ucep[0:263]

tess = pd.read_csv('./tess-2024-good.csv')

# Extract relevant columns and adjust time/magnitude
ucep_time = ucep['UNIX_Timestamp']
ucep_mag = ucep['Source_AMag_T1']

tess_time = tess['Unix_Timestamp']
tess_mag = tess['mag']

# Check the time ranges for overlap
print(f"U Cephei time range: {ucep_time.min()} to {ucep_time.max()}")
print(f"TESS time range: {tess_time.min()} to {tess_time.max()}")

# Normalize both U Cephei and TESS times
ucep_normalized_time = ucep_time - ucep_time.min()
tess_normalized_time = tess_time - tess_time.min()


# Interpolate U Cephei magnitudes to match TESS times
ucep_interp_mag = np.interp(tess_normalized_time, ucep_normalized_time, ucep_mag)

plt.plot(tess_normalized_time, tess_mag, label='TESS Data', color='blue', linestyle='-', marker='o', markersize=4)
plt.plot(tess_normalized_time, ucep_interp_mag, label='Personal Data from Montpellier', color='orange', linestyle='--', marker='x', markersize=4)

# Customize plot
plt.gca().invert_yaxis()  # Magnitudes are inverted (brighter is lower)
plt.xlabel('Time')
plt.ylabel('Magnitude')
plt.title('U Cephei Light Curve Comparison from TESS and Personal Data')
plt.legend()

# Plot TESS light curve
# plt.subplot(3, 1, 1)
# plt.plot(tess_normalized_time, tess_mag, label='TESS Magnitude', color='blue', marker='o', markersize=4)
# plt.gca().invert_yaxis()  # Magnitudes are inverted (brighter is lower)
# plt.ylabel('Magnitude')
# plt.title('TESS Light Curve')
# plt.legend()

# # Plot U Cephei light curve
# plt.subplot(3, 1, 2)
# plt.plot(tess_normalized_time, ucep_interp_mag, label='Interpolated U Cephei Magnitude', color='orange', marker='x', markersize=4)
# plt.gca().invert_yaxis()
# plt.ylabel('Magnitude')
# plt.title('Interpolated U Cephei Light Curve')
# plt.legend()



plt.tight_layout()
plt.show()


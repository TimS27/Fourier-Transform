import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fourioso
import scipy.constants

# Reading CSV file
data_photodiode = pd.read_csv("photodiode-on-blocked-1MS-500MSs-200microseconds-1mV.csv")   # Osci noise when photodiode is connected
data_nothing = pd.read_csv("nothing-connected-1MS-500MSs-200microseconds-1mV.csv")  # Osci noise when nothing is connected
 
# Converting column data to list then array
#t = np.array(data['time'].tolist())
#voltage = np.array(data['voltage'].tolist())

# Get smaller sample dataset by taking only every 10th entry of the array via [0::10]
t = np.array(data_photodiode['time'].tolist())
voltage = np.array(data_photodiode['voltage'].tolist())

# Time difference between neigboring data points, e.g. inverse sampling rate
#delta_t = t[1]-t[0]
#print(delta_t)
# Measurement duration
#duration = t[len(t) - 1] - t[0]
#print(duration)

t_span =  t[len(t) - 1] - t[0]
max_tspacing = np.abs(np.diff(t).max())

n_points, t_spacing = fourioso.n_spacing(max_tspacing, t_span) # automatically chooses efficient n_points
t_new = fourioso.get_axis(n_points, t_spacing) # frequencies centered around 0
#nu_THz = nu / 1e12  # calculate new frequency axis in THz

# Interpolate time domain data to new frequency axis
t_interpolatable = t_new + t[0] - t_new[0]  # get new frequency axis in data range for interpolation
voltage_interpolated = np.interp(t_interpolatable, t, voltage)


nu, data_transformed = fourioso.transform(t_new, voltage_interpolated)
#t_fs = t * 1e15 # calculate time axis in fs

#data_backtransformed = fourioso.itransform(nu, data_transformed, return_axis=False)
#print(data_transformed)

# simple fft for comparison
#simple_fft = np.fft.fft(voltage)
#simple_nu = np.fft.fftfreq(t.shape[-1])

plt.figure()
plt.plot(t, voltage, '-o', markersize=2)
#plt.xlim(-1e-12, 1e-12)
plt.title('Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.show()
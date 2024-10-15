import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fourioso
import scipy.constants

# Reading CSV file
data = pd.read_csv("photodiode-on-blocked-1MS-500MSs-200microseconds-1mV.csv")
 
# Converting column data to list then array
t = np.array(data['time'].tolist())
voltage = np.array(data['voltage'].tolist())

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

data_backtransformed = fourioso.itransform(nu, data_transformed, return_axis=False)

#print(data_transformed)


plt.figure()
plt.plot(nu, data_transformed, '-o', markersize=2)
#plt.xlim(-1e-12, 1e-12)
plt.title('Time domain electric field')
plt.xlabel('Time [s]')
plt.ylabel('Electric field')
plt.show()

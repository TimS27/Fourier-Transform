import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fourioso

# reading CSV file
data = pd.read_csv("Spectrum-5mm-Fused-Silica.csv")
 
# converting column data to list
wavelength = np.array(data['wavelength'].tolist())
counts = np.array(data['counts'].tolist())
 
# printing list data
#print('Wavelegths:', wavelength)
#print('Counts:', counts)
#print(type(np.array(wavelength)))

# Interpolate

x = np.linspace(736.24261 ,1321.4418, 10000)
xp = wavelength
fp = counts
spectrum_interpolated = np.interp(x, xp, fp)

#plt.plot(x, spectrum_interpolated)
#plt.ylabel('counts')
#plt.show()

#plt.plot(wavelength, counts)
#plt.show()

t_span = 50
max_tspacing = 0.1

#n_points, t_spacing = fourioso.n_spacing(max_tspacing, t_span) # automatically chooses efficient n_points
#t = fourioso.get_axis(n_points, t_spacing)

#data = np.exp(-t**2)

nu, data_transformed = fourioso.transform(wavelength, counts)
# you can also separate this:
#   nu = fourioso.transform(t)
#   data_transformed = fourioso.transform(t, data, return_axis=False)

data_backtransformed = fourioso.itransform(nu, data_transformed, return_axis=False)

plt.figure()
plt.plot(wavelength, data, 'x')
plt.plot(wavelength, data_backtransformed, '+')
plt.show()

#DOESNT WORK BECAUSE DATA HAS TO BE INTERPOLATED TO NEW AXIS
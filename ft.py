import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants
import scipy.signal
import obspy.signal.filter
import fourioso

# reading CSV file
data = pd.read_csv("Spectrum-5mm-Fused-Silica.csv")
 
# converting column data to list then array
wavelengths = np.array(data['wavelength'].tolist())
counts = np.array(data['counts'].tolist())

# covert wavelengths to frequencies
frequencies = scipy.constants.c / (wavelengths * 1e-9)
# intensity to field
field = np.sqrt(counts)

frequencies_reversed = frequencies[::-1]
field_reversed = field[::-1]

nu_span =  frequencies_reversed[len(frequencies_reversed)-1] - frequencies_reversed[0]
max_nuspacing = np.abs(np.diff(frequencies_reversed).max())
#print(nu_span)
#print(nu_span/max_nuspacing)

#nu_span = frequencies[0] - frequencies[len(frequencies)-1]
#max_nuspacing = np.abs(np.diff(frequencies).max())

n_points, nu_spacing = fourioso.n_spacing(max_nuspacing, nu_span) # automatically chooses efficient n_points
nu = fourioso.get_axis(n_points, nu_spacing)
#print(nu/1e12)
#print(frequencies)

# Test if arrax x is monotonic and can therefore be interpolated with np.interp
def monotonic(x):
    dx = np.diff(x)
    return np.all(dx <= 0) or np.all(dx >= 0)

#print(monotonic(frequencies_reversed))

# Interpolate spectral data to new frequency axis
spectrum_interpolated = np.interp(nu, frequencies_reversed, field_reversed)
#print(frequencies_reversed)
print(type(field_reversed[1]))
print(spectrum_interpolated[500])

t, data_transformed = fourioso.itransform(nu, spectrum_interpolated)
# you can also separate this:
#   nu = fourioso.transform(t)
#   data_transformed = fourioso.transform(t, data, return_axis=False)

data_backtransformed = fourioso.transform(t, data_transformed, return_axis=False)

intensity_envelope = obspy.signal.filter.envelope(data_transformed**2)

# Determine FWHM in fs
def get_fwhm(t, envelope):
  It = abs(envelope)**2
  spline = scipy.interpolate.UnivariateSpline(t, It-np.max(It)/2, s=0)

  try:
    r1, r2 = spline.roots()
    return r2-r1
  except ValueError:
    return np.nan

fwhm = get_fwhm(t, data_transformed) * 1e15

#print("FWHM: " + str(fwhm) + " fs")

plt.figure()
plt.plot(t, data_transformed, '+')
#plt.show()







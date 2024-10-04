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
 
nu_span = frequencies[0] - frequencies[len(frequencies)-1]
max_nuspacing = np.abs(np.diff(frequencies).max())

n_points, nu_spacing = fourioso.n_spacing(max_nuspacing, nu_span) # automatically chooses efficient n_points
nu = fourioso.get_axis(n_points, nu_spacing)

# Interpolate spectral data to new frequency axis
spectrum_interpolated = np.interp(nu, frequencies, field)

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

print("FWHM: " + str(fwhm) + " fs")

plt.figure()
plt.plot(t, data_transformed**2, '+')
plt.show()







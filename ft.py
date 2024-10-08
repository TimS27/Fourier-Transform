import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants
import scipy.signal
import obspy.signal.filter
import fourioso

# Reading CSV file
data = pd.read_csv("Spectrum-5mm-Fused-Silica.csv")
 
# Converting column data to list then array
wavelengths = np.array(data['wavelength'].tolist())
counts = np.array(data['counts'].tolist())

# Covert wavelengths to frequencies
frequencies = scipy.constants.c / (wavelengths* 1e-9)
# Intensity to field
field = np.sqrt(counts)

# Reverse frequencies and field because monotonically increasing xo is needed for interpolation with numpy.interp
frequencies_reversed = frequencies[::-1]
field_reversed = field[::-1]


nu_span =  frequencies_reversed[len(frequencies_reversed)-1] - frequencies_reversed[0]
max_nuspacing = np.abs(np.diff(frequencies_reversed).max())

n_points, nu_spacing = fourioso.n_spacing(max_nuspacing, nu_span) # automatically chooses efficient n_points
nu = fourioso.get_axis(n_points, nu_spacing)


# Test if arrax x is monotonic and can therefore be interpolated with np.interp
def monotonic(x):
    dx = np.diff(x)
    return np.all(dx <= 0) or np.all(dx >= 0)

# Check if strictly increasing
#print(np.all(np.diff(frequencies_reversed) > 0))


# Interpolate spectral data to new frequency axis
nu_interpolatable = nu + frequencies_reversed[0] - nu[0]  # get new frequency axis in data range for interpolation
spectrum_interpolated = np.interp(nu_interpolatable, frequencies_reversed, field_reversed)


t, data_transformed = fourioso.itransform(nu, spectrum_interpolated)
# you can also separate this:
#   nu = fourioso.transform(t)
#   data_transformed = fourioso.transform(t, data, return_axis=False)

data_backtransformed = fourioso.transform(t, data_transformed, return_axis=False)

# Optionally calculate envelope via Hilbert transform
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
plt.plot(t, data_transformed**2, '-o', markersize=2)
plt.xlim(-1e-12, 1e-12)
plt.title('Time domain intensity')
plt.xlabel('Time [s]')
plt.ylabel('Intensity')
plt.show()







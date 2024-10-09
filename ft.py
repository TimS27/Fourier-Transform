import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants
import scipy.signal
import fourioso
#import obspy.signal.filter

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
nu = fourioso.get_axis(n_points, nu_spacing) # frequencies centered around 0
nu_THz = nu / 1e12  # calculate new frequency axis in THz

# Test if arrax x is monotonic and can therefore be interpolated with np.interp
#def monotonic(x):
#    dx = np.diff(x)
#    return np.all(dx <= 0) or np.all(dx >= 0)

# Check if strictly increasing
#print(np.all(np.diff(frequencies_reversed) > 0))


# Interpolate spectral data to new frequency axis
nu_interpolatable = nu + frequencies_reversed[0] - nu[0]  # get new frequency axis in data range for interpolation
spectrum_interpolated = np.interp(nu_interpolatable, frequencies_reversed, field_reversed)


t, data_transformed = fourioso.itransform(nu, spectrum_interpolated)
# you can also separate this:
#   nu = fourioso.transform(t)
#   data_transformed = fourioso.transform(t, data, return_axis=False)
t_fs = t * 1e15 # calculate time axis in fs

data_backtransformed = fourioso.transform(t, data_transformed, return_axis=False)

# Optionally calculate envelope via Hilbert transform
#intensity_envelope = obspy.signal.filter.envelope(data_transformed**2)


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


# Plot spectrum, electric field, and intensity in one figure
fig, axs = plt.subplots(3, figsize=(8,14), gridspec_kw={'hspace': 0.5, 'wspace': 0.2})
fig.suptitle('Spectrum, Electric Field, and Intensity via Fourier Transform')

axs[0].plot(nu_THz, spectrum_interpolated, 'o', markersize=2)
axs[0].set_title('Spectrum')
axs[0].set_xlabel('Frequency span [THz]') # frequencies
axs[0].set_ylabel('Spectrum [counts]')

axs[1].plot(t_fs, data_transformed, '-o', markersize=2)
axs[1].set_xlim(-1000, 1000)  # restrict x axis to puls 
axs[1].set_title('Time domain electric field')
axs[1].set_xlabel('Time [fs]')
axs[1].set_ylabel('Electric field')
fwhm_text = "FWHM: " + str(round(fwhm, 2)) + " fs"
axs[1].text(250, -0.5e16, fwhm_text, fontsize=12)

axs[2].plot(t_fs, data_transformed**2, '-o', markersize=2)
axs[2].set_xlim(-1000, 1000)
axs[2].set_title('Time domain intensity')
axs[2].set_xlabel('Time [fs]')
axs[2].set_ylabel('Intensity')

plt.show()

# Simple plotting option
'''
plt.figure()
plt.plot(t, data_transformed, '-o', markersize=2)
plt.xlim(-1e-12, 1e-12)
plt.title('Time domain electric field')
plt.xlabel('Time [s]')
plt.ylabel('Electric field')
plt.show()
'''
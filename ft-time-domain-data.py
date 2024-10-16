import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV data
# Reading CSV file
data_photodiode = pd.read_csv("photodiode-on-blocked-1MS-2500MSs-20microseconds-1mV+fft.csv")   # Osci noise when photodiode is connected
data_nothing = pd.read_csv("nothing-connected-1MS-500MSs-200microseconds-1mV.csv")  # Osci noise when nothing is connected

# Converting column data to list then array
time = np.array(data_photodiode['time'].tolist())
voltage = np.array(data_photodiode['voltage'].tolist())

# Calculate the time resolution (Δt) from the time data
dt = time[1] - time[0]  # Assume uniform time steps
Fs = 1 / dt  # Sampling frequency (Hz)

# Number of samples
N = len(time)
    
# Perform the Fourier Transform on the voltage data
voltage_fft = np.fft.fft(voltage)
    
# Calculate the frequency axis
freqs = np.fft.fftfreq(N, dt)
#print(freqs[500000])   # highest frequency is 1.25 GHz
    
# Take the absolute value to get the magnitude of the spectrum
magnitude = np.abs(voltage_fft) / N  # Normalize the magnitude
    
# Since FFT returns both positive and negative frequencies, we only take the positive half
half_N = N // 2
freqs = freqs[:half_N]  # Only keep the positive frequencies
magnitude = magnitude[:half_N] * 2  # Double the magnitude to account for the removed half

# Calculate power (assuming a 50-ohm system and convert voltage to power in mW)
# Power = (Magnitude of FFT)^2 / 50 to get power in watts, then convert to mW (x 1000)
power_mW = (magnitude ** 2) / 50 * 1000
    
# Convert the power to dBm
power_dBm = 10 * np.log10(power_mW)

#print(freqs[1]-freqs[0])

# Plot the frequency spectrum in dBm
plt.figure(figsize=(10, 6))
plt.plot(freqs, power_dBm, label='Spectrum in dBm')  # Use this to get rid of (freqs[1000:], magnitude[1000:], label='Magnitude Spectrum')
plt.title('Frequency Spectrum from Oscilloscope Data (dBm) @ "20 kHz RBW"')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dBm)')
plt.grid(True)
plt.legend()
plt.show()

'''
# Change to this to plot magnitude instead
plt.plot(freqs, magnitude, label='Magnitude Spectrum')
plt.title('Frequency Spectrum from Oscilloscope Data')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (V/Hz)')
'''
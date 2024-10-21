import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the CSV data
# Reading CSV file
data_photodiode = pd.read_csv("data/photodiode-on-blocked-1MS-2500MSs-20microseconds-1mV+fft.csv")   # Osci noise when photodiode is connected
data_nothing = pd.read_csv("data/nothing-connected-1MS-2500MSs-20microseconds-1mV+fft.csv")  # Osci noise when nothing is connected

# Converting column data to list then array
time1 = np.array(data_nothing['time'].tolist())
voltage1 = np.array(data_nothing['voltage'].tolist())

# Add modulation of 50 microWatts and 100 MHz to signal (beware of factor 2 pi, because cos uses angular frequency and factor 0.5 because cos^2 has 2x frequency)
#voltage_modulated = np.sqrt(50e-6 * 50) * ((np.cos(100e6 * 2 * 0.5 * np.pi * time1) ** 2))
power = 50e-6
responsivity = 1
gain = 1e4
voltage = power * responsivity * gain * 0.01
voltage_modulated = voltage1 + voltage * (np.cos(100e6 * np.pi * time1) ** 2)

#time2 = np.array(data_nothing['time'].tolist())
#voltage2 = np.array(data_nothing['voltage'].tolist())

# Calculate the time resolution (Δt) from the time data
dt = time1[1] - time1[0]  # Assume uniform time steps
Fs = 1 / dt  # Sampling frequency (Hz)

# Number of samples
N = len(time1)
    
# Perform the Fourier Transform on the voltage data
voltage1_fft = np.fft.fft(voltage1)
#voltage2_fft = np.fft.fft(voltage2)
    
# Calculate the frequency axis
freqs = np.fft.fftfreq(N, dt)
#print(freqs[500000])   # highest frequency is 1.25 GHz
    
# Take the absolute value to get the magnitude of the spectrum
magnitude1 = np.abs(voltage1_fft) / N  # Normalize the magnitude
#magnitude2 = np.abs(voltage2_fft) / N  
    
# Since FFT returns both positive and negative frequencies, we only take the positive half
half_N = N // 2
freqs = freqs[:half_N]  # Only keep the positive frequencies
magnitude1 = magnitude1[:half_N] * 2  # Double the magnitude to account for the removed half
#magnitude2 = magnitude2[:half_N] * 2

# Calculate power (assuming a 50-ohm system and convert voltage to power in mW)
# Power = (Magnitude of FFT)^2 / 50 to get power in watts, then convert to mW (x 1000)
power1_mW = (magnitude1 ** 2) / 50 * 1000
#power2_mW = (magnitude2 ** 2) / 50 * 1000
    
# Convert the power to dBm
power1_dBm = 10 * np.log10(power1_mW)
#power2_dBm = 10 * np.log10(power2_mW)

#print(freqs[1]-freqs[0])

# Plot the frequency spectrum in dBm
plt.figure(figsize=(10, 6))
plt.plot(time1, voltage1, label='Oscilloscope dark noise')  # Use this to get rid of (freqs[1000:], magnitude[1000:], label='Magnitude Spectrum')
plt.plot(time1, voltage_modulated, label='Photodiode dark noise + 0.5 \u03bcW signal')
plt.title('0.5\u03bcW 100 MHz modulated signal + photodiode dark noise')   #Photodiode- vs. oscilloscope dark noise (dBm) @ "20 kHz RBW"
plt.xlabel('Time [s]')
#plt.xlabel('Frequency (Hz)')
plt.ylabel('Voltage [V]')
#plt.ylabel('Power (dBm)')
plt.xlim(0, 5e-8)
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
# Fourier Transform
This repository contains.
>- ft.py: an examplary implementation of a numerical Fourier transform that improves upon the fft/ifft functions supplied by numpy & scipy. In this case it takes spectral data.
>- ft-time-domain-data.py: an examplary implementation of a numerical FT to calculate the noise spectrum corresponding to time domain oscilloscope measurements.
<br>
ft.py is based on the Fourioso module: https://gitlab.com/leberwurscht/fourioso
and considers:
>- correct scaling of the temporal and frequency axes
>- correct scaling of the input and output amplitude (for the Parsival and Plancherel theorems to apply)
>- for FFT, the frequency and time axes start at zero, which is often not wanted (having zero at the center of the axis, with negative frequencies/times on the left and positive frequencies/times at the right, is more convenient)
<br>
The code in ft.py reads a .csv file that contains spectral counts in the first row and wavelengths in the second row. It then calculates the Fourier transform with the considerations above.
Finally the spectrum, electric field, and intensity are plotted and the FWHM of the electric field/intensity is given.
<br>
<br>
<!--![spectrum_electric-field_intensity](https://github.com/TimS27/Fourier-Transform/blob/main/spectrum_electric-field_intensity.png)-->
<img src="spectrum_electric-field_intensity.png" width="700">
<br>
<br>

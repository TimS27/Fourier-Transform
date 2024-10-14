import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.constants

# Reading CSV file
data = pd.read_csv("Spectrum-5mm-Fused-Silica.csv")
 
# Converting column data to list then array
wavelengths = np.array(data['wavelength'].tolist())
counts = np.array(data['counts'].tolist())
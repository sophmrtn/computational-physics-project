"""
INITIAL REPRESENTATION OF THE DATA FROM CSV FILE & PLOTTING HISTOGRAMS
21/11/18
SOPHIE MARTIN
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import functions as funcs

data = funcs.import_data()
# Plot histogram of the times, error is calculated using root(N)
time_freq, time_edges = np.histogram(data['t'], bins=300, normed=True)
time_centers = 0.5*(time_edges[1:]+time_edges[:-1])
widths_time= time_edges[1:]-time_edges[:-1]
error_time = np.sqrt(time_freq)/max(time_freq)

# Plot histogram for the uncertainty spread
sig_freq, sig_edges = np.histogram(data['sigma'], bins=300, normed=True)
sig_centers = 0.5*(sig_edges[1:]+sig_edges[:-1])
widths_sig = sig_edges[1:]-sig_edges[:-1]
error_sig = np.sqrt(sig_freq)


# p0 is the initial guess for the fitting coefficients (t, sigma) for fm
p0_f = [1, 1]
coeff_fm, var_matrix_fm = curve_fit(funcs.fm_function, time_centers, time_freq, p0=p0_f)
hist_fit_fm = funcs.fm_function(time_centers, *coeff_fm)

# p0 is the initial guess for the fitting coefficients (mu and sigma above)
p0 = [0, 2]
coeff, var_matrix = curve_fit(funcs.gauss, time_centers, time_freq, p0=p0)
mu = coeff[0]
sigma = coeff[1]
# Get the fitted curve
hist_fit = funcs.gauss(time_centers, *coeff)



# Plot distributions and gaussian/fm fit to the time spread
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,15))
fig.subplots_adjust(hspace=0.5)
ax1.bar(time_centers, time_freq, width=widths_time, color='orange',label='data')
ax1.plot(time_centers, hist_fit, label='Gaussian Fit', lw=1, color='red')
ax1.plot(time_centers, hist_fit_fm, label='F$_m$(t) Fit', lw=1, color='purple')
ax1.set_ylabel('Number of entries')
ax1.set_xlabel('Time ($p$s)')
ax1.set_title('Histogram of times measured')
ax1.legend()
ax1.grid()

ax2.bar(sig_centers, sig_freq, width=widths_sig, color='blue')
ax2.set_ylabel('Number of entries')
ax2.set_xlabel('$\sigma$ ($p$s)')
ax2.set_title('Histogram of errors on times')
ax2.grid()

plt.figure()
plt.plot(data['t'], data['sigma'], '.')
plt.title('No correlation between t and sigma')
plt.grid()

plt.figure()
plt.bar(time_centers, time_freq, width=widths_time, color='orange',label='data')
plt.plot(time_centers, hist_fit_fm, label='F$_m$(t) Fit', lw=1, color='purple')
plt.ylabel('Number of entries')
plt.xlabel('$\sigma$ ($p$s)')
plt.grid()
plt.title('Histogram of errors on times with F$_m$(t) scipy fit')
plt.show()

print('Gauss Mean t: ', mu, 'Gauss Std dev: ', sigma,
      'Fm sigma: ', coeff_fm[1], 'Fm tau: ', coeff_fm[0], 'Fm sigma: ', coeff_fm[1])
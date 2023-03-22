import numpy as np

# Generate a discrete sinusoidal signal with additive noise
N = 2000                                      # Number of measurements (21 cycles)
sampling_freq = 1000                          # Sampling frequency, in Hz
t = np.array(range(N))/sampling_freq          # Time array, in seconds
f = 10.5                                      # Signal frequency in Hz
A = 2                                         # Signal amplitude
phi = np.pi/4                                 # Signal phase
w = np.random.normal(scale=0.1, size=len(t))  # Random noise
y = A*np.cos(2*np.pi*f*t + phi) + w           # Sinusoid array

# Compute DFT component
N_zp = N*2           # considering N zeros added to signal
df = sampling_freq/N_zp
freq = f;            # expected frequency in Hz
k = np.round(freq/df)
X = 0;
for n in range(N):   # zeros do not need to be added
  X += y[n] * np.exp(-2j * np.pi * k * n / N_zp)

# Estimate amplitude and phase at peak frequency
A_est = 2 * np.abs(X) / N             # Estimated amplitude
phi_est = np.arctan2(X.imag,X.real)   # Estimated phase

print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est:.4f}; Error: {100*(A_est-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est:.4f}; Error: {100*(phi_est-phi)/phi:.2f}%')

# Second approach, at any given frequency
X_f = 0
for n in range(N):   # zeros do not need to be added
  X_f += y[n] * np.exp(-2j * np.pi * freq * n / sampling_freq)

# Estimate amplitude and phase at peak frequency
A_est_f = 2 * np.abs(X_f) / N               # Estimated amplitude
phi_est_f = np.arctan2(X_f.imag,X_f.real)   # Estimated phase

print('Second approach:')
print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est_f:.4f}; Error: {100*(A_est_f-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est_f:.4f}; Error: {100*(phi_est_f-phi)/phi:.2f}%')
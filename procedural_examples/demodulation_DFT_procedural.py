import numpy as np

# Generate a discrete sinusoidal signal with noise
N = 1000                                      # Number of measurements (10 cycles)
sampling_freq = 1000                          # Sampling frequency, in Hz
t = np.array(range(N))/sampling_freq          # Time array in seconds
f = 10                                        # Signal frequency in Hz
A = 2                                         # Signal amplitude
phi = np.pi/4                                 # Signal phase
w = np.random.normal(scale=0.1, size=len(t))  # Random noise
y = A*np.cos(2*np.pi*f*t + phi) + w

# Compute DFT component
df = sampling_freq/N
freq = 10;            # expected frequency in Hz
k = np.round(freq/df)
X = 0;
for n in range(N):
  X += y[n] * np.exp(-2j * np.pi * k * n / N)

# Estimate amplitude and phase at peak frequency
A_est = 2 * np.abs(X) / N           # Estimated amplitude
phi_est = np.arctan2(X.imag,X.real) # Estimated phase

print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est:.4f}; Error: {100*(A_est-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est:.4f}; Error: {100*(phi_est-phi)/phi:.2f}%')
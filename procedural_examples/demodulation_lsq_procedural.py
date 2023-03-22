import numpy as np

# Generate a discrete sinusoidal signal with additive noise
N = 1000                                      # Number of measurements
sample_freq = 1000                            # Sample frequency, in Hz
t = np.array(range(N))/sample_freq            # Time array, in seconds
f = 10                                        # Signal frequency in Hz
A = 2                                         # Signal amplitude
phi = np.pi/4                                 # Signal phase
w = np.random.normal(scale=0.1, size=len(t))  # Random noise
y = A*np.sin(2*np.pi*f*t + phi) + w           # Sinusoid array

# Compute H
col1 = np.sin(2 * np.pi * f * t)
col2 = np.cos(2 * np.pi * f * t)
col3 = np.ones(t.shape)
H = np.column_stack((col1, col2, col3))

# Compute the pseudo-inverse of H
pinvH = np.linalg.pinv(H)

# Find x_lsq = pinvH * y
x_lsq = np.matmul(pinvH,y)

# Print the estimated parameters
A_est = np.sqrt(x_lsq[0]**2 + x_lsq[1]**2)  # Estimated amplitude
phi_est = np.arctan2(x_lsq[1],x_lsq[0])     # Estimated phase
print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est:.4f}; Error: {100*(A_est-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est:.4f}; Error: {100*(phi_est-phi)/phi:.2f}%')
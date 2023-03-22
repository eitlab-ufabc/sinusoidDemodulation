import numpy as np

# Generate a discrete sinusoidal signal with noise
N = 1000                                      # Number of measurements (aprox. 21 cycles)
sampling_freq = 1000                          # Sampling frequency, in Hz
t = np.array(range(N))/sampling_freq
f = 10.555                                    # Signal frequency in Hz
A = 2                                         # Signal amplitude
phi = np.pi/4                                 # Signal phase
w = np.random.normal(scale=0.1, size=len(t))  # Random noise
y = A*np.cos(2*np.pi*f*t + phi) + w           # Sinusoid array

# Apply Hamming window to the signal
window = [(0.54 + 0.46*np.cos(2 * np.pi * (n-(N-1)/2) / (N-1)))  for n in range(N)]
yw = y * window

# Find DFT peak
freq = 10             # initial guess
step = 0.2
A_est = -np.inf
f_max = 0
phi_est = 0
for dec in range(4):
  for f_idx in np.arange(freq-10*step, freq+10*step, step):
    X_f = 0
    for n in range(N):
      X_f += yw[n] * np.exp(-2j * np.pi * f_idx * n / sampling_freq)
    ampl = 2 * np.abs(X_f) / (N*np.mean(window))
    if ampl > A_est:
      A_est = ampl;
      freq = f_idx
      phi_est = np.arctan2(X_f.imag,X_f.real)
  step = step / 10

print(f'Real frequency: {f:.4f}; Estimated peak frequency = {freq:.4f}; Error: {100*(freq-f)/f:.2f}%')
print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est:.4f}; Error: {100*(A_est-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est:.4f}; Error: {100*(phi_est-phi)/phi:.2f}%')
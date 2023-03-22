import numpy as np

# Generate a discrete sinusoidal signal with noise
N = 1000              # Number of measurements (aprox. 21 cycles)
sampling_freq = 1000  # Sampling frequency, in Hz
t = np.array(range(N))/sampling_freq
f = 10.555            # Signal frequency in Hz
A = 2                 # Signal amplitude
phi = np.pi/4         # Signal phase
c = 0.1               # Signal offset
y = A*np.sin(2*np.pi*f*t + phi) + c + np.random.normal(scale=0.1, size=len(t))

#   initial guess
[Ao, fo, phio, co] = [2.5, 11, 0.0, 0.0]

nIterMax = 300        # maximum number of iterations
step_size = 1         # can be reduced to improve stability
last_error = np.inf
for idx in range(nIterMax):
  # Compute Ho and so
  #   partial derivatives
  thetas = 2 * np.pi * fo * t
  partialA = np.sin(thetas) * np.cos(phio) + np.cos(thetas) * np.sin(phio)
  partialf = ( Ao * np.cos(thetas) * 2 * np.pi * t * np.cos(phio) 
              - Ao * np.sin(thetas) * 2 * np.pi * t * np.sin(phio) )
  partialPhi = -Ao * np.sin(thetas) * np.sin(phio) + A * np.cos(thetas) * np.cos(phio)
  partialC = np.ones(t.shape)

  Ho = np.column_stack((partialA, partialf, partialPhi, partialC))
  so =  Ao * np.sin(2 * np.pi * fo * t + phio) + co - np.matmul(Ho,[Ao, fo, phio, co])

  # Compute the pseudo-inverse of Ho
  pinvHo = np.linalg.pinv(Ho)

  # Find x_lsq = pinvHo * (y - so)
  x_lsq = np.matmul(pinvHo,(y-so))
  
  # Update current estimate
  [Ao, fo, phio, co] = [Ao, fo, phio, co] + step_size*(x_lsq-[Ao, fo, phio, co] )

  # Interrupt loop if converged
  error = np.linalg.norm( y - (Ao * np.sin(2 * np.pi * fo * t + phio) + co) )
  if np.abs(error - last_error)<1e-10:
    break
  last_error = error

# Print the estimated parameters
[A_est, freq, phi_est, c_est] = x_lsq
print(f'Real frequency: {f:.4f}Hz; Estimated peak frequency = {freq:.4f}Hz; Error: {100*(freq-f)/f:.2f}%')
print(f'Real amplitude: {A:.4f}; Estimated amplitude: {A_est:.4f}; Error: {100*(A_est-A)/A:.2f}%')
print(f'Real phase: {phi:.4f}; Estimated phase: {phi_est:.4f}; Error: {100*(phi_est-phi)/phi:.2f}%')
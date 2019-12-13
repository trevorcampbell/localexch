import numpy as np

def local_empirical_measure(tau, X, T, f, b = lambda tau, t : 2*np.sqrt(f(tau, t))):
  b0 = b(tau, T) 
  bb = np.sorted(b0)
  bsum = 0.
  for j in range(T.shape[0]):
    bsum += bb[j]
    if bb[j] >= (0.5 + bsum)/(j+1)
      bsum -= bb[j]
      mu = (0.5 + bsum)/j
      return 2*np.maximum(mu - b0, 0.)
   

def local_empirical_estimate(h, tau, X, T, f, b = lambda tau, t : 2*np.sqrt(f(tau, t))):
  xi = local_empirical_measure(tau, X, T, f, b)
  return (xi*h(X)).sum()

import numpy as np
import os
import bokeh.plotting as bkp


np.random.seed(1)
M = 5
ell = 1.
sig = 1.
sign = 0.1
kernel = lambda x, y : sig**2*np.exp(-(x-y)**2/(2.*ell**2))
a = sig**2/(2.*ell**2)
f = lambda x : np.minimum(1., np.sqrt(2.*sig**2/(2.*ell**2*np.pi*sign**2))*x)

#mixture of K linear processes with random start/end points in [0, 1] (uniform 0, 1), and weight vectors interpolating from 0 to 1

#hyp testing example with covariate in [0, 1], effect changing random start/end in [0, 1], bernoulli based on p




N = 100000
xs = np.random.rand(N)
for m in range(M):
  K = np.zeros((N, N))
  for i in range(N):
    for j in range(N):
      K[i, j] = kernel(xs[i], xs[j])
  

x = np.linspace(0., 1., 1000)

p = bkp.figure()
p.line(x, f(x))
bkp.show(p)




# show that our method gets better as N to infty -- automatically performs bias variance tradeoff for local estimation
# GP is misspecified and expensive
# windowed methods don't reduce bias -- converge to "oversmoothed" etsimate
# use scipy.stats.wasserstein dist to evaluate with lots of samples from truth




#generate mixture of K gaussian processes

#compute

#window vs GP vs local exch


#estimation error vs computation time
#initial spike



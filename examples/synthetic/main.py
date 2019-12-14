import numpy as np
import os
import bokeh.plotting as bkp
import bokeh.layouts as bkl
from localexch.empirical import local_empirical_measure
import scipy.stats as st

np.random.seed(1)
N = 1000000
K = 5
sig = 0.05
f = lambda tau, t : np.minimum(1., (1. + 1./np.sqrt(2*np.pi*sig**2))*np.fabs(tau-t))
bf = lambda tau, t : f(tau, t)**3

#mixture of K linear processes with random start/end points in [0, 1] (uniform 0, 1), and interpolated weights (from Dirichlets)
a = np.random.rand(K)
b = np.random.rand(K)
wa = np.random.dirichlet(np.ones(K)/2)
wb = np.random.dirichlet(np.ones(K)/2)

#observation locations in [0, 1]
T = np.sort(np.random.rand(N))
w = (T[:,np.newaxis]*wb + (1.-T)[:,np.newaxis]*wa)
X = np.zeros(N)
for i in range(N):
  k = np.random.choice(K, p=T[i]*wb + (1.-T[i])*wa)
  X[i] = (T[i]*b[k] + (1.-T[i])*a[k]) + np.random.randn()*sig


plots = []

taus = np.linspace(0, 1, 5)
for tau in taus:
  xi = local_empirical_measure(tau, X, T, f, bf)
  eta = np.zeros(N)
  eta[ np.fabs(T-tau) < 0.01 ] = 1.
  eta /= eta.sum()
  xs = np.linspace(-.1, 1.1, 10000)
  pdfs = ((tau*wb + (1-tau)*wa)[:,np.newaxis]*np.array([st.norm.pdf(xs, loc=tau*b[k]+(1-tau)*a[k], scale=sig) for k in range(K)])).sum(axis=0)
  p = bkp.figure()
  p.line(xs, pdfs, line_width=3)
  heights, edges = np.histogram(X, bins=100, range=(-0.1, 1.1), weights=xi, density = True)
  p.quad(top=heights, bottom=0, left=edges[:-1], right=edges[1:], fill_color='black', line_color='white', alpha=0.5)
  heights, edges = np.histogram(X, bins=100, range=(-0.1, 1.1), weights=eta, density = True)
  p.quad(top=heights, bottom=0, left=edges[:-1], right=edges[1:], fill_color='blue', line_color='white', alpha=0.5)
  #p.segment(x0 = X, x1 = X, y0 = np.zeros(N), y1 = xi, color='black', line_width=3)
  plots.append(p)


#scatter
p = bkp.figure()
tt = np.linspace(0, 1, 1000)
p.scatter(T, X, alpha=0.1)
for k in range(K):
  p.scatter(tt, b[k]*tt + (1-tt)*a[k], fill_color='black', alpha = tt*wb[k] + (1-tt)*wa[k])
plots.append(p)


bkp.show(bkl.gridplot([plots]))




# show that our method gets better as N to infty -- automatically performs bias variance tradeoff for local estimation
# GP is misspecified and expensive
# windowed methods don't reduce bias -- converge to "oversmoothed" etsimate
# use scipy.stats.wasserstein dist to evaluate with lots of samples from truth




#generate mixture of K gaussian processes

#compute

#window vs GP vs local exch


#estimation error vs computation time
#initial spike



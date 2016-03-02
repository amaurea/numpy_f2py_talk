import numpy as np, fortran
from itimeit import itimeit
def bench(name, command):
	print "%-14s %8.4f ms" % (name, itimeit(command, mode='t', tmin=0.05)*1e3)
np.random.seed(0)
vecs = np.random.standard_normal([10000,3])

def mindist(vecs):
	best = np.inf
	for i, v1 in enumerate(vecs[:-1]):
		dists = np.sum((vecs[i+1:]-v1[None])**2,1)
		best = min(np.min(dists),best)
	return best

bench("mindist numpy", "mindist(vecs)")
bench("mindist fortran", "fortran.m.mindist(vecs.T)")

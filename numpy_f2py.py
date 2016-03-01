import numpy as np, fortran
from itimeit import itimeit

# f2py lets us call fortran directly on numpy arrays.
# Need to run f2py on the fortran file first. This produces a python module
# ("import fortran" above). If your computer is like mine, running "make"
# should be enough.

def bench(name, command):
	print "%-14s %8.4f ms" % (name, itimeit(command, mode='t', tmin=0.05)*1e3)

print "Sum of 10 M doubles"
a = np.arange(10000000.)
sum_numpy = np.sum(a)
sum_fortran = fortran.m.sum_plain(a)
print "numpy: %15.7e fortran: %15.7e diff: %15.7e" % (sum_numpy, sum_fortran, sum_numpy-sum_fortran)
print

print "They agree, but which one is faster?"
bench("numpy",   "np.sum(a)")
bench("fortran", "fortran.m.sum_plain(a)")
bench("fortran omp", "fortran.m.sum_omp(a)")
print
print "Speed for numpy and plain format is similar."
print "Not strange, as numpy is implemented in C."
print "But we can beat numpy by using OpenMP parallelization"
print "How much we beat it by depends on the number of cores on your computer"
print

print "A factor ~2 in speed relative to numpy is nice, but not worth"
print "mucking around in fortran for. The real gain of f2py is to implement"
print "operations that numpy doesn't provide."
print

print "Nontrivial example: Maximum in many subranges of array."
print "This operation is not supported by numpy, so we need manual looping"
bsize = 50
start = np.random.randint(0, len(a)-bsize, 100000)
bins = np.ascontiguousarray(np.array([start,start+bsize]).T)
# make half-open, like normal python ranges
bins[:,1] += 1

def max_by_bin(a, bins):
	res = np.zeros(len(bins))
	for i, b in enumerate(bins):
		res[i] = np.max(a[b[0]:b[1]])
	return res

def max_by_bin_fortran(a, bins):
	res = np.zeros(len(bins))
	fortran.m.max_by_bin(a, bins.T, res)
	return res
bench("numpy loop", "max_by_bin(a,bins)")
bench("fortran omp", "max_by_bin_fortran(a,bins)")

print "In this case, f2py gives a factor ~100 speedup compared to numpy!"

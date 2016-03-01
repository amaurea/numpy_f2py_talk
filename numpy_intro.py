import numpy as np
# Convenient array operations with numpy

print "Create a 3,3 2d-array full of zeros"
a = np.zeros((3,3))
print a

print "Set the [0,1] element to 4"
a[0,1] = 4
print a

print "Add 1 to the first two rows"
a[:2] += 1
print a

print "Compute the sum along each column"
asum = np.sum(a, 0)
print asum

print "And the total sum"
print np.sum(a)

print

print "Generate a sequence of integers"
b = np.arange(10)
print b

print "Extract every even number"
print b[0::2]

print "and every odd one"
print b[1::2]

print "Or reverse it"
print b[::-1]

print

print "Generate a [3,100000] array of random numbers with standard deviation 5"
c = np.random.standard_normal((3,100000))*5
print "shape: ", c.shape
print "first 5 columns"
print c[:,:5]

print "Compute the covariance matrix <cc'>"
cov = np.cov(c)
print cov

print "Normalize to get the correlation matrix"
var = np.diag(cov)
corr = cov/(var[None,:]*var[:,None])**0.5
print corr

print "Compute the covariance manually instead"
cov2 = c.dot(c.T)/c.shape[1]
print cov2

print

print "Generate a [2,3,4] 3d array with sequentially valued cells"
d = np.arange(2*3*4).reshape(2,3,4)
print d

print "Move the last axis first"
d = np.rollaxis(d, 2)
print d

print "Flatten into 1d array"
dflat = d.reshape(-1)
print dflat

print "And sort"
print np.sort(dflat)

print

print "Eigenvalue decomposition of matrix"
print "Original matrix (should be positive-definite)"
print cov
e, v = np.linalg.eigh(cov)
print "eivenvalues:"
print e
print "eigenvectors"
print v

print "Reconstruct original matrix naively"
print "v:", v
print "times"
print "np.diag(e):", np.diag(e)
print "times"
print "v.T", v.T
print "="
cov2 = v.dot(np.diag(e)).dot(v.T)
print cov2

print "Difference"
print cov-cov2

print "Reconstruct via einstein summation. Very flexible command worth remembering."
cov3 = np.einsum("ij,j,kj->ik",v,e,v)
print cov3
print "Difference"
print cov-cov3

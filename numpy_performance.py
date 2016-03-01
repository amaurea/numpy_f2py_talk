import numpy as np
from itimeit import itimeit

# How fast is numpy compared to normal python?
# Is it always faster? What are the pitfalls?

def bench(name, command):
	print "%-26s %9.4f ms" % (name, itimeit(command, mode='t', tmin=0.1)*1e3)

print "3x3 matrix product"
print "------------------"
a = np.eye(3)*2
b = np.arange(3*3.).reshape(3,3)
bench("numpy", "a.dot(b)")

alist = a.tolist()
blist = b.tolist()
def pydot(alist, blist):
	clist = [[0 for i in blist[0]] for j in alist]
	for i, crow in enumerate(clist):
		for j, cval in enumerate(crow):
			for k in range(len(blist)):
				clist[i][j] += alist[i][k]*blist[k][j]
	return clist
bench("python lists", "pydot(alist,blist)")
print "Only a factor 5 or so difference in speed for small arrays"

print

print "100x100 matrix product"
print "----------------------"
a = np.eye(100)*2
b = np.arange(100*100.).reshape(100,100)
bench("numpy", "a.dot(b)")
alist = a.tolist()
blist = b.tolist()
bench("python lists", "pydot(alist,blist)")
print "Python lists are roughly 1000 times slower than numpy!"

print

print "Simple sum of 10 M doubles"
print "----------"
a = np.arange(10000000.)
alist = a.tolist()
bench("python sum of list", "sum(alist)")
bench("numpy sum of array", "np.sum(a)")
bench("python sum of array", "sum(a)")
bench("numpy sum of list", "np.sum(alist)")
def mysum(a):
	res = 0
	for v in a: res += v
	return res
bench("manual sum over list", "mysum(alist)")
bench("manual sum over array", "mysum(a)")
print """
Conclusion:
1. Numpy operations are only fast on numpy arrays
2. Numpy is *slower* than plain python with manual looping"""

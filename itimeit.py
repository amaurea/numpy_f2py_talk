# coding=utf-8
"""An implementation of ipython's magic timeit command for plain python"""
from __future__ import print_function
import time, inspect, gc, math
# Make it work with both python2 and python3 without wasting
# potentially large amounts of memory
try: xrange
except NameError: xrange = range

template = """def itimeit_core():
	import time
	try: xrange
	except NameError: xrange = range
	%(setup)s
	t1 = time.time()
	for i in xrange(%(niter)d):
		%(command)s
	t2 = time.time()
	t3 = time.time()
	return t2-t1, t3-t2"""

template_with_base = """def itimeit_core():
	import time
	try: xrange
	except NameError: xrange = range
	%(setup)s
	t1 = time.time()
	for i in xrange(%(niter)d):
		%(command)s
		%(baseline)s
	t2 = time.time()
	for i in xrange(%(niter)d):
		%(baseline)s
	t3 = time.time()
	return t2-t1, t3-t2"""

def itimeit(command="pass", setup="pass", baseline=None, locs="caller",
		globs="caller", repeat=3, niter=0, tmin=0.2, mode="p"):
	"""Run the specified command (string) repeatedly, and estimate the
	run time. Like ipython's magic %timeit command, but unlike the normal
	python timeit, the environment is inherited from the calling frame.
	This means that you can usually call it directly without bothering with
	the 'setup' argument.
	
	Like %itimeit, the number of iterations is automatically adjusted
	such that the run time takes between repeat*tmin and repeat*tmin*10 seconds
	(or repeat times the time for a single evaluation if greater). This gives
	a useful compromise between accuracy and run time. The final time estimate
	is the shortest run time out of the repetitions, divided by the number of
	iterations per repetition.

	If you don't want to use the caller's environment, you can override this
	by passing in dictionaries to use for locals and globals in their
	respective arguments.

	If 'baseline' is specified, it should be a command string whose time will
	be subtracted from the estimate. For example, baseline="pass" will subtract
	the time an empty loop takes, which will approximately compensate for the
	benchmark overhead. Because the speed of a statement depends on what statements
	ran before it, among other things, this isn't necessarily very accurate, and
	can result in negative times for when command and baseline take almost the
	same time.

	The 'mode' argument controls how the results are reported.
	'p': Print the result in %timeit format
	't': Return the estimated run time for the command
	'f': Return a dictionary with more detailed information.
	
	Examples:
		>itimeit("1+1")
		10000000 loops, best of 3: 21.03 ns per loop

		>itimeit("1+1", baseline="pass")
		10000000 loops, best of 3: 4.367 ns per loop

		# Access functions and modules without a cumbersome setup
		>def foo(i):
			while i != 0:
				i /= 2
		>itimeit("foo(100)")
		1000000 loops, best of 3: 593.7 ns per loop

		>itimeit("np.random.standard_normal((1000,1000))")
		10 loops, best of 3: 72.01 ms per loop

		# The cost of this is that the environment is affected
		# when timing mutating commands.
		>a = np.arange(10)
		>def bar(a): a += 1
		1000000 loops, best of 3: 1.145 µs per loop
		>print a[0]
		3111111
	"""
	# Set up our timing core. We want the looping inside
	# the compiled object to minimize the number of exec calls
	params = {"setup": setup, "command": command, "baseline": baseline, "niter": 1}
	# Set up our environment
	if locs == "caller":
		caller = inspect.currentframe().f_back
		locs  = caller.f_locals
	if globs == "caller":
		caller = inspect.currentframe().f_back
		globs = caller.f_globals
	def build_core(niter):
		params["niter"] = niter
		if baseline is not None:
			code = compile(template_with_base % params, "<itimeit>", "exec")
		else:
			code = compile(template % params, "<itimeit>", "exec")
		exec code in globs, locs
		return locs["itimeit_core"]
	# Turn off garbage collection during timing
	gc_was_enabled = gc.isenabled()
	try:
		gc.disable()
		# Start our best-of-N loop
		times = []
		core = None
		for i in xrange(repeat):
			if niter == 0:
				# Automatically determine number of loops
				niter = 1
				# Would be while True, but this is safer in case
				# something is wrong with the timing or time limits
				for j in range(100):
					core = build_core(niter)
					t, tref = core()
					if t+tref > tmin: break
					niter *= 10
				times.append(t-tref)
			else:
				if core is None:
					core = build_core(niter)
				t, tref = core()
				times.append(t-tref)
	finally:
		if gc_was_enabled:
			gc.enable()
	time_per = min(times)/niter
	if "p" in mode:
		# Print result
		time_desc = format_si(time_per)
		print(u"%d loop%s, best of %d: %ss per loop" % (
			niter, "" if niter == 1 else "s", repeat, time_desc))
	if "r" in mode:
		return {"times": times, "niter": niter, "repeat": repeat,
			"time_per": time_per}
	elif "t" in mode:
		return time_per

def format_si(num, fmt="%.4g"):
	prefixes = [u"p", u"n", u"µ", u"m", u"", u"k", u"M", u"G", u"T", u"P"]
	offset = 4
	group  = int(max(-offset,min(len(prefixes)-offset,math.floor(math.log10(abs(num))/3))))
	prefix = prefixes[group+offset]
	scaled = num * 1000**(-group)
	return fmt % scaled + " " + prefix

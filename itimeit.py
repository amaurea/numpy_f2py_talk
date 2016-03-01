# coding=utf-8
"""An implementation of ipython's magic timeit command for plain python"""
import time, inspect, gc, math

template = """def itimeit_core():
	import time
	%(setup)s
	t1 = time.time()
	for i in xrange(%(niter)d):
		%(command)s
	t2 = time.time()
	if '%(baseline)s' is not 'None':
		for i in xrange(%(niter)d):
			%(baseline)s
	t3 = time.time()
	return t2-t1, t3-t2"""

def itimeit(command="pass", setup="pass", baseline=None, locs="caller",
		globs="caller", repeat=3, niter=0, tmin=0.2, mode="p"):
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
		print u"%d loop%s, best of %d: %ss per loop" % (
			niter, "" if niter == 1 else "s", repeat, time_desc)
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

Notes for talk on numpy and f2py
================================
These are notes/example code used for my talk optimizing python code with numpy
and f2py. They are mostly meant as a skeleton to give the talk around, not as
a replacement for the talk, but I post them here in the hope that they will be
useful anyway.

1. `numpy_intro.py`: Introduction to numpy through many small examples.
2. `numpy_performance.py`: How fast is numpy compared to python?
3. `numpy_f2py.py`: Calling fortran from python via numpy. How much is there to gain?
4. `fortran.f90`: Fortran code used in `numpy_f2py.py`.

These are mostly self-contained from the talk, and can be run as stand-alone examples,
for example `python numpy_performance.py`. Before running `python numpy_f2py.py`, the
fortran code needs to be compiled. On linux (possibly mac?), this should be as simple
as running `make`.

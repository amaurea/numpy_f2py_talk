export FFLAGS = -fopenmp -Ofast -fvect-cost-model=unlimited -fPIC -ffree-line-length-none -fdiagnostics-color=always -Wno-tabs

fortran.so: fortran.f90
	f2py2 -c --noopt -m fortran fortran.f90 -lgomp
clean:
	rm -f *.so *.mod *.pyc

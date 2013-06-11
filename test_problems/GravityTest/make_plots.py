import numpy as na
import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
import matplotlib.pyplot as plt

Data = na.loadtxt("TestGravityCheckResults.out")

# Read in data from text file produced by code

radius = Data[:,0]
ForceTangentialComputed = Data[:,1]
ForceRadialComputed = Data[:,2]
ForceRadialTrue = Data[:,3]

Error = (ForceRadialComputed-ForceRadialTrue)/ForceRadialTrue
indices = na.where((radius > 1.0) & (radius < 8.0))
rmsError = na.std(Error[indices])
print "rms error = "+str(rmsError)

# Plot the computed radial force again the r-2 profile 
#  (which should be equal except for outer part where the periodic 
#   boundary conditions are important, and inner part, where grid
#   softening is important).
# Also plot tangential component of force, which should be zero
#  (or at least small compared to radial component).

plt.loglog(radius, ForceRadialComputed, label=r'F$_{\rm rad}$', ls='None', marker='.')
plt.loglog(radius, ForceRadialTrue, label=r'F$_{\rm rad}$ (true)')
plt.loglog(radius, ForceTangentialComputed, label=r'F$_{\rm tang}$', ls='None', marker='+')
plt.xlabel('r (root grid cells)')
plt.ylabel('Acceleration')
plt.axis([0.2,14.0,1.0e-7,1.0e0])
plt.legend()
plt.savefig('GravityTest.eps')

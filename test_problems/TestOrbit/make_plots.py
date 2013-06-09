#
#  This script makes the plots for the TestOrbit problem type.
#
# Note: this script assumes enzo has been run with "enzo.exe TestOrbit.exe > output.log"
#   (since we need some stuff from output.log)
#
import numpy as na
import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
import matplotlib.pyplot as plt
import os
from math import *
from yt.mods import *
from yt.utilities.linear_interpolators import *

FileIn = open("output.log", "r")

xpos = []
ypos = []
zpos = []
xvel = []
yvel = []
zvel = []

# read stuff in from file
for line in FileIn:
   if 'id=1' in line:
      lst = line.split()
      xpos.append(lst[1])
      ypos.append(lst[2])
      zpos.append(lst[3])
      xvel.append(lst[4])
      yvel.append(lst[5])
      zvel.append(lst[6])
      
FileIn.close()

# convert to numpy array: easier to manipulate
x = na.array(xpos)
y = na.array(ypos)
z = na.array(zpos)
xv = na.array(xvel)
yv = na.array(yvel)
zv = na.array(zvel)

rad_diff = []
counter = []
energy = []

diffweight=0.0
radsum=0.0
energysum=0.0

# go through and calculate radius error, also kinetic energy
for i in range(len(x)):
   radius = ( ( float(x[i])-0.5)**2 + ( float(y[i])-0.5)**2 + ( float(z[i])-0.5)**2 )**0.5
   raddiff = (radius-0.3)/0.03125 
   radsum = radsum + raddiff
   diffweight = diffweight + 1.0
   kinetice = 0.5*(float(xv[i])**2 + float(yv[i])**2 + float(zv[i])**2)
   vmag = (float(xv[i])**2 + float(yv[i])**2 + float(zv[i])**2)**0.5
   rad_diff.append(raddiff)
   energy.append(kinetice)
   energysum += kinetice
   counter.append(i)

radsum = radsum/diffweight
energysum /= diffweight

#print "radsum is ", radsum
#print "energysum is ", energysum

# tweak radius to mean
rd = na.array(rad_diff)-radsum
# convert counter to orbit number
ct = na.array(counter)/416.

# switch energy to val/<val>, for convenience
en = na.array(energy)/energysum


# plots orbit in x-y plane (should be a circle)
plt.scatter(x[::8], y[::8], s=1, lw=0, marker='.')
plt.axis("equal")
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('TestOrbit_xy.eps')
plt.close()

# plots orbit in x-z plane (should be a straight line)
# NOT in paper.
plt.scatter(x[::8], z[::8], s=1, lw=0, marker='.')
plt.xlim(0.1,0.9)
plt.ylim(0.4999999,0.5000001)
plt.xlabel('x')
plt.ylabel('z')
plt.savefig('TestOrbit_xz.eps')
plt.close()

# plots delta_r / delta_x (error in orbit radius)
# (should be very small)
plt.plot(ct[::2], rd[::2])
plt.xlabel('Orbit Number')
plt.ylabel('$\delta r / \Delta x$')
plt.xlim(0,200)
plt.savefig('orbit_radius_error.eps')
plt.close()

# plots kinetic energy of orbit (normalized to 1)
# (we need to do quite a bit more for the total energy plot, that's in another file)
plt.plot(ct[::2], en[::2])
plt.xlabel('Orbit Number')
plt.ylabel('Kinetic Energy')
plt.xlim(0,200)
plt.savefig('kinetic_energy.eps')
plt.close()

#
#
#  This script makes the total energy plot for the TestOrbit parameter type.
#
# Note: this script assumes enzo has run the TestOrbit problem with the baryon
#  fields turned on and the gravitational potential written out.  To do this,
#  make sure that the following parameters are set to 1 in the enzo parameter
#  file:
#
#    TestOrbitUseBaryons = 1
#    ComputePotential = 1
#    WritePotential = 1
#


KE = []
PE = []
TE = []
time = []

it = 0

ts = TimeSeriesData.from_filenames("*/*.hierarchy")
for pf in ts:
    
    # particle position
    xp = pf.h.grids[0]["particle_position_x"][1]
    yp = pf.h.grids[0]["particle_position_y"][1]
    zp = pf.h.grids[0]["particle_position_z"][1]
    # particle mass
    xv = pf.h.grids[0]["particle_velocity_x"][1]
    yv = pf.h.grids[0]["particle_velocity_y"][1]
    zv = pf.h.grids[0]["particle_velocity_z"][1]

    myKE = 0.5 * (xv**2 + yv**2 + zv**2)

    # calculate potential energy (somewhat laborious; need to use potential value
    # in grids, hence the gymnastics)
    fv = {'x':np.array([xp],ndmin=3), 'y':np.array([yp],ndmin=3), 'z':np.array([zp],ndmin=3)}
    pot = TrilinearFieldInterpolator(pf.h.grids[0]["Grav_Potential"],(0.0, 1.0, 0.0, 1.0, 0.0, 1.0),"xyz",True)
    myPE = float(pot(fv)[0][0][0])

    myTE = myKE + myPE

    #print myKE, myPE, myTE

    # ignore first value: the PE is garbage since the potential energy field is not
    # actually calculated before this is written out.
    if it > 0:
        KE.append(myKE)
        PE.append(myPE)
        TE.append(myTE)
        time.append(pf.current_time)

    it += 1

# turn into NumPy arrays for convenient manipulation
TotalEnergy = na.array(TE) 
AllTime = na.array(time)

# print out some interesting info (note: all energies are specific total energies, in arbitrary units)
print "Total energy mean: ", np.mean(TotalEnergy)
print "Total energy STD: ", np.std(TotalEnergy)
print "total energy min, max: ", np.min(TotalEnergy), np.max(TotalEnergy)
print "|std/mean|: ", abs(np.std(TotalEnergy)/np.mean(TotalEnergy))
print "|max-min/mean|: ", abs( (np.max(TotalEnergy)-np.min(TotalEnergy))/np.mean(TotalEnergy))

# make the actual plot (note: total energy is specific total energy, in arbitrary units)
plt.plot(AllTime[::2], TotalEnergy[::2])
plt.plot([0,200],[np.mean(TotalEnergy),np.mean(TotalEnergy)],'k--')
plt.plot([0,200],[np.mean(TotalEnergy)+np.std(TotalEnergy),np.mean(TotalEnergy)+np.std(TotalEnergy)],'k:')
plt.plot([0,200],[np.mean(TotalEnergy)-np.std(TotalEnergy),np.mean(TotalEnergy)-np.std(TotalEnergy)],'k:')
plt.xlabel('Orbit Number')
plt.ylabel('Total Energy')
plt.xlim(1,200)
plt.ylim(-1.78, -1.75)
plt.figtext(0.17, 0.82, '$<\mathrm{TE}> = -1.76797$', size=15)
plt.figtext(0.17, 0.77, '$\sigma_{\mathrm{TE}} = 0.004885$', size=15)
plt.figtext(0.17, 0.72, '$\sigma_{\mathrm{TE}}/|<\mathrm{TE}>| = 0.002763$', size=15)
plt.savefig('TestOrbit_TotalEnergy.eps')
plt.close()


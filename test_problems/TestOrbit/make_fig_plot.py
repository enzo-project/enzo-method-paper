#
#  This script makes most of the plots for the TestOrbit problem type.  The
#   one that is not made is the total energy plot, which is in another file
#   for the sake of clarity.
#
# Note: this script assumes enzo has been run with "enzo.exe TestOrbit.exe > TestOrbit.out"
#   (since we need some stuff from TestOrbit.out)
#
import numpy as na
import matplotlib.pyplot as plt
import os
from math import *

FileIn = open("TestOrbit.out", "r")

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
plt.plot(x[::2], y[::2])
plt.axis("equal")
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('TestOrbit_xy.png')
plt.close()

# plots orbit in x-z plane (should be a straight line)
# NOT in paper.
plt.plot(x[::2], z[::2])
plt.xlim(0.1,0.9)
plt.ylim(0.4999999,0.5000001)
plt.xlabel('x')
plt.ylabel('z')
plt.savefig('TestOrbit_xz.png')
plt.close()

# plots delta_r / delta_x (error in orbit radius)
# (should be very small)
plt.plot(ct[::2], rd[::2])
plt.xlabel('Orbit Number')
plt.ylabel('$\delta r / \Delta x$')
plt.xlim(0,200)
plt.savefig('orbit_radius_error.png')
plt.close()

# plots kinetic energy of orbit (normalized to 1)
# (we need to do quite a bit more for the total energy plot, that's in another file)
plt.plot(ct[::2], en[::2])
plt.xlabel('Orbit Number')
plt.ylabel('Kinetic Energy')
plt.xlim(0,200)
plt.savefig('kinetic_energy.png')
plt.close()

#

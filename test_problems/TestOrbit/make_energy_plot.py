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
from yt.mods import *
from yt.utilities.linear_interpolators import *
import numpy as na
import matplotlib.pyplot as plt

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
plt.figtext(0.17, 0.82, '$<TE> = -1.76797$', size=15)
plt.figtext(0.17, 0.77, '$\sigma_{TE} = 0.004885$', size=15)
plt.figtext(0.17, 0.72, '$\sigma_{TE}/|<TE>| = 0.002763$', size=15)
plt.savefig('TotalEnergy.png')
plt.close()

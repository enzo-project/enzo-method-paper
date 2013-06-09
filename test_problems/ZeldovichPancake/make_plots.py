import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
import matplotlib.pyplot as plt
from yt.mods import *

pf = load('DD0001/data0001')
ray = pf.h.ortho_ray(0,(0,0))

p = plt.subplot(311)
plt.semilogy(ray['x'], ray['Density'], c='k', ls='-', marker='.', ms=5)
plt.ylabel(r'Density (cm$^{-3}$)')

p = plt.subplot(312)
plt.semilogy(ray['x'], ray['Temperature'], c='k', ls='-', marker='.', ms=5)
plt.ylabel('Temperature (K)')
plt.ylim(0.3,1.5e8)
p.yaxis.set_major_locator(mpl.ticker.FixedLocator([1,100,1e4,1e6,1e8]))


p = plt.subplot(313)
plt.plot(ray['x'], 1e-5*ray['x-velocity'], c='k', ls='-', marker='.', ms=5)
plt.ylabel('Velocity (km/s)')
plt.xlabel('x')
plt.ylim(-2250,2250)
p.yaxis.set_major_locator(mpl.ticker.FixedLocator([-2000,-1000,0,1000,2000]))

plt.savefig('AMRZeldovichPancake.eps')

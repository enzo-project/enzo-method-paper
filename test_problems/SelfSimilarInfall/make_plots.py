import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
from yt.mods import *
import pylab

# This script generates a plot for the self-similar infall test

### define problem name
problem_name = 'SphericalInfall'

### define simulation output directory and filename base
output_dir_base = 'DD'
datafile_base = 'data'

### define output to be plotted
dumpid = '0024'

# This is the effective resolution of the initial conditions
Ninitial = 64

# This is the initial perturbation amplitude of a single cell in the IC's
delta_init = 40.0

### define some filenames
exact_solution_filename = './exact_solution_gamma_53.txt'
plot_filename = './' + problem_name + '.eps'
filename = output_dir_base + dumpid + '/' + datafile_base + dumpid

### read exact solution
exact = pylab.csv2rec( exact_solution_filename, delimiter=' ', names=('lambda', 'V', 'D', 'P', 'M') )

# open output
pf = load(filename)

# Compute radial profile
r_min = pf.h.get_smallest_dx()*pf.units["cm"]
r_max = 0.4*pf.units["cm"]
center = pf.domain_center*(1.0+1.0/Ninitial)
print "center = ", center
center = pf.h.all_data().quantities["MaxLocation"]('Density')[2:5]
print "center = ", center

slc = SlicePlot(pf, 'z', ['Density','x-velocity', 'Temperature'], center='max')
slc.save()

sphere = pf.h.sphere(center, r_max)
profile = BinnedProfile1D(sphere, 40, "Radius", r_min, r_max)
profile.add_fields("Density", weight="CellVolume")
profile.add_fields("RadialVelocity", weight="CellVolume")
profile.add_fields("Pressure", weight="CellVolume")
profile.add_fields("CellMass", weight=None, accumulation=True)
#profile.write_out('test.txt', '%0.6e', 'left')


# Convert to Bertschinger dimensionless variables (eq. 2.9 and 3.2 of Bertschinger 1985)
G          = 6.67e-8
time_init  = 0.8165131621921  # in enzo time units
tau        = pf.current_time / time_init # both in enzo time units
r_init     = ((3.0/(4.0*pylab.pi))**(1.0/3.0)) / Ninitial * pf.units["cm"]  / tau**(2.0/3.0)
r_ta       = (4.0*tau/(3.0*pylab.pi))**(8.0/9.0) * delta_init**(1.0/3.0) * r_init
print "r_init, rta, tau = ", r_init, r_ta, tau
HubbleConstant = 2.0/(3.0*(pf.current_time * pf["Time"]))
rho_H      = 1.0/(6*pylab.pi*G * (pf.current_time * pf["Time"])**2)
vel_units  = r_ta / (pf["Time"]*pf.current_time)
pressure_units = rho_H * vel_units**2
mass_units = (4.0/3.0) * pylab.pi * rho_H * r_ta**3

r = profile["Radius"] / r_ta
D = profile["Density"] / rho_H
V = (profile["RadialVelocity"] + profile["Radius"]*HubbleConstant) / vel_units   # Velocity is peculiar velocity so we need to add bag in the Hubble flow
P = profile["Pressure"] / pressure_units
M = profile["CellMass"] / mass_units

# Generate figure
fig = pylab.figure(1, figsize=(7,7))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharex=ax1)
ax3 = fig.add_subplot(223, sharex=ax1)
ax4 = fig.add_subplot(224, sharex=ax1)

ax1.loglog(r, D, 'o')
ax1.loglog(exact['lambda'], exact['D'])
ax1.set_xlabel(r'$\lambda$')
ax1.set_ylabel('D')
ax1.set_xlim(0.02, 1.0)
ax1.set_ylim(1.0e-1, 1.0e5)

ax2.semilogx(r, V, 'o')
ax2.semilogx(exact['lambda'], exact['V'])
ax2.set_xlabel(r'$\lambda$')
ax2.set_ylabel('V')
ax2.set_ylim(-2, 2)

ax3.loglog(r, P, 'o')
ax3.loglog(exact['lambda'], exact['P'])
ax3.set_xlabel(r'$\lambda$')
ax3.set_ylabel('P')
ax3.set_ylim(1.0e-3, 1.0e5)

ax4.loglog(r, M, 'o')
ax4.loglog(exact['lambda'], exact['M'])
ax4.set_xlabel(r'$\lambda$')
ax4.set_ylabel('M')
ax4.set_ylim(1.0e-1, 1.0e2)


pylab.tight_layout()

### Save plot
fig.savefig(plot_filename)

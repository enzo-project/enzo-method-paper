# This figure requires the grackle chemistry and cooling library.
# Visit grackle.readthedocs.org for more information.

from matplotlib import pyplot

from utilities.testing import *

from pygrackle.grackle_wrapper import *
from pygrackle.fluid_container import FluidContainer

from utilities.api import \
     setup_fluid_container, \
     calculate_mean_molecular_weight, \
     calculate_hydrogen_number_density, \
     set_cosmology_units, \
     get_cooling_units

from utilities.primordial_equilibrium import \
     total_cooling, \
     nHI, nHII, nHeI, nHeII, nHeIII, ne
     
from utilities.physical_constants import \
     mass_hydrogen_cgs, \
     sec_per_Myr, \
     sec_per_Gyr, \
     cm_per_mpc

my_chem = chemistry_data()
my_chem.use_chemistry = 1
my_chem.with_radiative_cooling = 0
my_chem.primordial_chemistry = 1
my_chem.metal_cooling = 0
my_chem.UVbackground = 0
my_chem.include_metal_heating = 0
my_chem.comoving_coordinates = 0
my_chem.a_units = 1.0
my_chem.density_units = mass_hydrogen_cgs
my_chem.length_units = 1.0
my_chem.time_units = 1.0
my_chem.velocity_units = my_chem.length_units / my_chem.time_units
current_redshift = 0.0
fc = setup_fluid_container(my_chem, current_redshift=current_redshift,
                           converge=True, tolerance=1e-6, max_iterations=np.inf,
                           dt=(0.0001 * sec_per_Myr / my_chem.time_units))
calculate_temperature(fc)
a = 1.0 / (1.0 + current_redshift) / my_chem.a_units
calculate_cooling_time(fc, a)      
t_sort = np.argsort(fc["temperature"])
t_cool = fc["cooling_time"][t_sort] * my_chem.time_units
my_T = fc["temperature"][t_sort]
my_nH = calculate_hydrogen_number_density(my_chem, fc).mean()
cooling_rate = fc["energy"][t_sort] / t_cool * fc["density"] * \
  my_chem.density_units / my_nH**2
eq_cooling = total_cooling(my_T, my_nH) / my_nH**2
eq_cooling_cen = total_cooling(my_T, my_nH, rates='cen') / my_nH**2

fontsize = 14
n_rows = 1
n_columns = 1

# blank space between edge of figure and active plot area
top_buffer = 0.03
bottom_buffer = 0.1
left_buffer = 0.12
right_buffer = 0.03

# blank space between plots
hor_buffer = 0.05
vert_buffer = 0.05

# calculate the height and width of each panel
panel_width = ((1.0 - left_buffer - right_buffer - 
                ((n_columns-1)*hor_buffer)) / n_columns)
panel_height = ((1.0 - top_buffer - bottom_buffer - 
                 ((n_rows-1)*vert_buffer)) / n_rows)

# create a figure (figsize is in inches
pyplot.figure()

### Cooling figure
axes = pyplot.axes((left_buffer, bottom_buffer, 
                    panel_width, panel_height))
axes.loglog(my_T, eq_cooling, color='black', alpha=0.7,
            linestyle="--", linewidth=1.5)
axes.loglog(my_T, cooling_rate, color='black', alpha=0.7,
            linestyle="-", linewidth=1)
axes.loglog(my_T, eq_cooling_cen, color='black', alpha=0.7,
            linestyle=":", linewidth=1.5)
axes.xaxis.set_label_text('T [K]', fontsize=fontsize)
axes.yaxis.set_label_text('$\\Lambda$ / n${_{\\rm H}}^{2}$ [erg s$^{-1}$ cm$^{3}$]', 
                          fontsize=fontsize)
axes.set_xlim(1e4, 1e9)
axes.set_ylim(1e-26, 2e-22)
tick_labels = axes.xaxis.get_ticklabels() + \
  axes.yaxis.get_ticklabels()
for tick_label in tick_labels:
    tick_label.set_size(fontsize)
pyplot.savefig('cooling.png')
pyplot.savefig('cooling.pdf')
pyplot.savefig('cooling.eps')

pyplot.clf()

### Ionization balance figure
axes = pyplot.axes((left_buffer, bottom_buffer, 
                    panel_width, panel_height))

# Plot H ions
axes.loglog(my_T, (nHI(my_T, my_nH) /
                   (nHI(my_T, my_nH) +
                    nHII(my_T, my_nH))),
            color="#B82E00", alpha=0.7, linestyle="--", linewidth=1.5)
axes.loglog(my_T, (nHII(my_T, my_nH) /
                   (nHI(my_T, my_nH) +
                    nHII(my_T, my_nH))),
            color="#B88A00", alpha=0.7, linestyle="--", linewidth=1.5)

axes.loglog(my_T, (nHI(my_T, my_nH, rates='cen') / 
                   (nHI(my_T, my_nH, rates='cen') +
                    nHII(my_T, my_nH, rates='cen'))),
            color="#B82E00", alpha=0.7, linestyle=":", linewidth=1.5)
axes.loglog(my_T, (nHII(my_T, my_nH, rates='cen') /
                   (nHI(my_T, my_nH, rates='cen') +
                    nHII(my_T, my_nH, rates='cen'))),
            color="#B88A00", alpha=0.7, linestyle=":", linewidth=1.5)

axes.loglog(my_T, (fc["HI"] / (fc["HI"] + fc["HII"])),
            label="HI", color="#B82E00", alpha=0.7, linestyle="-", linewidth=1.)
axes.loglog(my_T, (fc["HII"] / (fc["HI"] + fc["HII"])),
            label="HII", color="#B88A00", alpha=0.7, linestyle="-", linewidth=1.)

# Plot He ions
axes.loglog(my_T, (nHeI(my_T, my_nH) /
                   (nHeI(my_T, my_nH)   +
                    nHeII(my_T, my_nH)  +
                    nHeIII(my_T, my_nH))),
            color="#002EB8", alpha=0.7, linestyle="--", linewidth=1.5)
axes.loglog(my_T, (nHeII(my_T, my_nH) /
                   (nHeI(my_T, my_nH)   +
                    nHeII(my_T, my_nH)  +
                    nHeIII(my_T, my_nH))),
               color="#008AB8", alpha=0.7, linestyle="--", linewidth=1.5)
axes.loglog(my_T, (nHeIII(my_T, my_nH) /
                   (nHeI(my_T, my_nH)   +
                    nHeII(my_T, my_nH)  +
                    nHeIII(my_T, my_nH))),
               color="#00B88A", alpha=0.7, linestyle="--", linewidth=1.5)

axes.loglog(my_T, (nHeI(my_T, my_nH, rates='cen') / 
                   (nHeI(my_T, my_nH, rates='cen')   +
                    nHeII(my_T, my_nH, rates='cen')  +
                    nHeIII(my_T, my_nH, rates='cen'))),
              color="#002EB8", alpha=0.7, linestyle=":", linewidth=1.5)
axes.loglog(my_T, (nHeII(my_T, my_nH, rates='cen') /
                   (nHeI(my_T, my_nH, rates='cen')   +
                    nHeII(my_T, my_nH, rates='cen')  +
                    nHeIII(my_T, my_nH, rates='cen'))),
              color="#008AB8", alpha=0.7, linestyle=":", linewidth=1.5)
axes.loglog(my_T, (nHeIII(my_T, my_nH, rates='cen') /
                   (nHeI(my_T, my_nH, rates='cen')   +
                    nHeII(my_T, my_nH, rates='cen')  +
                    nHeIII(my_T, my_nH, rates='cen'))),
              color="#00B88A", alpha=0.7, linestyle=":", linewidth=1.5)

axes.loglog(my_T, (fc["HeI"] / (fc["HeI"] + fc["HeII"] + fc["HeIII"])),
              label="HeI", color="#002EB8", alpha=0.7, linestyle="-", linewidth=1.)
axes.loglog(my_T, (fc["HeII"] / (fc["HeI"] + fc["HeII"] + fc["HeIII"])),
              label="HeII", color="#008AB8", alpha=0.7, linestyle="-", linewidth=1.)
axes.loglog(my_T, (fc["HeIII"] / (fc["HeI"] + fc["HeII"] + fc["HeIII"])),
              label="HeIII", color="#00B88A", alpha=0.7, linestyle="-", linewidth=1.)

axes.xaxis.set_label_text('T [K]', fontsize=fontsize)
axes.yaxis.set_label_text('fraction', fontsize=fontsize)
axes.set_xlim(1e4, 1e9)
axes.set_ylim(1e-10, 1)
tick_labels = axes.xaxis.get_ticklabels() + \
  axes.yaxis.get_ticklabels()
for tick_label in tick_labels:
    tick_label.set_size(fontsize)
axes.legend(loc='best', prop=dict(size=fontsize))
pyplot.savefig('fractions.png')
pyplot.savefig('fractions.pdf')
pyplot.savefig('fractions.eps')

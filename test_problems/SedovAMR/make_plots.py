import os as os

# Calculates analytic solution for Sedov blast, creates text file sedov.in
# (contains radius, density, pressure, velocity, temperature, and internal
# energy)
execfile('sedov_analytic_solution.py') 

# Calculates radial profiles for simulations, writes into
# files sedov_ppm_output.dat and sedov_zeus_output.dat
# (not explicitly used, but useful)
execfile('sedov_outputdata.py')

# Makes slices of density for both simulations (PPM, Zeus)
execfile('sedov_slice.py')

# plots annulus-averaged profiles from both simulations, along
# with the analytical result from sedov.in
execfile('sedov_density_plot.py')
execfile('sedov_internal_energy_plot.py')
execfile('sedov_pressure_plot.py')
execfile('sedov_velocity_plot.py')

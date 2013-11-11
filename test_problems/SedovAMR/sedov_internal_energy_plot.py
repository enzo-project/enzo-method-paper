from yt.mods import *
# plots radially-averaged pressure profile from both simulations, along
# with the analytical result from sedov.in

import matplotlib.pyplot as plt

################ PPM ################
# Load the dataset.
pf_ppm = load("PPM/DD0007/DD0007")

pc_ppm = PlotCollection(pf_ppm, center=[0.5, 0.5, 0.5])

pc_ppm.add_profile_sphere(0.5, "cm", ["Radius", "ThermalEnergy"], x_bins=100, x_log=False)
thermal_energy_data_ppm = pc_ppm.plots[-1].data["ThermalEnergy"]
radius_data_ppm =  pc_ppm.plots[-1].data["Radius"]


################ Zeus ################
# Load the dataset.
pf_zeus = load("Zeus/DD0007/DD0007")

pc_zeus = PlotCollection(pf_zeus, center=[0.5, 0.5, 0.5])

pc_zeus.add_profile_sphere(0.5, "cm", ["Radius", "ThermalEnergy"], x_bins=100, x_log=False)
thermal_energy_data_zeus = pc_zeus.plots[-1].data["ThermalEnergy"]
radius_data_zeus =  pc_zeus.plots[-1].data["Radius"]

################################ Make plot ################

# read in anlytical solution
sedovsol_radius = []
sedovsol_thermal_energy = []
file = open("sedov.in", "r")
for line in file:
    linesplit = line.split('\t')
    if linesplit[0] != '#':
        sedovsol_radius.append(float(linesplit[0]))
        sedovsol_thermal_energy.append(float(linesplit[4]))
        

# python plot                                                                                                                     
plotfig = plt.figure()

# normalised mass by total mass                                                                                                   
plt.plot(sedovsol_radius, sedovsol_thermal_energy,'k-', linewidth=3)  # analytic solution
plt.plot(radius_data_ppm, thermal_energy_data_ppm, 'bo-', radius_data_zeus, thermal_energy_data_zeus, 'ro-', linewidth=1)
plt.yscale('log')

plt.axis([0.2, 0.5, 1.0, 500.0])

plt.figtext(0.75,0.76,"Zeus",color='r', fontsize=14)
plt.figtext(0.75,0.80,"PPM",color='b', fontsize=14)
plt.figtext(0.75,0.84,"Analytic", color='k', fontsize=14)

plt.xlabel('R')
plt.ylabel('U')

# save python plot as png file                                                                                                    
plt.savefig("sedov_internal_energy_plot.eps")


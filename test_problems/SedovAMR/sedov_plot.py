from yt.mods import *
# plots radially-averaged density profile from both simulations, along
# with the analytical result from sedov.in

import matplotlib.pyplot as plt

################ PPM ################
# Load the dataset.
pf_ppm = load("PPM/DD0007/DD0007")

pc_ppm = PlotCollection(pf_ppm, center=[0.5, 0.5, 0.5])

pc_ppm.add_profile_sphere(0.5, "cm", ["Radius", "CellMass"], weight=None, x_bins=100, x_log=False)
mass_data_ppm = pc_ppm.plots[-1].data["CellMass"]
radius_data_ppm =  pc_ppm.plots[-1].data["Radius"]

pc_ppm.add_profile_sphere(0.5, "cm", ["Radius", "CellVolume"], weight=None, x_bins=100, x_log=False)
volume_data_ppm = pc_ppm.plots[-1].data["CellVolume"]

density_data_ppm = mass_data_ppm/volume_data_ppm


################ Zeus ################
# Load the dataset.
pf_zeus = load("Zeus/DD0007/DD0007")

pc_zeus = PlotCollection(pf_zeus, center=[0.5, 0.5, 0.5])

pc_zeus.add_profile_sphere(0.5, "cm", ["Radius", "CellMass"], weight=None, x_bins=100, x_log=False)
mass_data_zeus = pc_zeus.plots[-1].data["CellMass"]
radius_data_zeus =  pc_zeus.plots[-1].data["Radius"]

pc_zeus.add_profile_sphere(0.5, "cm", ["Radius", "CellVolume"], weight=None, x_bins=100, x_log=False)
volume_data_zeus = pc_zeus.plots[-1].data["CellVolume"]

density_data_zeus = mass_data_zeus/volume_data_zeus


################################ Make density plot ################

# read in anlytical solution
sedovsol_radius = []
sedovsol_density = []
file = open("sedov.in", "r")
for line in file:
    linesplit = line.split('\t')
    if linesplit[0] != '#':
        sedovsol_radius.append(float(linesplit[0]))
        sedovsol_density.append(float(linesplit[2]))
        

# python plot                                                                                                                     
plotfig = plt.figure()

# normalised mass by total mass                                                                                                   
plt.plot(sedovsol_radius, sedovsol_density,'k-', linewidth=3)  # analytic solution
plt.plot(radius_data_ppm, density_data_ppm, 'ro-', radius_data_zeus, density_data_zeus, 'bo-', linewidth=1)

plt.figtext(0.2,0.76,"Zeus",color='b', fontsize=14)
plt.figtext(0.2,0.80,"PPM",color='r', fontsize=14)
plt.figtext(0.2,0.84,"Analytic", color='k', fontsize=14)

plt.xlabel('Radius')
plt.ylabel('Density')

# save python plot as png file                                                                                                    
plt.savefig("sedov_density_plot.eps")


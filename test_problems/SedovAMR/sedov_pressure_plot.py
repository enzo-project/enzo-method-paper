from yt.mods import *
# plots radially-averaged pressure profile from both simulations, along
# with the analytical result from sedov.in

import matplotlib.pyplot as plt

################ PPM ################
# Load the dataset.
pf_ppm = load("PPM/DD0007/DD0007")

pc_ppm = PlotCollection(pf_ppm, center=[0.5, 0.5, 0.5])

pc_ppm.add_profile_sphere(0.5, "cm", ["Radius", "Pressure"], x_bins=100, x_log=False)
pressure_data_ppm = pc_ppm.plots[-1].data["Pressure"]
radius_data_ppm =  pc_ppm.plots[-1].data["Radius"]


################ Zeus ################
# Load the dataset.
pf_zeus = load("Zeus/DD0007/DD0007")

pc_zeus = PlotCollection(pf_zeus, center=[0.5, 0.5, 0.5])

pc_zeus.add_profile_sphere(0.5, "cm", ["Radius", "Pressure"], x_bins=100, x_log=False)
pressure_data_zeus = pc_zeus.plots[-1].data["Pressure"]
radius_data_zeus =  pc_zeus.plots[-1].data["Radius"]

################################ Make plot ################

# read in anlytical solution
sedovsol_radius = []
sedovsol_pressure = []
file = open("sedov.in", "r")
for line in file:
    linesplit = line.split('\t')
    if linesplit[0] != '#':
        sedovsol_radius.append(float(linesplit[0]))
        sedovsol_pressure.append(float(linesplit[5]))
        

# python plot                                                                                                                     
plotfig = plt.figure()

# normalised mass by total mass                                                                                                   
plt.plot(sedovsol_radius, sedovsol_pressure,'k-', linewidth=3)  # analytic solution
plt.plot(radius_data_ppm, pressure_data_ppm, 'bo-', radius_data_zeus, pressure_data_zeus, 'ro-', linewidth=1)
plt.axis([0.2, 0.5, 0.0, 10.0])


plt.figtext(0.2,0.76,"Zeus",color='r', fontsize=14)
plt.figtext(0.2,0.80,"PPM",color='b', fontsize=14)
plt.figtext(0.2,0.84,"Analytic", color='k', fontsize=14)

plt.xlabel('R')
plt.ylabel('P')

# save python plot as png file                                                                                                    
plt.savefig("sedov_pressure_plot.eps")


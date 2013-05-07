from yt.mods import *
import matplotlib.pyplot as plt

# Load the dataset.
#pf = load("../100amr4/ppm/DD0007/sb_L2x2_amr4_0007")
pf = load("../100amr4/zeus/DD0007/sb_L2x2_amr4_zeus_0007")

pc = PlotCollection(pf, center=[0.5, 0.5, 0.5])

pc.add_profile_sphere(0.5, "cm", ["Radius", "CellMass"], weight=None, x_bins=100, x_log=False)
mass_data = pc.plots[-1].data["CellMass"]
radius_data =  pc.plots[-1].data["Radius"]

pc.add_profile_sphere(0.5, "cm", ["Radius", "CellVolume"], weight=None, x_bins=100, x_log=False)
volume_data = pc.plots[-1].data["CellVolume"]

density_data = mass_data/volume_data


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
plt.plot(radius_data, density_data, 'ro', sedovsol_radius, sedovsol_density)

plt.xlabel('Radius')
plt.ylabel('Density')

# save python plot as png file                                                                                                    
plt.savefig("sedov_density_plot")


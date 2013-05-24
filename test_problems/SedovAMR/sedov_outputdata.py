# Calculates radial profiles for simulations, writes into
# files sedov_ppm_output.dat and sedov_zeus_output.dat

from yt.mods import *
import matplotlib.pyplot as plt

################# ZEUS plots
pf1 = load("Zeus/DD0007/DD0007")
pc1 = PlotCollection(pf1, center=[0.5, 0.5, 0.5])
pc1.add_profile_sphere(0.5, "cm", ["Radius", "CellMass"], weight=None, x_bins=100, x_log=False)

mass_data = pc1.plots[-1].data["CellMass"]
radius_data =  pc1.plots[-1].data["Radius"]

pc1.add_profile_sphere(0.5, "cm", ["Radius", "CellVolume"], weight=None, x_bins=100, x_log=False)
volume_data = pc1.plots[-1].data["CellVolume"]

density_data = mass_data/volume_data

pc1.add_profile_sphere(0.5, "cm", ["Radius", "RadialVelocity"], weight="CellMass", x_bins=100, x_log=False)
velocity_data = pc1.plots[-1].data["RadialVelocity"]

pc1.add_profile_sphere(0.5, "cm", ["Radius", "Pressure"], weight="CellMass", x_bins=100, x_log=False)
pressure_data = pc1.plots[-1].data["Pressure"]

pc1.add_profile_sphere(0.5, "cm", ["Radius", "ThermalEnergy"], weight="CellMass", x_bins=100, x_log=False)
internalenergy_data = pc1.plots[-1].data["ThermalEnergy"]


# output profiles

file = open("sedov_zeus_output.dat", 'w')
print >> file, "# radius density internal-energy pressure velocity"
for i in range(len(radius_data)):
    print >> file, "%f\t%f\t%f\t%f\t%f" % (radius_data[i], density_data[i], internalenergy_data[i], pressure_data[i], velocity_data[i])
file.close()

################# PPM plots

# ZEUS plots
pf2 = load("PPM/DD0007/DD0007")
pc2 = PlotCollection(pf2, center=[0.5, 0.5, 0.5])
pc2.add_profile_sphere(0.5, "cm", ["Radius", "CellMass"], weight=None, x_bins=100, x_log=False)

mass_data = pc2.plots[-1].data["CellMass"]
radius_data =  pc2.plots[-1].data["Radius"]

pc2.add_profile_sphere(0.5, "cm", ["Radius", "CellVolume"], weight=None, x_bins=100, x_log=False)
volume_data = pc2.plots[-1].data["CellVolume"]

density_data = mass_data/volume_data

pc2.add_profile_sphere(0.5, "cm", ["Radius", "RadialVelocity"], weight="CellMass", x_bins=100, x_log=False)
velocity_data = pc2.plots[-1].data["RadialVelocity"]

pc2.add_profile_sphere(0.5, "cm", ["Radius", "Pressure"], weight="CellMass", x_bins=100, x_log=False)
pressure_data = pc2.plots[-1].data["Pressure"]

pc2.add_profile_sphere(0.5, "cm", ["Radius", "ThermalEnergy"], weight="CellMass", x_bins=100, x_log=False)
internalenergy_data = pc2.plots[-1].data["ThermalEnergy"]


# output profiles

file = open("sedov_ppm_output.dat", 'w')
print >> file, "# radius density internal-energy pressure velocity"
for i in range(len(radius_data)):
    print >> file, "%f\t%f\t%f\t%f\t%f" % (radius_data[i], density_data[i], internalenergy_data[i], pressure_data[i], velocity_data[i])
file.close()

:from yt.mods import *
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

pc.add_profile_sphere(0.5, "cm", ["Radius", "RadialVelocity"], weight="CellMass", x_bins=100, x_log=False)
velocity_data = pc.plots[-1].data["RadialVelocity"]

pc.add_profile_sphere(0.5, "cm", ["Radius", "Pressure"], weight="CellMass", x_bins=100, x_log=False)
pressure_data = pc.plots[-1].data["Pressure"]

pc.add_profile_sphere(0.5, "cm", ["Radius", "ThermalEnergy"], weight="CellMass", x_bins=100, x_log=False)
internalenergy_data = pc.plots[-1].data["ThermalEnergy"]


# output profiles

file = open("sedov_zeus_output.dat", 'w')
print >> file, "# radius density internal-energy pressure velocity"
for i in range(len(radius_data)):
    print >> file, "%f\t%f\t%f\t%f\t%f" % (radius_data[i], density_data[i], internalenergy_data[i], pressure_data[i], velocity_data[i])
file.close()

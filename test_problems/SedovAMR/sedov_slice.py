# Makes slices of density for both simulations (PPM, Zeus)

from yt.mods import * 

fn1 = "PPM/DD0007/DD0007"
pf1 = load(fn1)
slice1 = SlicePlot(pf1, 'z', "Density", center=[0.5, 0.5, 0.0]).save("PPM_Density_slice.eps")

fn2 = "Zeus/DD0007/DD0007"
pf2 = load(fn2)
slice2 = SlicePlot(pf2, 'z', "Density", center=[0.5, 0.5, 0.0]).save("Zeus_Density_slice.eps")


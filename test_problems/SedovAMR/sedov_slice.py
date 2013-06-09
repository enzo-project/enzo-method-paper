# Makes slices of density for both simulations (PPM, Zeus)

from yt.mods import * 

fn1 = "PPM/DD0007/DD0007"
pf1 = load(fn1)
slice1 = SlicePlot(pf1, 'z', "Density", center=[0.5, 0.5, 0.0], origin='domain')
slice1.set_width((1.05,'unitary'))
# See matplotlib issue #1188
slice1.plots['Density'].cb.solids.set_edgecolor('face')
slice1.set_font({'size':15})
slice1.save("sedov-ppm-slice.eps", mpl_kwargs={'bbox_inches':'tight'})


fn2 = "Zeus/DD0007/DD0007"
pf2 = load(fn2)
slice2 = SlicePlot(pf2, 'z', "Density", center=[0.5, 0.5, 0.0], origin='domain')
slice2.set_width((1.05,'unitary'))
# See matplotlib issue #1188
slice2.plots['Density'].cb.solids.set_edgecolor('face')
slice2.save("sedov-zeus-slice.eps", mpl_kwargs={'bbox_inches':'tight'})


# Makes slices of density for both simulations (PPM, Zeus)
from yt.mods import *

def _DensityCode(field, data):
    return data['Density']/data.convert('Density')

add_field('DensityCode', display_name="Density", units="",
          function=_DensityCode)

fn1 = "PPM/DD0007/DD0007"
pf1 = load(fn1)
slice1 = SlicePlot(pf1, 'z', "DensityCode", center=[0.5, 0.5, 0.0], origin='domain')
slice1.set_window_size(5)
slice1.set_width((1.05,'unitary'))
slice1.set_zlim('DensityCode',1.5e-3,7e0)
# See matplotlib issue #1188
slice1.plots['DensityCode'].cb.solids.set_edgecolor('face')
slice1.save("sedov-ppm-slice.eps", mpl_kwargs={'bbox_inches':'tight'})


fn2 = "Zeus/DD0007/DD0007"
pf2 = load(fn2)
slice2 = SlicePlot(pf2, 'z', "DensityCode", center=[0.5, 0.5, 0.0], origin='domain')
slice2.set_window_size(5)
slice2.set_width((1.05,'unitary'))
slice2.set_zlim('DensityCode',1.5e-3,7e0)
# See matplotlib issue #1188
slice2.plots['DensityCode'].cb.solids.set_edgecolor('face')
slice2.save("sedov-zeus-slice.eps", mpl_kwargs={'bbox_inches':'tight'})


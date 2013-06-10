from yt.mods import *

def _DensityCode(field, data):
    return data['Density']/data.convert('Density')

add_field('DensityCode', display_name="Density", units="",
          function=_DensityCode)

name1 = './CT/DD0056/data0056'
name2 = './Dedner/DD0032/data0032'
pf1 = load(name1)
pf2 = load(name2)
names=[
    'MHDCT_OrszagTang_Density.eps',
    'MHDDedner_OrszagTang_Density.eps'
    ]
for i, pf in enumerate([pf1,pf2]):
  sl = SlicePlot( pf, 2, 'DensityCode', origin='domain', width=(1.05, 'unitary'))
  sl.set_window_size(5)
  sl.set_zlim('DensityCode',0.1,1)
  # See matplotlib issue #1188
  sl.plots['DensityCode'].cb.solids.set_edgecolor('face')
  print sl.save(names[i],mpl_kwargs={'bbox_inches':'tight'})

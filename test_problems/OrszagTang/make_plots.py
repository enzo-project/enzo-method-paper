from yt.mods import *
name1 = '/Users/dcollins/scratch/Paper31/ot04_large_2d/DD0056/data0056'
name2 = '/Users/dcollins/scratch/Paper31/ot08_large_dedner_hlld/DD0032/data0032'
pf1 = load(name1)
pf2 = load(name2)
names=['mhdct_0056','mhddedner_0035']
sl=[]
for i, pf in enumerate([pf1,pf2]):
  sl.append( SlicePlot( pf, 2, 'Density') )
  sl[-1].set_zlim('Density',0.1,1)
  print sl[-1].save(names[i]+".eps")

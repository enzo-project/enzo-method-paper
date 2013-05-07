from yt.mods import * 

#fn = "../100amr4/ppm/DD0007/sb_L2x2_amr4_0007"
fn = "../100amr4/zeus/DD0007/sb_L2x2_amr4_zeus_0007"

pf = load(fn)
pc = PlotCollection(pf, center=[0.5, 0.5, 0.5])

p = pc.add_slice("Density", 2)
#p.modify["grids"]()

pc.save(fn)


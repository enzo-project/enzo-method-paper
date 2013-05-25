from yt.mods import *
import yt.visualization.eps_writer as EPS

output_num = 150
#fields = ["Density", "HI_Fraction", "Pressure", "Temperature"]
fields = ["Pressure", "Neutral_Fraction", "Density", "Temperature"]
cmap = ["algae", "gist_stern", "algae", "hot"]
zlim = [(2e-15, 2e-13), (1e-4, 1), (1e-28, 1e-25), (1e4, 1e5)]

fn = "DD%4.4d/data%4.4d" % (output_num, output_num)
pf = load(fn)

pc = PlotCollection(pf, center=[0.5, 0.5, 0.4990234375])
for i,f in enumerate(fields):
    p = pc.add_slice(f, 'y', use_colorbar=False)
    p.set_cmap(cmap[i])
    p.set_zlim(zlim[i][0], zlim[i][1])

ep = EPS.multiplot_yt(2,2,pc, margins=(0.2,0.2), bare_axes=True)
ep.scale_line(1.0/6.6, '1 kpc')
ep.title_box("15 Myr")
ep.save_fig("code-test-shadowing.eps")

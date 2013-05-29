from yt.mods import *

for n in range(11,12):

    pf = load("DD%04i/DD%04i" % (n,n))

    c = [2.0,0.5,0]

    buff = [120,480]  # this is backward because matplotlib transposes buffers.

    slice = SlicePlot(pf, 'z', "Density", center=c, width=((4.0, '1'), (1.0, '1')), origin='domain', axes_unit=('1','1')) 
    slice.set_buff_size(buff)

    filename = "DD%04i" % n

    slice.save(mpl_kwargs={'bbox_inches':'tight'},name="%s_slice_Density_z.eps" % filename)

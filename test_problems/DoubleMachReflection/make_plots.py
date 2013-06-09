from yt.mods import *

for n in range(11,12):

    pf = load("DD%04i/DD%04i" % (n,n))

    c = [2.0,0.5,0]

    slice = SlicePlot(pf, 'z', "Density", center=c,
                      width=((4.15, '1'), (1.15, '1')),
                      origin='domain', axes_unit=('1','1'))

    slice.set_zlim('Density',.5, 20)

    slice.set_buff_size((1000, 300))
    
    slice.set_window_size(12)
    
    # See matplotlib issue #1188
    slice.plots['Density'].cb.solids.set_edgecolor('face')

    slice.save(mpl_kwargs={'bbox_inches':'tight'},name="DoubleMachTest.eps")

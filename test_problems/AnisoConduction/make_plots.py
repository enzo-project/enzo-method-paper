from yt.mods import *

for n in range(11,12):
    
    pf = load("DD%04i/DD%04i" % (n,n))

    dd = pf.h.all_data()

    print "----------------------------------------------------"
    print "output number", n
    print " "
    print "Temperature:"
    print dd["Temperature"].min()
    print dd["Temperature"].max()

    #print "Density:"
    #print dd["Density"].min()
    #print dd["Density"].max()

    slice = SlicePlot(pf, 'z', "Temperature", width = (1.0, '1'), origin='domain', axes_unit=('1','1'))  #.save()
    #slice = SlicePlot(pf, 'z', "Temperature", width = (1.0, '1'), origin='domain', axes_unit=None)  #.save()

    filename = "DD%04i" % n

    slice.save(mpl_kwargs={'bbox_inches':'tight'}, name="%s_slice_Temperature_z.eps" % filename)

# the end

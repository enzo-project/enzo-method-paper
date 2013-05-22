from yt.mods import *

for n in range(300,301):
    
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

    slice.save(mpl_kwargs={'bbox_inches':'tight'})

    #slice.save("testplot.png")

# the end

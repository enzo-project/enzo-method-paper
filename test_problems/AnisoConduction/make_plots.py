from yt.mods import *

for n in [0,11]:
    
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


    x = (dd['x'].reshape((256,256)))[:,0]
    y = (dd['y'].reshape((256,256)))[0,:]
    Bx = dd['Bx'].reshape((256,256))
    By = dd['By'].reshape((256,256))
    ax = slice.plots['Temperature'].axes

    ## I found that I had to reverse Bx and By to get the correct
    ## closed circles. Something to do with the plot's origin being in
    ## the lower left?
    streams = ax.streamplot(x,y,By,Bx,color=(1,1,1,0.5),linewidth=1.5,density=1)

    ax.set_rasterization_zorder(5.0)
    
    ## filename = "DD%04i_slice_Temperature_z.png" % n
    filename = "DD%04i_slice_Temperature_z.eps" % n

    slice.save(mpl_kwargs={'bbox_inches':'tight'}, name=filename)

# the end

from yt.mods import *

filenames = {0: 'aniso_conduction_initial_output.eps',
             11: 'aniso_conduction_final_output.eps'}

for n in [0,11]:
    
    pf = load("DD%04i/DD%04i" % (n,n))

    dd = pf.h.all_data()

    print "----------------------------------------------------"
    print "output number", n
    print " "
    print "Temperature:"
    print dd["Temperature"].min()
    print dd["Temperature"].max()

    slice = SlicePlot(pf, 'z', "Temperature", width = (1.05, '1'), origin='domain', axes_unit=('1','1'))  #.save()
    slice.set_window_size(5)

    slice.annotate_streamlines('Bx', 'By', plot_args={'color':(1,1,1,0.5),'linewidth':0.7})
    
    slice.set_zlim('Temperature', 7e5, 2e7)

    # See matplotlib issue #1188
    slice.plots['Temperature'].cb.solids.set_edgecolor('face')
    
    slice.save(name=filenames[n], mpl_kwargs={'bbox_inches':'tight'})

# the end

from yt.mods import *
import pylab

# This script generates a 3x2 panel of plots for the Wave Pool
#   for three different hydro solvers at three different times.
#   It assumes the simulations have been run and are in the
#   directory structure PPM/AMR, PPM/noAMR, Zeus/AMR, etc.

### define problem name
problem_name = 'WavePool'

### define simulation output directory and filename base
output_dir_base = 'DD'
datafile_base = 'data'


### define some filenames
plot_filename = './' + problem_name + '.eps'

### generate exact solution
def make_exact(time):
    dens0 = 1.0
    wavelength = 0.1
    Gamma = 1.4
    speed = pylab.sqrt(Gamma*1.0/dens0)
    omega = 2.0*pylab.pi*speed/wavelength
    xexact = pylab.arange(0.0, 1.0, 0.001)
    deltime = time - xexact/speed
    exact = pylab.zeros(shape=deltime.shape)
    index = pylab.all([deltime*speed < wavelength, deltime > 0],axis=0)
    exact[index] = 0.01*pylab.sin(omega*deltime[index])
    exact = dens0*(1.0 + exact)
    return (xexact, exact)


#define plot a single frame
def plot_one(filename, name, axes, xbegin1, xwidth):
    print "opening " + filename

    # open output and create ray
    pf = load(filename)
    ray = pf.h.ortho_ray(0, [0.5, 0.5])

    # Get exact result
    (xexact, exact) = make_exact(pf.current_time)

    # rough computation of level for each point in ray (probably better way)
    level = -pylab.log(ray['dx']/ray['dx'][0])/pylab.log(2.0)

    # plot
    ax = pylab.axes(axes)
    pylab.axhline(0,color='k',linestyle='dotted')
    pylab.scatter(ray['x']+0.5*ray['dx'],ray['Density'], c=level, s=40, linewidths=(0,))
    pylab.plot(xexact, exact)

    #plot dashed lines for refined region
#    pylab.plot([0.25, 0.25], [0.9, 1.1], linestyle="--") 
#    pylab.plot([0.75, 0.75], [0.9, 1.1], linestyle="--") 
    x1 = pylab.array([0.25, 0.75])
    y1 = pylab.array([1.0, 1.0])
    ax.fill_between(x1, y1-0.01, y1+0.01, facecolor='grey', alpha=0.2)

    #set boundaries
    pylab.axis([xbegin1,xbegin1+xwidth,0.99,1.009999])
    ax.xaxis.set_major_locator(pylab.matplotlib.ticker.MultipleLocator(0.1))

    # Set axis (clunky)
    if axes[1] < 0.3:
        pylab.xlabel('Position')
    else:
        ax.set_xticklabels([])
    if axes[0] < 0.12:
        pylab.ylabel('Density')
    else:
        ax.set_yticklabels([])

    pylab.text(xbegin1+0.1*xwidth, 1.009, name, va='top')  
    pylab.text(xbegin1+0.1*xwidth, 1.007, "t=%3.2f" % pf.current_time, va='top')  


### make plot

def make_name(id):
    return output_dir_base + id + '/' + datafile_base + id

pylab.figure(1, figsize=(8,8))

dumpid = ['0002', '0003', '0008']
name = ['MUSCL', 'Zeus', 'PPM']
xbegin = [0.0, 0.1, 0.6]
xwidth = [0.3999, 0.3999, 0.4]
xstart = 0.1
ystart = 0.08
xsize = 0.29
ysize = 0.29
for i in range(3):
    for j in range(3):
        corner = [xstart+xsize*j, ystart+ysize*i, xsize, ysize]
        plot_one('./'+name[i]+'/' + make_name(dumpid[j]), name[i], corner, xbegin[j], xwidth[j])


### Save plot
pylab.savefig(plot_filename)

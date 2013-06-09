import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
from yt.mods import *
import pylab

# This script generates a 3x2 panel of plots for the Shock Pool
#   for three different hydro solvers at three different times.
#   It assumes the simulations have been run and are in the
#   directory structure PPM, Zeus, MUSCL

### define problem name
problem_name = 'ShockPool'

### define simulation output directory and filename base
output_dir_base = 'DD'
datafile_base = 'data'


### define some filenames
plot_filename = './' + problem_name + '.eps'

### generate exact solution
def make_exact(time):
    dens1 = 1.0
    Gamma = 1.4
    Mach  = 2.0
    dens2 = dens1*(Gamma + 1.0)*Mach**2 / ((Gamma - 1.0) * Mach**2 + 2.0)
    speed = Mach*pylab.sqrt(Gamma*1.0/dens1)
    xexact = pylab.arange(0.0, 1.0, 0.001)
    deltime = time - xexact/speed
    exact = pylab.ones(shape=deltime.shape)*dens1
    index = pylab.all([deltime > 0],axis=0)
    exact[index] = dens2
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

    #get axis
    ax = pylab.axes(axes)

    #plot grey for refined region
    x1 = pylab.array([0.25, 0.75])
    y1 = pylab.array([0.0, 0.0])
    ax.fill_between(x1, y1, y1+3, facecolor='grey', alpha=0.2)

    # plot
    pylab.axhline(0,color='k',linestyle='dotted')
    pylab.scatter(ray['x']+0.5*ray['dx'],ray['Density'], c=level, s=40, linewidths=(0,))
    pylab.plot(xexact, exact)

    #set boundaries
    pylab.axis([xbegin1,xbegin1+xwidth,0.7,3.0])
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

    pylab.text(xbegin1+0.05*xwidth, 1.2, name, va='top')  
    pylab.text(xbegin1+0.05*xwidth, 1.0, "t=%3.2f" % pf.current_time, va='top')  


### make plot

def make_name(id):
    return output_dir_base + id + '/' + datafile_base + id

pylab.figure(1, figsize=(8,8))

dumpid = ['0002', '0003', '0007']
name = ['MUSCL', 'Zeus', 'PPM']
xbegin = [0.05, 0.1, 0.65]
xwidth = [0.3, 0.3, 0.3]
xstart = 0.1
ystart = 0.08
xsize = 0.29
ysize = 0.29
for i in range(3):
    for j in range(3):
        corner = [xstart+xsize*j, ystart+ysize*i, xsize, ysize]
        plot_one('./'+name[i]+'/' + make_name(dumpid[j]), name[i], corner, xbegin[j], xwidth[j])



### Save plot
pylab.savefig(plot_filename, bbox_inches='tight')

from yt.mods import *
import pylab

# This script generates a 3x2 panel of plots for the SodShockTube
#   for three different hydro solvers with and without AMR.
#   It assumes the simulations have been run and are in the
#   directory structure PPM/AMR, PPM/noAMR, Zeus/AMR, etc.

### define problem name
problem_name = 'SodShockTube'

### define simulation output directory and filename base
output_dir_base = 'DD'
datafile_base = 'data'

### define output to be plotted
dumpid = '0001'

### define some filenames
exact_solution_filename = './SodShockTube_t=0.25_exact.txt'
plot_filename = './' + problem_name + '.eps'

### read exact solution
exact = pylab.csv2rec( exact_solution_filename, delimiter=' ', names=('x', 'Density', 'x-velocity', 'Pressure', 'InternalEnergy') )

# define error norm text label function
def error_label(name, norm, maxnorm, xpos, ypos):
    thistext = name + '\n'
    vexp =  pylab.floor( pylab.log10( norm ) )
    if norm == 0: vexp = 0
    vmant = norm / 10**vexp
    thistext += r'$\Vert$E$\Vert_1 = \, %3.1f' % vmant
    if vexp != 0:
        thistext += r' \times \, 10^{%2d}' % vexp
    thistext += '$\n'

    vexp =  pylab.floor( pylab.log10( maxnorm ) )
    if maxnorm == 0: vexp = 0
    vmant = maxnorm / 10**vexp
    thistext += r'$\Vert$E$\Vert_\infty \! = \, %3.1f' % vmant
    if vexp != 0:
        thistext += r' \times \, 10^{%2d}' % vexp
    thistext += '$'

    pylab.text(xpos, ypos, thistext, va='top')  


#define plot a single frame
def plot_one(filename, name, axes):
    field = 'Density'
    print "opening " + filename

    # open output and create ray
    pf = load(filename)
    ray = pf.h.ortho_ray(0, [0.5, 0.5])

    # first interpolate the exact solution onto the ray
    ray_exact = {'x': ray['x'], 
             'Density': pylab.stineman_interp(ray['x'],exact['x'],exact['Density']),
             'x-velocity': pylab.stineman_interp(ray['x'],exact['x'],exact['x-velocity']),
             'Pressure': pylab.stineman_interp(ray['x'],exact['x'],exact['Pressure']),
             'InternalEnergy': pylab.stineman_interp(ray['x'],exact['x'],exact['InternalEnergy'])}


    # compute first order and max error norms
    delta = ray['dx'] * abs( ray[field] - ray_exact[field] )
    norm = delta.sum()
    maxnorm = delta.max()

    # rough computation of level for each point in ray (probably better way)
    level = -pylab.log(ray['dx']/ray['dx'][0])/pylab.log(2.0)

    # plot
    ax = pylab.axes(axes)
    pylab.axhline(0,color='k',linestyle='dotted')
    pylab.plot(exact['x'],exact[field], c='black', linewidth=(1,))
    pylab.scatter(ray['x'],ray[field], c=level, s=8,  linewidths=(0,))

    # Set axis (clunky)
    pylab.axis([0,0.999,0,1.1]) # for density
    if axes[1] < 0.5:
        pylab.xlabel('Position')
    else:
        ax.set_xticklabels([])
    if axes[0] < 0.1:
        pylab.ylabel(field)
    else:
        ax.set_yticklabels([])

    error_label(name, norm, maxnorm, 0.41, 1.0)


### make plot

filename = output_dir_base + dumpid + '/' + datafile_base + dumpid

pylab.figure(1, figsize=(8,5))

plot_one('./PPM/noAMR/' + filename, 'PPM', [0.08, 0.54, 0.3, 0.42])
plot_one('./Zeus/noAMR/' + filename, 'Zeus', [0.38, 0.54, 0.3, 0.42])
plot_one('./MUSCL/noAMR/' + filename, 'MUSCL', [0.68, 0.54, 0.3, 0.42])
plot_one('./PPM/AMR/' + filename, 'PPM (AMR)', [0.08, 0.12, 0.3, 0.42])
plot_one('./Zeus/AMR/' + filename, 'Zeus (AMR)', [0.38, 0.12, 0.3, 0.42])
plot_one('./MUSCL/AMR/' + filename, 'MUSCL (AMR)', [0.68, 0.12, 0.3, 0.42])

### Save plot
pylab.savefig(plot_filename)

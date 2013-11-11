from yt.mods import *
import yt.visualization.eps_writer as EPS
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager, FontProperties
font= FontProperties(size='small')
rc('font', family='serif', serif='cmr10', size=18)

from matplotlib.ticker import NullFormatter
nullfmt = NullFormatter()

########################################################################
# Derived fields
########################################################################
def _MyRadius(field, data):
    center = data.get_field_parameter("center")
    dx = data["x"] - center[0]
    dy = data["y"] - center[1]
    dz = data["z"] - center[2]
    return na.sqrt(dx*dx + dy*dy + dz*dz)
add_field("Radius", function=_MyRadius, take_log=False, units='')
def _MyIonizedFrac(field, data):
    return data['HII_Fraction'] / 0.75908798
add_field("Ionized_Fraction", function=_MyIonizedFrac, take_log=True,
          units='')
def _MyNeutralFrac(field, data):
    return data['HI_Fraction'] / 0.75908798
add_field("Neutral_Fraction", function=_MyNeutralFrac, take_log=True,
          units='')
########################################################################

########################################################################
# Slice multi-panel plot
########################################################################

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
ep.save_fig("shadowing-slices.eps")

########################################################################
# Line cuts through the clump center at t = 1, 5, 10, 15 Myr
########################################################################

output = [10,50,100,150]
fields = ["Density", "Temperature", "Neutral_Fraction", "Pressure"]

xbound = (0.4,1)

# Calculate profiles

alldata = {}
for i in range(len(output)):
    amrfile = "DD%4.4d/data%4.4d" % (output[i], output[i])
    pf = load(amrfile)
    ray = pf.h.ray([xbound[0], 0.5, 0.5], [xbound[1], 0.5, 0.5])
    data = {}
    data['x'] = ray['x']
    for f in fields: 
        data[f] = ray[f]
    alldata[output[i]] = data
    del pf

# Plot the profiles

colors = ['r', 'g', 'm', 'b', 'k']
styles = ['--', ':', '-', '-.', '-']
ylabels = ['Density', 'Temperature', 'Neutral Fraction', 'Pressure']
units = ['g/cm$^3$', 'K', '', r'g cm$^{-1}$ s$^{-2}$']
ymins = [2e-28, 100, 5e-6, 2e-16]
ymaxs = [2e-25, 1e5, 1.5, 3e-13]
labels = ['1 Myr', '5 Myr', '10 Myr', '15 Myr']

plt.clf()
plt.subplots_adjust(hspace=1e-3, wspace=1e-3, right=0.875)
for i,f in enumerate(fields):
    p = plt.subplot(2,2,i+1)
    for j in range(len(output)):
        plt.semilogy(alldata[output[j]]['x'], alldata[output[j]][f],
                     c=colors[j], ls=styles[j],
                     label=labels[j])

    # Legend
    if f == "Neutral_Fraction":
        p.legend(loc='lower right', prop=font)

    # y-labels
    ylabel = ylabels[i]
    if units[i] != "":
        ylabel += " (" + units[i] + ")"
    p.set_ylabel(ylabel)

    if i % 2 == 1:
        p.set_xlim(xbound[0]+1e-3, xbound[1])
        p.axes.yaxis.set_label_position('right')
        for tick in p.axes.yaxis.get_major_ticks():
            tick.label1On = False
            tick.label2On = True
        p.axes.yaxis.set_label_coords(+1.2,0.5)
    else:
        p.axes.yaxis.set_label_coords(-0.2,0.5)

    # x-labels
    if i >= 2:
        p.set_xlabel(r'x/L$_{\rm box}$')
    else:
        p.axes.xaxis.set_major_formatter(nullfmt)

    yl = p.get_ylim()
    yl1 = []
    if ymins[i] != None:
        yl1.append(ymins[i])
    else:
        yl1.append(yl[0])
    if ymaxs[i] != None:
        yl1.append(ymaxs[i])
    else:
        yl1.append(yl[1])
    p.set_ylim(yl1)

    p.set_autoscale_on(True)

    i = i+1


plt.savefig('shadowing-rays.eps')


########################################################################
# PDFs of temperature and Mach number
########################################################################

nbins = 50
outputs = [100]
fields = ["Temperature", "MachNumber"]
labels = ["Temperature / 10$^4$ K", "Mach Number"]
styles = ["-", "--", ":"]
colors = ["k", "b", "r"]
times = [10, 50]
ranges = [[1,7], [0,2.5]]
yrange = [1e-4,1]
log = [False, False]

ni = len(outputs)
nj = len(fields)

plt.clf()
plt.subplots_adjust(right=0.97, top=0.95, hspace=1e-3, wspace=0.2)

index = 1
for i,out in enumerate(outputs):
    fn = "DD%4.4d/data%4.4d" % (out,out)
    pf = load(fn, data_style="enzo_packed_3d")
    #reg = pf.h.sphere([0.75757575, 0.5, 0.5], 0.121212)
    reg = pf.h.all_data()
    for j,f in enumerate(fields):
        data = na.log10(reg[f]) if log[j] else reg[f]
        if f == "Temperature" and not log[j]: data /= 1e4
        ntot = float(data.size)
        hh, bin_edges = na.histogram(data, bins=nbins, range=ranges[j], 
                                     weights=reg['CellVolumeCode'], 
                                     normed=False)
        centers = 0.5*(bin_edges[:-1] + bin_edges[1:])
        #p = plt.subplot(ni,nj,index)
        p = plt.subplot(1,2,j+1)
        plt.semilogy(centers, hh, ls="steps"+styles[i], c=colors[i],
                     label="%d Myr" % times[i])
        if j == 0 and i == 0: plt.ylabel("Probability distribution function")
        #if j == 1: plt.legend(loc="best", prop=font)
        if i+1 == ni:
            plt.ylim(yrange[0], yrange[1])
            plt.xlabel(labels[j])
        else:
            plt.ylim(1.00001*yrange[0], yrange[1])
            p.axes.xaxis.set_major_formatter(nullfmt)
        index += 1
    del reg
    del pf
        
plt.savefig("shadowing-pdf.eps")

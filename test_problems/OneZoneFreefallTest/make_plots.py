from collections import defaultdict
import matplotlib as mpl
mpl.rcParams['font.family'] = 'STIXGeneral'
from matplotlib import pyplot
import numpy as np
import cPickle as pickle
import sys

from yt.mods import *

def get_tracks(filenames, fields=None):
    if fields is None: fields = ['NumberDensity', 'Temperature']
    ts = TimeSeriesData.from_filenames(filenames)
    data = defaultdict(list)
    for pf in ts:
        print pf.fullpath
        for field in fields:
            data[field].append(pf.h.grids[0][field][0, 0, 0])
    for field in fields:
        data[field] = np.array(data[field])
    del ts
    return data

dirs = ['mf', 'Z-5', 'Z-4', 'Z-3', 'Z-2']
labels = ['$Z=0$', '10$^{-5}\/Z_\odot$',  '10$^{-4}\/Z_\odot$',
          '10$^{-3}\/Z_\odot$',  '10$^{-2}\/Z_\odot$']
colors = ['black', 'blue', 'green', 'orange', 'red']

if os.path.exists('data.p'):
    with open('data.p', 'rb') as fp:
        my_data = pickle.load(fp)
else:
    my_data = {}
    for my_dir in dirs:
        my_data[my_dir] = get_tracks("%s/DD*/*.hierarchy" % my_dir)

    with open('data.p', 'wb') as fp:
        pickle.dump(my_data, fp)
    
fontsize = 12

n_rows = 1
n_columns = 1

# blank space between edge of figure and active plot area
top_buffer = 0.01
bottom_buffer = 0.1
left_buffer = 0.09
right_buffer = 0.04

# blank space between plots
hor_buffer = 0.05
vert_buffer = 0.05

# calculate the height and width of each panel
panel_width = ((1.0 - left_buffer - right_buffer - 
                ((n_columns-1)*hor_buffer)) / n_columns)
panel_height = ((1.0 - top_buffer - bottom_buffer - 
                 ((n_rows-1)*vert_buffer)) / n_rows)

# create a figure (figsize is in inches
pyplot.figure()

my_axes = pyplot.axes((left_buffer, bottom_buffer, 
                       panel_width, panel_height))
    
for i, my_dir in enumerate(dirs):
    my_axes.loglog(my_data[my_dir]['NumberDensity'],
                   my_data[my_dir]['Temperature'],
                   color=colors[i], linestyle='-',
                   linewidth=1.5, alpha=0.7, label=labels[i])
my_axes.set_xlim(1, 1e12)
my_axes.set_ylim(10, 2e3)
my_axes.yaxis.set_label_text("T [K]", fontsize=fontsize)
my_axes.xaxis.set_label_text("n [cm$^{-3}$]", fontsize=fontsize)
tick_labels = my_axes.xaxis.get_ticklabels() + \
  my_axes.yaxis.get_ticklabels()
for tick_label in tick_labels:
    tick_label.set_size(fontsize)
my_axes.legend(loc='lower right', prop=dict(size=fontsize))
pyplot.savefig('OneZoneCollapseTest.eps')

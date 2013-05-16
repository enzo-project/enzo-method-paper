import glob
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font', size=24)
from matplotlib.font_manager import fontManager, FontProperties
font= FontProperties(size=16)

files = glob.glob('performance_*.out')
nfiles = len(files)

MAX_LEVEL = 6

timing = {'cores': np.zeros(nfiles, dtype='int'),
          'total_time': np.zeros(nfiles),
          'level_time': np.zeros((nfiles, MAX_LEVEL+1)),
          'routines': [],
          'routine_time': None}

# Determine the routine names
lines = open(files[0], 'r').readlines()
for l in lines:
    if not l.startswith('#') and len(l.split()) == 5:
        timing['routines'].append(l.split()[0])
nroutines = len(timing['routines'])
timing['routine_time'] = np.zeros((nfiles, nroutines, 4))
 
# Parse performance files         
for i, f in enumerate(files):
    lines = open(f, 'r').readlines()
    for l in lines:
        if l.find('MPI processes') >= 0:
            timing['cores'][i] = int(l.split(':')[1])
        elif l.startswith('Level'):
            level = int(l[7:9])
            time = float(l.split()[1])
            timing['level_time'][i,level] = time
        elif l.startswith('Total'):
            timing['total_time'][i] = float(l.split()[1])
        elif len(l) > 1:
            str0 = l.split()[0]
            if str0 in timing['routines']:
                ipl = timing['routines'].index(str0)
                timing['routine_time'][i,ipl,:] = \
                    map(float, l.split()[1:5])
        

# Sort by cores
isort = np.argsort(timing['cores'])
timing['cores'] = timing['cores'][isort]
timing['total_time'] = timing['total_time'][isort]
timing['level_time'] = timing['level_time'][isort,:]
timing['routine_time'] = timing['routine_time'][isort,:,:]

colors = ['k', 'b', 'r', 'g', 'm', 'c']
styles = ['-', '--', ':', '-.']
markers = ['v', '^', 's', '*', '+', 'D']
########################################################################
# Plot of time spent: total and on each level
########################################################################
plt.subplots_adjust(left=0.13, right=0.99, bottom=0.13, top=0.87, hspace=1e-3)
plt.loglog(timing['cores'], timing['total_time'], 'k-', lw=3,
           label='Total', marker='o', ms=10)
for i in range(MAX_LEVEL+1):
    plt.loglog(timing['cores'], timing['level_time'][:,i],
               color=colors[i%len(colors)], ls=styles[i%len(styles)],
               label='Level %d' % i, marker=markers[i%len(markers)], ms=10)
plt.xlim(100,20000)
plt.ylim(1,4e3)
plt.xlabel('Number of Cores')
plt.ylabel('Time [s]')
plt.legend(loc=8, prop=font, ncol=4, bbox_to_anchor=[0.5,0.975])
plt.savefig('strong_scaling_levels.eps')

########################################################################
# Timing of the routines
########################################################################
plt.clf()
plt.subplots_adjust(left=0.135, right=0.99, bottom=0.13, top=0.785, hspace=1e-3)
for i in range(nroutines):
    plt.loglog(timing['cores'], timing['routine_time'][:,i,0],
               color=colors[i%len(colors)], ls=styles[i%len(styles)],
               marker=markers[i%len(markers)], ms=10,
               label=timing['routines'][i])
plt.xlim(100,20000)
plt.ylim(0.1,1e3)
plt.xlabel('Number of Cores')
plt.ylabel('Time [s]')
plt.legend(loc=8, prop=font, ncol=2, bbox_to_anchor=[0.425,1.03])
plt.savefig('strong_scaling_routines.eps')

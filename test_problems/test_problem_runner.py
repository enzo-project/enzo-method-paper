"""
This script makes all of the figures in the 'Representative test problems' section
of the Enzo method paper (Section 11.2).  It requires you to have built an Enzo executable,
named enzo.exe, ***using the HYPRE library (http://acts.nersc.gov/hypre/)***, and also yt built
with SciPy.  If you do NOT use the HYPRE library, or do not have SciPy installed along with yt, 
remove the 'CosmoIFront' problem from the testnames list below.  You also need to set
two paths (edit the variables directly below this comment block), and you can turn on
and off some options.  

Note that running this script can take quite a bit of time - some of the simulations
take a while to run (hours).  If you're worried that it's not doing anything, go into
the simulation directory for the simulation that is currently running (which will be
printed out by the script) and look to see when the file output.log was last modified.
This file contains stdout and stderr from the simulation.

    --Brian O'Shea, oshea@msu.edu, May 2013
    
"""
import os as os

############ USER SETS THESE PARAMETERS #############

# directory where the enzo.exe binary is stored
enzodir = '/Users/bwoshea/Desktop/SYNCHED/Current\ Projects/Papers/enzo-method-paper/test_problems'

# directory where this file is located (need absolute path name)
topleveldir = '/Users/bwoshea/Desktop/SYNCHED/Current Projects/Papers/enzo-method-paper/test_problems'

# the following options allow you to articulate whether you want the simulations to be run (runsim),
#   figures to be made (makefig), and directories to be cleaned out (cleandata/cleanfigs).  Note that 
#   this is so you can separately run the various simulations, make the figures, and/or clean out all
#   of the various subdirectories.

# if cleandata == 1, delete all simulation files in the directory.  If 0, don't touch them.
#    Note: output log is always deleted before a simulation is run.  Also, if you clean out
#    the data, you can't make figures without rerunning the simulations!
cleandata = 1

# if cleanfigs == 1, delete all figures in the directory.  If 0, don't touch them.
cleanfigs = 1

# if runsim > 0, run simulations; if 0, don't.
runsim = 0

# if makefig > 0, make figures.  if 0, don't.  Figures require simulation data!
makefig = 0

############ END OF USER-SET PARAMETERS #############

# do some preemptive cleaning of directory names
enzoexec = (enzodir.rstrip(' ')).rstrip('/') + '/enzo.exe'
topleveldir = (topleveldir.rstrip(' ')).rstrip('/')

print '\n'
print 'Using this enzo binary:', enzoexec
print 'Top level directory is:', topleveldir
print '\n'

"""
testnames = ['AnisoConduction', 'CosmoIFront', 'DoubleMachReflection',
            'GravityTest', 'OneZoneFreefallTest', 'OrszagTang', 'PhotonShadowing',
            'SedovAMR', 'SelfSimilarInfall', 'ShockPool', 'ShockTube', 'TestOrbit',
            'WavePool', 'ZeldovichPancake']
"""
#testnames = ['ZeldovichPancake',  'OneZoneFreefallTest']
testnames =  ['OneZoneFreefallTest']

# goes through directory dirname and its subdirs and makes list of directories that
#   contains enzo parameter files (which end in '.enzo')
def add_sim_dirs(my_list, dirname, fns):
    for fn in fns:
        if fn.endswith(".enzo"):
            my_list += [dirname]

# goes through directory dirname and its subdirs and makes list of directories that
#   contains scripts to make figures (which are all named 'make_figs.py')
def add_figure_dirs(my_list, dirname, fns):
    for fn in fns:
        if fn == 'make_plots.py':
            my_list += [dirname]

all_sim_dirs = []
all_figure_dirs = []

# goes through list of test problems and creates lists of simulation directories and
#   figure directories.
for thistest in testnames:
    os.path.walk(thistest, add_sim_dirs, all_sim_dirs)
    os.path.walk(thistest, add_figure_dirs, all_figure_dirs)

print 'All simulation directories:', all_sim_dirs, '\n'
print 'All figure directories:', all_figure_dirs, '\n'


"""
 loop over all directories containing .enzo files (from list generated above)
 and run simulations.
"""
for simdir in all_sim_dirs:
    print 'In simulation directory', simdir, '\n'
    os.chdir(simdir)  # go into simulation directory
     
    if cleandata == 1:
        os.system('rm -rf DD* Enzo_Build* Evtime *out *log *Log RunFinished SphericalInfallReport')
        
    if runsim > 0:  # now we actually run the simulation!
        dirlisting = os.listdir('.')  # get listing of all of the files in the directory
        for names in dirlisting:  # loop over file names
            if names.endswith('.enzo'):  # if we have found a parameter file...
                os.system('rm -f output.log')
                execscript = enzodir + '/enzo.exe -d ' + names + ' >& output.log'
                os.system(execscript)

    os.chdir(topleveldir)  # go back to top-level directory


"""
 loop over all directories containing make_plots.py files (from list generated above)
 and generate all of the figures.
"""
for figuredir in all_figure_dirs:
    print 'In figure directory', figuredir, '\n'
    os.chdir(figuredir)  # go into figure directory

    if cleanfigs == 1:
        os.system('rm -f *.png *.eps *.jpg')

    if makefig > 0:  # actually make the figures
        dirlisting = os.listdir('.')  # get listing of all files in the directory
        for names in dirlisting: # loop over file names
            if names == 'make_plots.py':
                execfile('make_plots.py')  

    os.chdir(topleveldir)  # back to top-level dir.
    
# fin.

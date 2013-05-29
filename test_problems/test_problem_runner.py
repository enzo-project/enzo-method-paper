"""
         Enzo method paper figure generator

This script makes all of the figures in the 'Representative test
problems' section of the Enzo method paper (Section 11.2).  It
requires you to have compiled an Enzo executable, named enzo.exe,
***using the HYPRE library (http://acts.nersc.gov/hypre/)***, and also
have yt (http://yt-project.org) built with SciPy, which requires a
non-default option to be set in the install script.  If you do NOT
compile Enzo with the HYPRE library, or do not have SciPy installed
along with yt, remove the 'CosmoIFront' problem from the testnames
list below.  You also need to set two paths -- the location of the
Enzo binary and the path to the test problem directory -- and you
can turn on and off some options.  This is all done directly below
this comment block.

Note: some of the simulations used to create the method paper figures
can take several hours to run, or should be run on several CPUs. See
the README file in this directory for specifics.  You can change the
simulations that are run with this script by editing the variable
'testnames', below.

    --Brian O'Shea, oshea@msu.edu, May 2013
    
"""
import os as os

############ USER SETS THESE PARAMETERS #############

# directory where the enzo.exe binary is stored (needs absolute path name)
enzodir = '/Users/bwoshea/Desktop/SYNCHED/Current\ Projects/Papers/enzo-method-paper/test_problems'

# directory where this file is located (needs absolute path name)
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

# if runsim = 1, run simulations; if 0, don't.
runsim = 1

# if makefig = 1, make figures.  if 0, don't.  Figures require simulation data!
makefig = 1

############ END OF USER-SET PARAMETERS #############

# do some preemptive cleaning of directory names
enzoexec = (enzodir.rstrip(' ')).rstrip('/') + '/enzo.exe'
topleveldir = (topleveldir.rstrip(' ')).rstrip('/')

print '\n'
print 'Using this enzo binary:', enzoexec
print 'Top level directory is:', topleveldir
print '\n'

"""
Complete list of test names, for convenience:

all_testnames = ['AnisoConduction', 'CosmoIFront', 'DoubleMachReflection',
            'GravityTest', 'OneZoneFreefallTest', 'OrszagTang', 'PhotonShadowing',
            'SedovAMR', 'SelfSimilarInfall', 'ShockPool', 'ShockTube', 'TestOrbit',
            'WavePool', 'ZeldovichPancake']
"""

testnames = ['AnisoConduction', 'CosmoIFront', 'DoubleMachReflection',
            'GravityTest', 'OneZoneFreefallTest', 'OrszagTang', 'PhotonShadowing',
            'SedovAMR', 'SelfSimilarInfall', 'ShockPool', 'ShockTube', 'TestOrbit',
            'WavePool', 'ZeldovichPancake']

print "The tests that will be run are: ", testnames, "\n\n"

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
        os.system('rm -rf DD* Enzo_Build* Evtime *out *log *Log RunFinished SphericalInfallReport sedov.in sedov*dat')
        
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

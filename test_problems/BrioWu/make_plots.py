from yt.mods import *
import matplotlib
import pylab
from yt.visualization._mpl_imports import FigureCanvasAgg

#Figure parameters
total_width = 36
total_height = 6
n_plots = 4
fontsize = 30

fig = matplotlib.figure.Figure((total_width,total_height), dpi=300)
fig.set_canvas(FigureCanvasAgg(fig))

#numbers from this point on are relative to the total
m_left = 0.05    #left margin
m_right = 0.01
m_bottom = 0.2  #bottom margin
m_top = 0.05
width = (1.-m_right)/(n_plots) - m_left
height_main = (1 - m_bottom - m_top) * 0.66
height_dx = 1-m_bottom - height_main - m_top
#ax_rho_d = fig.add_axes( [0.01, 0.01, 0.5, 0.5])  
#ax_rho_1 = fig.add_axes( [m_left,m_bottom+height_dx, width, height_main])

ax_main = []
ax_diff = []
for n_plot in range(n_plots):
    this_plot_left = m_left+n_plot*(m_left+width)
    extents_density_diff =  [this_plot_left,m_bottom,width,height_dx] 
    extents_density_main =  [this_plot_left,m_bottom+height_dx,width,height_main] 
    ax_diff.append(fig.add_axes( extents_density_diff )  )
    ax_main.append(fig.add_axes( extents_density_main) )
    ax_diff[-1].set_xlabel(r'$x$')

#
# fill plots
#

n=488
pf_ct = load('bw_ct_lowres/DD%04d/data%04d'%(n,n))
n=487
pf_de = load('bw_dedner_lowres/DD%04d/data%04d'%(n,n))
pf_ref= load('bw_highres/DD0122/data0122')

ray_ct = pf_ct.h.ortho_ray(0,[0.501]*2)
ray_de = pf_de.h.ortho_ray(0,[0.501]*2)
ray_ref = pf_ref.h.ortho_ray(0,[0.501]*2)

field = 'Density'
n_plot = 0
ax_main[n_plot].plot(ray_ct['x'],ray_de[field],c=[0.5]*3)
ax_main[n_plot].plot(ray_ref['x'],ray_ref[field],c=[0.2]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_ct[field],c='k',marker='.')
ax_diff[n_plot].plot(ray_ct['x'],(ray_ct[field]-ray_de[field]),c='k')
ax_main[n_plot].set_ylabel(r'$\rho$')
ax_main[n_plot].set_xticklabels([])
lll = na.arange(0.1,1.1,0.1)
ax_main[0].set_yticks(lll)
ax_main[0].set_xticks(x_ticks)
ax_main[0].set_yticklabels([r'$%0.1f$'%num for num in lll])

field = 'By'
n_plot = 1
ax_main[n_plot].plot(ray_ref['x'],ray_ref[field],c=[0.2]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_de[field],c=[0.5]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_ct[field],c='k',marker='.')
ax_diff[n_plot].plot(ray_ct['x'],(ray_ct[field]-ray_de[field]),c='k')
ax_main[n_plot].set_ylabel(r'$B_y$')
ax_main[n_plot].set_xticklabels([])
lll = na.arange(-4.0,5,1)
ax_main[1].set_yticks(lll)
ax_main[1].set_xticks(x_ticks)
ax_main[1].set_yticklabels([r'$%0.1f$'%num for num in lll])

field = 'Pressure'
n_plot = 2
ax_main[n_plot].plot(ray_ref['x'],ray_ref[field],c=[0.2]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_de[field],c=[0.5]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_ct[field],c='k',marker='.')
ax_diff[n_plot].plot(ray_ct['x'],(ray_ct[field]-ray_de[field]),c='k')
ax_main[n_plot].set_ylabel(r'$P$')
ax_main[n_plot].set_xticklabels([])
lll = na.arange(0.0, 1.4, 0.2)
ax_main[2].set_yticks(lll)
ax_main[2].set_xticks(x_ticks)
ax_main[2].set_yticklabels([r'$%0.1f$'%num for num in lll])

field = 'x-velocity'
n_plot = 3
ax_main[n_plot].plot(ray_ref['x'],ray_ref[field],c=[0.2]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_de[field],c=[0.5]*3)
ax_main[n_plot].plot(ray_ct['x'],ray_ct[field],c='k',marker='.')
ax_diff[n_plot].plot(ray_ct['x'],(ray_ct[field]-ray_de[field]),c='k')
ax_main[n_plot].set_ylabel(r'$v_x$')
ax_main[n_plot].set_xticklabels([])
lll = na.arange(-0.4,1.0,0.2)
ax_main[3].set_yticks(lll)
ax_main[3].set_xticks(x_ticks)
ax_main[3].set_yticklabels([r'$%0.1f$'%num for num in lll])

for ax in ax_diff:
    x_ticks = [0.1,0.5,0.9]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([r'$%0.1f$'%num for num in x_ticks])

    lll = [-0.05,0.0, 0.05]
    ax.set_ylim(-0.07,0.07)
    ax.set_yticks(lll)
    ax.set_yticklabels([r'$%0.2f$'%num for num in lll])




fname = 'BRIO.pdf'

pylab.rc('font',size=fontsize)
print fname
fig.savefig(fname)


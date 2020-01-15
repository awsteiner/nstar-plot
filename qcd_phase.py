import matplotlib.pyplot as plot

def default_plot(left_margin=0.14,bottom_margin=0.12,
                 right_margin=0.04,top_margin=0.04,fontsize=16,
                 fig_size_x=6.0,fig_size_y=6.0,ticks_in=False,
                 rt_ticks=False):
    """
    This function sets up the O\ :sub:`2`\ sclpy ``matplotlib``
    defaults. It returns a pair of objects, the figure object and axes
    object.

    This function is in ``utils.py``.
    """
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    fig=plot.figure(1,figsize=(fig_size_x,fig_size_y))
    fig.set_facecolor('white')
    ax=plot.axes([left_margin,bottom_margin,
                  1.0-left_margin-right_margin,1.0-top_margin-bottom_margin])
    ax.minorticks_on()
    if ticks_in:
        ax.tick_params('both',length=12,width=1,which='major',direction='in')
        ax.tick_params('both',length=5,width=1,which='minor',direction='in')
    else:
        ax.tick_params('both',length=12,width=1,which='major')
        ax.tick_params('both',length=5,width=1,which='minor')
    if rt_ticks:
        ax.tick_params('x',which='both',top=True,bottom=True)
        ax.tick_params('y',which='both',left=True,right=True)
    #ax.tick_params('both',length=5,width=1,which='minor')
    ax.tick_params(labelsize=fontsize*0.8)
    plot.grid(False)
    return (fig,ax)
    
(fig,ax)=default_plot(fig_size_x=8,fig_size_y=6,left_margin=0.12,fontsize=20)
ax.set_xlim(0,3000)
ax.set_ylim(0,200)
ax.set_xlabel(r'$ \mu_B~[\mathrm{MeV}]$',fontsize=20)
ax.set_ylabel(r'$ T~[\mathrm{MeV}]$',fontsize=20)

# From 200 to 1000
transition_x1=[200+i*8 for i in range(0,100)]
# From 200 to 3000
transition_x2=[200+i*28 for i in range(0,100)]
# From 0 to 140
transition_y=[(99-i)*1.4 for i in range(0,100)]

fill_region_x=[]
fill_region_y=[]
for i in range(0,len(transition_x1)):
    fill_region_x.append(transition_x1[i])
    fill_region_y.append(transition_y[i])
le=len(transition_x2)
for i in range(0,le):
    fill_region_x.append(transition_x2[le-1-i])
    fill_region_y.append(transition_y[le-1-i])
fill_region_x.append(transition_x1[0])
fill_region_y.append(transition_y[0])

ax.fill(fill_region_x,fill_region_y,color='blue',alpha=0.5)

plot.show()


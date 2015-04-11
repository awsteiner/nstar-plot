"""
-------------------------------------------------------------------

Copyright (C) 2015, Andrew W. Steiner

This is based on the excellent work by Dany Page at
http://www.astroscu.unam.mx/neutrones/home.html

This neutron star plot is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3 of
the License, or (at your option) any later version.

This neutron star plot is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this neutron star plot. If not, see
<http://www.gnu.org/licenses/>.

-------------------------------------------------------------------
"""

import math
from math import cos
from math import sin
from math import sqrt
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pylab import rand
import matplotlib.pyplot as plot

""" -------------------------------------------------------------------
Functions 
"""

# Default plot function from O2scl
def default_plot(lmar=0.14,bmar=0.12,rmar=0.04,tmar=0.04):
    plot.rc('text',usetex=True)
    plot.rc('font',family='serif')
    plot.rcParams['lines.linewidth']=0.5
    fig=plot.figure(1,figsize=(8.0,8.0))
    fig.set_facecolor('white')
    ax=plot.axes([lmar,bmar,1.0-lmar-rmar,1.0-tmar-bmar])
    ax.minorticks_on()
    ax.tick_params('both',length=12,width=1,which='major')
    ax.tick_params('both',length=5,width=1,which='minor')
    plot.grid(False)
    return (fig,ax)

"""
Cutaway function

Based on the polar form for an ellipse:

r = a b / sqrt( (b*cos(t))^2 + (a*sin(t))^2 )

"""
def cutaway(factor,cname):
    # Number of points per arc
    N2=100
    # Upper left part, from pi/2 to pi
    x=[]
    top_y=[]
    bot_y=[]
    ell_b=0.3*factor
    ell_a=0.1*factor
    for i in range(0,N2):
        angle=pi-float(i)/(N2-1)*(pi/2.0)
        r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
        x.append(0.5+r*cos(angle))
        top_y.append(0.5+r*sin(angle))
        if angle>pi*3.0/4.0:
            angle2=2*pi-angle
            bot_y.append(0.5+r*sin(angle2))
        else:
            bot_y.append(0.5+r*cos(angle))
        ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=2)
    # Upper right part, from 0 to pi/2
    x=[]
    top_y=[]
    bot_y=[]
    ell_b=0.3*factor
    ell_a=0.2*factor
    for i in range(0,N2):
        angle=pi/2-float(i)/(N2-1)*(pi/2)
        r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
        x.append(0.5+r*cos(angle))
        top_y.append(0.5+r*sin(angle))
        if angle>pi/8.0:
            bot_y.append(0.5-r*cos(angle)/4*1.5)
        else:
            bot_y.append(0.5+r*sin(-angle))
        ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=2)
    # Lower part, from 5*pi/4 to 15*pi/8
    x=[]
    top_y=[]
    bot_y=[]
    ell_b=0.1*factor
    ell_a=0.3*factor
    for i in range(0,N2):
        angle=5*pi/4+float(i)/(N2-1)*(5.02*pi/8)
        r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
        x.append(0.5+r*cos(angle))
        bot_y.append(0.5+r*sin(angle))
        if angle>3*pi/2:
            top_y.append(0.5-r*cos(angle)/4*1.5)
        else:
            top_y.append(0.5+r*cos(angle))
        ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=2)

# Initialize the plot, and make sure the limits are from (0,0) to (1,1)
def init():
    (fig,ax)=default_plot(0.0,0.0,0.0,0.0)
    plot.plot([0,0.01],[0,0.01],color='black',ls='-')
    plot.plot([0.99,1.0],[0.99,1.0],color='black',ls='-')
    return (fig,ax)

# Form the base black background
def bkgd(ax):
    # Black background
    bkgd=Rectangle((0,0),1,1)
    bkgd.set_facecolor('black')
    ax.add_artist(bkgd)

"""
Plot the magnetic field

This is a pure dipole field given by 

3 \vec{r} (m dot r)/r^5 - \vec{m}/r^3

"""
def mag_field(ax):
    mx=0.5
    my=-0.5
    fact=400
    N=10
    for i in range(0,N+1):
        for j in range(0,11):
            rx=-0.5+float(i)/N
            ry=-0.5+float(j)/N
            rmag=sqrt(rx*rx+ry*ry)
            if rmag>0.3:
                dot=mx*rx+my*ry
                Bx=(3*rx*dot/rmag**5-mx/rmag**3)/fact
                By=(3*ry*dot/rmag**5-my/rmag**3)/fact
                ax.arrow(rx+0.5+Bx,ry+0.5+By,-Bx,-By,
                         head_width=0.01,head_length=0.03,color='blue',
                         zorder=2)
    ang2=3*pi/4+0.1
    ax.arrow(0.5+0.2*cos(ang2),
             0.5+0.2*sin(ang2),
             0.23*cos(ang2),
             0.23*sin(ang2),
             head_width=0.01,head_length=0.03,color='cyan',
             zorder=2)
    ax.arrow(0.5+0.3*cos(ang2+pi),
             0.5+0.3*sin(ang2+pi),
             0.1*cos(ang2+pi),
             0.1*sin(ang2+pi),
             head_width=0.01,head_length=0.03,color='cyan',
             zorder=2)
    bkgdb=Rectangle((0.04,0.68),0.26,0.07,zorder=3)
    bkgdb.set_facecolor('black')
    ax.add_artist(bkgdb)
    ax.text(0.17,0.72,r'$B\sim 10^{7-16}~$G',
            fontsize=24,color='cyan',va='center',
            ha='center',zorder=4)

def base_star(ax):
    # Base star
    N=100
    ang=0
    for i in range(0,N):
        centx=0.5-float(i)*0.14/N
        centy=0.5+float(i)*0.14/N
        size1=0.6-float(i)*0.56/N
        size2=0.6-float(i)*0.56/N
        green=float(i)/N
        base=Ellipse((centx,centy),size1,size2,lw=0,angle=ang)
        base.set_facecolor((1,green,0))
        ax.add_artist(base)

def rotation(ax):
    ang3=3*pi/4-0.1
    ax.arrow(0.5+0.2*cos(ang3),
             0.5+0.2*sin(ang3),
             0.15*cos(ang3),
             0.15*sin(ang3),
             head_width=0.01,head_length=0.03,color=(0.2,0.8,0.2),
             zorder=2)
    ax.arrow(0.5+0.3*cos(ang3+pi),
             0.5+0.3*sin(ang3+pi),
             0.07*cos(ang3+pi),
             0.07*sin(ang3+pi),
             head_width=0.01,head_length=0.03,color=(0.2,0.8,0.2),
             zorder=2)
    bkgdb=Rectangle((0.085,0.80),0.33,0.07,zorder=3)
    bkgdb.set_facecolor('black')
    ax.add_artist(bkgdb)
    ax.text(0.25,0.84,r'$\omega=0.1-720~$Hz',
            fontsize=24,color=(0.2,0.8,0.2),va='center',
            ha='center',zorder=4)

def axes(ax):
    # axes
    linex=Line2D([0.5,0.5+0.21*cos(15*pi/8)],
                 [0.5,0.5+0.21*sin(15*pi/8)],color='black',ls='-',lw=1.5)
    ax.add_artist(linex)
    liney=Line2D([0.5,0.5],[0.5,0.8],color='black',ls='-',lw=1.5)
    ax.add_artist(liney)
    linez=Line2D([0.5,0.41],[0.5,0.41],color='black',ls='-',lw=1.5)
    ax.add_artist(linez)
    ax.text(0.51,0.44,r'$R{\approx}10-13$ km',rotation=-22.5,fontsize=20)

def cut_labels(ax):
    line1=Line2D([0.58,0.68],[0.78,0.93],color=atmos_color,ls='-',lw=1.5)
    ax.add_artist(line1)
    ax.text(0.69,0.92,'Atmosphere',fontsize=20,color=atmos_color,
            va='center',ha='left')
    line2=Line2D([0.59,0.68],[0.74,0.87],color=crust_color,ls='-',lw=1.5)
    ax.add_artist(line2)
    ax.text(0.69,0.87,'Crust',fontsize=20,color=crust_color,va='center',
            ha='left')
    line3=Line2D([0.62,0.68],[0.68,0.81],color=core_color,ls='-',lw=1.5)
    ax.add_artist(line3)
    ax.text(0.69,0.81,'Outer Core',fontsize=20,color=core_color,
            va='center',ha='left')
    line4=Line2D([0.60,0.68],[0.51,0.75],color=inner_color,ls='-',lw=1.5)
    ax.add_artist(line4)
    ax.text(0.69,0.75,'Inner Core',fontsize=20,color=inner_color,
            va='center',ha='left')

def title(ax):
    bkgd2=Rectangle((0.04,0.905),0.485,0.075,zorder=3)
    bkgd2.set_facecolor('black')
    ax.add_artist(bkgd2)
    ax.text(0.05,0.95,'A neutron star',fontsize=30,color='white',
            va='center',ha='left',zorder=4)

def pasta_box(ax):
    box_bkgd=Rectangle((0.01,0.01),0.5,0.3,zorder=3,color='white',lw=1.5)
    ax.add_artist(box_bkgd)
    line5=Line2D([0.01,0.408],[0.31,0.5],color='white',ls='--',lw=1.5)
    ax.add_artist(line5)
    line6=Line2D([0.51,0.412],[0.31,0.5],color='white',ls='--',lw=1.5)
    ax.add_artist(line6)
    bkgd3=Rectangle((0.41,0.01),0.1,0.3,zorder=3,lw=0)
    bkgd3.set_facecolor(core_color)
    ax.add_artist(bkgd3)
    bkgd4=Rectangle((0.01,0.01),0.2,0.3,zorder=3,lw=0)
    bkgd4.set_facecolor(crust_color)
    ax.add_artist(bkgd4)
    bkgd5=Rectangle((0.21,0.01),0.2,0.3,zorder=3,lw=0)
    bkgd5.set_facecolor(neutron_color)
    ax.add_artist(bkgd5)
    ax.text(0.45,0.12,'Core',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.05,0.12,'Outer',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.09,0.12,'Crust',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.20,0.12,'neutron drip',fontsize=16,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.25,0.12,'Inner',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.29,0.12,'Crust',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.38,0.12,'Pasta',fontsize=20,color='black',rotation='90',
            va='center',ha='center',zorder=5)
    ax.text(0.08,0.24,'g/cm$^{3}$:',fontsize=20,color='black',
            va='bottom',ha='center',zorder=5)
    ax.text(0.18,0.25,'$10^{11}$',fontsize=20,color='black',
            va='bottom',ha='center',zorder=5)
    ax.text(0.39,0.25,'$10^{14}$',fontsize=20,color='black',
            va='bottom',ha='center',zorder=5)
    for j in range(0,20):
        for i in range(0,j+2):
            nuc1=Ellipse((0.02+float(j)*0.02,rand()*0.3+0.01),0.01,0.01,
                         zorder=4,lw=0)
            nuc1.set_facecolor(core_color)
            ax.add_artist(nuc1)
    for i in range(0,60):
        pasta1=Ellipse((0.40-0.1*rand()*rand(),rand()*0.28+0.02),0.01,0.04,
                       angle=rand()*360,zorder=4,lw=0)
        pasta1.set_facecolor(core_color)
        ax.add_artist(pasta1)
    for i in range(0,20):
        pasta2=Ellipse((0.41-0.02*rand()*rand(),rand()*0.28+0.02),0.01,0.06,
                       angle=rand()*30,zorder=4,lw=0)
        pasta2.set_facecolor(core_color)
        ax.add_artist(pasta2)
        
""" -------------------------------------------------------------------
Main plotting code
"""

pi=math.acos(-1)
atmos_color='red'
crust_color=(1.0,0.5,0.5)
core_color=(0.75,0.75,1.0)
inner_color=(0.5,0.5,1.0)
neutron_color=(0.875,0.625,0.75)

(fig,ax)=init()
bkgd(ax)
mag_field(ax)
base_star(ax)
rotation(ax)
axes(ax)

cutaway(1.0,atmos_color)
cutaway(0.98,crust_color)
cutaway(0.9,core_color)
cutaway(0.5,inner_color)
cut_labels(ax)

pasta_box(ax)

title(ax)

bkgdm=Rectangle((0.71,0.04),0.27,0.13,zorder=3)
bkgdm.set_facecolor('black')
ax.add_artist(bkgdm)
ax.text(0.85,0.125,r'$M_{\mathrm{min}}{\approx}1\mathrm{M}_{\odot}$',
        fontsize=20,color='white',va='center',
        ha='center',zorder=4)
ax.text(0.85,0.075,r'$M_{\mathrm{max}}>2\mathrm{M}_{\odot}$',
        fontsize=20,color='white',va='center',
        ha='center',zorder=4)

plot.savefig('nstar_plot.png')
plot.savefig('nstar_plot.eps')
plot.show()

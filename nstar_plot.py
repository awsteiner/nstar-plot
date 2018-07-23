"""
-------------------------------------------------------------------

Copyright (C) 2015-2018, Andrew W. Steiner

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

import os
import math
from math import cos
from math import sin
from math import sqrt
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
from pylab import rand
import matplotlib.pyplot as plot
import numpy
import os
import urllib.request
import o2sclpy
from load_crust import load_crust

update_plot_files=False

class nstar_plot(load_crust):

    pi=math.acos(-1)
    # Default text color
    text_color='white'
    # Background color
    bkgd_color='black'
    # Color for atmosphere
    atmos_color='red'
    # Color for crust
    crust_color=(1.0,0.5,0.5)
    # Color for outer core
    core_color=(0.75,0.75,1.0)
    # Color for inner core
    inner_color=(0.5,0.5,1.0)
    # Color for neutron drip
    neutron_color=(0.875,0.625,0.75)
    # Figure object
    fig=0
    # Axis object
    ax=0
    # Font scaling parameter (default 20)
    font_scale=20

    """
    Initialize the plot, and make sure the limits are from (0,0) 
    to (1,1) by plotting a couple small lines.
    """
    def init(self):
        (self.fig,self.ax)=o2sclpy.default_plot(0.0,0.0,0.0,0.0)
        plot.xlim([0,1])
        plot.ylim([0,1])
        #plot.plot([0,0.01],[0,0.01],color=self.bkgd_color,ls='-')
        #plot.plot([0.99,1.0],[0.99,1.0],color=self.bkgd_color,ls='-')

    # Form the base black background
    def bkgd(self):
        # Black background
        main_bkgd=Rectangle((0,0),1,1)
        main_bkgd.set_facecolor(self.bkgd_color)
        self.ax.add_artist(main_bkgd)

    """
    The star's surface, red and yellow, created from a series of 
    circles
    """
    def base_star(self):
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
            self.ax.add_artist(base)
            
    """
    Plot the magnetic field
    
    This is a pure dipole field given by 
    
    \vec{B} = 3 \vec{r} (m dot r)/r^5 - \vec{m}/r^3
    """
    def mag_field(self,ord):
        mx=0.5
        my=-0.5
        fact=400
        N=10
        # vector field
        for i in range(0,N+1):
            for j in range(0,11):
                rx=-0.5+float(i)/N
                ry=-0.5+float(j)/N
                rmag=sqrt(rx*rx+ry*ry)
                if rmag>0.3:
                    dot=mx*rx+my*ry
                    Bx=(3*rx*dot/rmag**5-mx/rmag**3)/fact
                    By=(3*ry*dot/rmag**5-my/rmag**3)/fact
                    self.ax.arrow(rx+0.5+Bx,ry+0.5+By,-Bx,-By,
                             head_width=0.01,head_length=0.03,color='blue',
                             zorder=ord)
        # Arrow for magnetic north
        ang2=3*self.pi/4+0.1
        self.ax.arrow(0.5+0.2*cos(ang2),
                      0.5+0.2*sin(ang2),
                      0.23*cos(ang2),
                      0.23*sin(ang2),
                      head_width=0.01,head_length=0.03,color='cyan',
                      zorder=ord)
        # Arrow for magnetic south
        self.ax.arrow(0.5+0.4*cos(ang2+self.pi),
                      0.5+0.4*sin(ang2+self.pi),
                      -0.1/1.414*cos(ang2+self.pi),
                      -0.1/1.414*sin(ang2+self.pi),
                      head_width=0.01,head_length=0.03,color='cyan',
                      zorder=ord)
        """
        Label for B field magnitude
        
        B=2e15 for SGR 1806-20 from Woods et al. (2006),
        http://dx.doi.org/10.1086/507459 .

        B=10^7 is estimate from P-Pdot diagrams, e.g.
        from arxiv.org/abs/1103.4538 
        """
        self.ax.text(0.22,0.72,
                     r'$B_{\mathrm{surf}}\sim 10^{7-15}~\mathrm{G}$',
                     fontsize=self.font_scale,color='cyan',va='center',
                     ha='center',zorder=ord+1,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))

    """
    Cutaway function
    
    Based on the polar form for an ellipse:
    r = a b / sqrt( (b*cos(t))^2 + (a*sin(t))^2 )
    where a is the radius in the x direction and b is the radius in
    the y direction.
    """
    def cutaway(self,factor,cname,ord):
        # Number of points per arc
        N2=100
        # Upper left part, from pi/2 to pi
        x=[]
        top_y=[]
        bot_y=[]
        ell_b=0.3*factor
        ell_a=0.1*factor
        for i in range(0,N2):
            angle=self.pi-float(i)/(N2-1)*(self.pi/2.0)
            r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
            x.append(0.5+r*cos(angle))
            top_y.append(0.5+r*sin(angle))
            if angle>self.pi*3.0/4.0:
                angle2=2*self.pi-angle
                bot_y.append(0.5+r*sin(angle2))
            else:
                bot_y.append(0.5+r*cos(angle))
        self.ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=ord)

        # Upper right part, from 0 to pi/2
        x=[]
        top_y=[]
        bot_y=[]
        ell_b=0.3*factor
        ell_a=0.2*factor
        for i in range(0,N2):
            angle=self.pi/2-float(i)/(N2-1)*(self.pi/2)
            r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
            x.append(0.5+r*cos(angle))
            top_y.append(0.5+r*sin(angle))
            if angle>self.pi/8.0:
                bot_y.append(0.5-r*cos(angle)/4*1.5)
            else:
                bot_y.append(0.5+r*sin(-angle))
        self.ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=ord)

        # Lower part, from 5*pi/4 to 15*pi/8
        x=[]
        top_y=[]
        bot_y=[]
        ell_b=0.1*factor
        ell_a=0.3*factor
        for i in range(0,N2):
            angle=5*self.pi/4+float(i)/(N2-1)*(5.02*self.pi/8)
            r=ell_a*ell_b/sqrt((ell_b*cos(angle))**2+(ell_a*sin(angle))**2)
            x.append(0.5+r*cos(angle))
            bot_y.append(0.5+r*sin(angle))
            if angle>3*self.pi/2:
                top_y.append(0.5-r*cos(angle)/4*1.5)
            else:
                top_y.append(0.5+r*cos(angle))
        self.ax.fill_between(x,bot_y,top_y,facecolor=cname,lw=0,zorder=ord)

    """
    Arrows and label for rotation

    716 Hz from Hessels et al. (2006), 
    http://dx.doi.org/10.1126/science.1123430 .

    1/11.79 Hz from Rim and Kaspi (2014),
    http://dx.doi.org/10.1088/0004-637X/784/1/37 .
    
    Now 4.2e-5 Hz from D'Ai et al. (2016),
    http://dx.doi.org/10.1093/mnras/stw2023
    """
    def rotation(self,ord):
        ang3=3*self.pi/4-0.1
        self.ax.arrow(0.5+0.2*cos(ang3),0.5+0.2*sin(ang3),
                      0.15*cos(ang3),0.15*sin(ang3),
                      head_width=0.01,head_length=0.03,color=(0.2,0.8,0.2),
                      zorder=ord)
        self.ax.arrow(0.5+0.3*cos(ang3+self.pi),
                      0.5+0.3*sin(ang3+self.pi),
                      0.07*cos(ang3+self.pi),
                      0.07*sin(ang3+self.pi),
                      head_width=0.01,head_length=0.03,color=(0.2,0.8,0.2),
                      zorder=ord)
        self.ax.text(0.30,0.84,
                     r'$\mathrm{freq.}=4.2\times 10^{-5}-720~\mathrm{Hz}$',
                     fontsize=self.font_scale,color=(0.2,0.8,0.2),va='center',
                     ha='center',zorder=ord+1,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))

    """
    Axes for the cutaway
    
    Radius range from Steiner, et al. (2016)
    http://dx.doi.org/10.1088/2041-8205/765/1/L5
    """
    def cutaway_axes(self,ord):
        # axes
        plot.plot([0.5,0.5+0.21*cos(15*self.pi/8)],
                  [0.5,0.5+0.21*sin(15*self.pi/8)],
                  color='black',ls='-',lw=1.5,zorder=ord)
        plot.plot([0.5,0.5],[0.5,0.8],color='black',ls='-',lw=1.5,
                  zorder=ord)
        plot.plot([0.5,0.41],[0.5,0.41],color='black',ls='-',lw=1.5,
                  zorder=ord)
        self.ax.text(0.51,0.44,r'$R{\approx}10-13$ km',
                     rotation=-22.5,fontsize=self.font_scale*0.8,zorder=ord)

    """
    Labels for the cutaway
    """
    def cut_labels(self,ord):
        self.ax.text(0.69,0.95,'Atmos.: H, He, C',fontsize=self.font_scale*0.7,
                     color=self.atmos_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.90,'Outer Crust',fontsize=self.font_scale*0.7,
                     color=self.crust_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.85,'(Z,N)+e',fontsize=self.font_scale*0.7,
                     color=self.crust_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.80,'Inner crust',fontsize=self.font_scale*0.7,
                     color=self.crust_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.75,'(Z,N)+e+n',fontsize=self.font_scale*0.7,
                     color=self.crust_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.70,'Outer Core: n+p+e',fontsize=self.font_scale*0.7,
                     color=self.core_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.69,0.65,'Inner Core: ?',fontsize=self.font_scale*0.7,
                     color=self.inner_color,va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        plot.plot([0.58,0.68],[0.78,0.95],
                     color=self.atmos_color,ls='-',lw=1.5,zorder=ord)
        plot.plot([0.59,0.68],[0.74,0.82],
                     color=self.crust_color,ls='-',lw=1.5,zorder=ord)
        plot.plot([0.62,0.68],[0.68,0.70],
                     color=self.core_color,ls='-',lw=1.5,zorder=ord)
        plot.plot([0.60,0.68],[0.51,0.65],
                     color=self.inner_color,ls='-',lw=1.5,zorder=ord)

    """
    Box showing crust
    """
    def crust_box(self,ord):
        # Dashed lines to show zoom
        plot.plot([0.01,0.408],[0.31,0.5],color='white',
                  ls='--',lw=1.5,zorder=ord)
        plot.plot([0.51,0.412],[0.31,0.5],color='white',
                  ls='--',lw=1.5,zorder=ord)
        # Boxes to provide background
        box_bkgd1=Rectangle((0.01,0.01),0.5,0.3,zorder=ord,
                            color='white',lw=1.5)
        self.ax.add_artist(box_bkgd1)
        box_bkgd2=Rectangle((0.41,0.01),0.1,0.3,zorder=ord,lw=0)
        box_bkgd2.set_facecolor(self.core_color)
        self.ax.add_artist(box_bkgd2)
        box_bkgd3=Rectangle((0.01,0.01),0.2,0.3,zorder=ord,lw=0)
        box_bkgd3.set_facecolor(self.crust_color)
        self.ax.add_artist(box_bkgd3)
        box_bkgd4=Rectangle((0.21,0.01),0.2,0.3,zorder=ord,lw=0)
        box_bkgd4.set_facecolor(self.neutron_color)
        self.ax.add_artist(box_bkgd4)
        # Nuclei
        for j in range(0,20):
            shift=rand()*0.02
            if j%2==0:
                shift=shift+0.15/float(j+2)
            for i in range(0,j+2):
                y=0.3*float(i)/float(j+2)+0.01+shift
                if y>0.30:
                    y=0.30
                nuc1=Ellipse((0.02+float(j)*0.02,y),
                             0.01,0.01,zorder=ord+1,lw=0)
                nuc1.set_facecolor(self.core_color)
                self.ax.add_artist(nuc1)
        # Pasta
        for i in range(0,60):
            y=0.3*float(i)/60.0
            if (y<0.03):
                y=0.03
            pasta1=Ellipse((0.40-0.1*rand()*rand(),y),
                           0.01,0.04,angle=rand()*360,zorder=ord+1,lw=0)
            pasta1.set_facecolor(self.core_color)
            self.ax.add_artist(pasta1)
        # Thinner pasta
        for i in range(0,20):
            y=0.3*float(i)/20.0
            if (y<0.04):
                y=0.04
            pasta2=Ellipse((0.415-0.04*rand()*rand(),y),
                           0.01,0.06,angle=rand()*60-30,zorder=ord+1,lw=0)
            pasta2.set_facecolor(self.core_color)
            self.ax.add_artist(pasta2)
        # Labels
        self.ax.text(0.05,0.12,'Outer',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        self.ax.text(0.09,0.12,'Crust',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        self.ax.text(0.21,0.12,'neutron drip',fontsize=self.font_scale*0.6,color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        self.ax.text(0.25,0.12,'Inner',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.neutron_color,lw=0))
        self.ax.text(0.29,0.12,'Crust',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.neutron_color,lw=0))
        self.ax.text(0.38,0.12,'Pasta',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.core_color,lw=0))
        self.ax.text(0.45,0.12,'Core',fontsize=self.font_scale*0.8,
                     color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2)
        # Density labels
        self.ax.text(0.08,0.24,'g/cm$^{3}$:',fontsize=self.font_scale*0.8,
                     color='black',
                     va='bottom',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        self.ax.text(0.18,0.25,'$10^{11}$',fontsize=self.font_scale*0.8,
                     color='black',
                     va='bottom',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        self.ax.text(0.39,0.25,'$10^{14}$',fontsize=self.font_scale*0.8,
                     color='black',
                     va='bottom',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.core_color,lw=0))
        # Crust thickness label
        self.ax.text(0.26,0.335,
                     '$R_{\mathrm{crust}}=0.4-2.0~\mathrm{km}$',
                     fontsize=self.font_scale*0.8,color=self.text_color,
                     va='center',ha='center',zorder=13,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))

    """
    Generic function to reformat a float as a latex string
    """
    def latex_float(self,f):
        float_str = "{0:.2g}".format(f)
        if "e" in float_str:
            base, exponent = float_str.split("e")
            return r"${0} \times 10^{{{1}}}$".format(base, int(exponent))
        else:
            return float_str    
    
    """
    Crust structure from SLy4 model in Steiner (2012)
    http://dx.doi.org/10.1103/PhysRevC.85.055804
    """
    def crust_box2(self,ord):
        # Dashed lines to show zoom
        plot.plot([0.01,0.408],[0.31,0.5],color='white',
                  ls='--',lw=1.5,zorder=ord)
        plot.plot([0.52,0.412],[0.31,0.5],color='white',
                  ls='--',lw=1.5,zorder=ord)
        
        # Load crust in parent class
        self.load()
            
        # Set up inner crust axes
        ax_ic=self.fig.add_axes([0.28,0.01,0.24,0.3],
                                facecolor=(1.0,0.5,0.5))
        ax_ic.minorticks_on()
        ax_ic.tick_params('both',length=12,width=1,which='major')
        ax_ic.tick_params('both',length=5,width=1,which='minor')
        ax_ic.set_yticks([])
        ax_ic.set_xticks([10.8,10.9,11.0,11.1,11.2,11.3])
        ax_ic.set_xticklabels(['','','','','',''])
        ax_ic.set_xlim([numpy.max(self.r_nnuc),numpy.min(self.r_nnuc)])
        ax_ic.set_ylim([0,1])
        
        ctr=0
        for label in ax_ic.get_xticklabels():
            t=label.get_position()
            if ctr%2==0:
                t2=t[0],t[1]+0.18
            else:
                t2=t[0],t[1]+0.26
            if ctr==0:
                t2=t[0]+0.05,t[1]
            label.set_position(t2)
            label.set_fontsize(16)
            ctr+=1
        
        # Plot inner crust
        ax_ic.plot(self.r_nn,self.w_nn,marker='o',lw=0,mfc=(0.9,0.9,1.0),
          mec=(0.9,0.9,1.0),mew=0.0,ms=2.0)
        for i in range(0,len(self.r_nnuc)):
            ax_ic.plot(self.r_nnuc[i],self.w_nnuc[i],
                  marker='.',lw=0,mfc=(0.75,0.75,1.0),
                      mec=(0.75,0.75,1.0),
                  ms=self.Rn_nnuc[i])

        ax_ic.text(10.9,0.2,'10.9',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_ic.text(11.0,0.115,'11.0',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_ic.text(11.1,0.2,'11.1',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_ic.text(11.2,0.115,'11.2',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_ic.text(11.27,0.2,'11.3',fontsize=self.font_scale*0.6,
          va='center',ha='center')
            
        #ax_ic.text(10.8,0.9,self.latex_float(rho_108),
        #fontsize=self.font_scale*0.6,
        #  va='top',ha='center',rotation=90)
        
        ax_ic.text(10.9,0.9,self.latex_float(self.rho_109),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_ic.text(11.0,0.9,self.latex_float(self.rho_110),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_ic.text(11.1,0.9,self.latex_float(self.rho_111),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_ic.text(11.2,0.9,self.latex_float(self.rho_112),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_ic.text(11.3,0.9,self.latex_float(self.rho_113),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        
        # Inner crust labels
        ax_ic.text(10.84,0.4,'pasta',fontsize=self.font_scale*0.6,color='black',
                     rotation='90',va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        ax_ic.text(11.08,0.35,'inner crust',
                   fontsize=self.font_scale*0.6,color='black',
                     va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))

        # Set up outer crust axes
        ax_oc=self.fig.add_axes([0.01,0.01,0.24,0.3],
                                facecolor=(1.0,0.5,0.5))
        ax_oc.minorticks_on()
        ax_oc.tick_params('both',length=12,width=1,which='major')
        ax_oc.tick_params('both',length=5,width=1,which='minor')
        ax_oc.set_xlim([numpy.max(self.r_nnuc_outer),
                        numpy.min(self.r_nnuc_outer)]) 
        ax_oc.set_ylim([0,1])
        ax_oc.set_xticks([11.4,11.5,11.6,11.7])
        ax_oc.set_xticklabels(['','','',''])
        ax_oc.set_yticks([])
        
        # Plot outer crust
        for i in range(0,len(self.r_nnuc)):
            ax_oc.plot(self.r_nnuc_outer[i],self.w_nnuc_outer[i],
                       marker='.',lw=0,mfc=(0.75,0.75,1.0),
                       mec=(0.75,0.75,1.0),
                       ms=self.Rn_nnuc_outer[i])
        
        for label in ax_oc.get_xticklabels():
            t=label.get_position()
            t2=t[0],t[1]+0.18
            label.set_position(t2)
            label.set_fontsize(16)

        ax_oc.text(11.65,0.2,'11.7 km',fontsize=self.font_scale*0.6,
          va='center',ha='center')
        ax_oc.text(11.41,0.115,'11.4',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_oc.text(11.5,0.2,'11.5',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        ax_oc.text(11.6,0.115,'11.6',fontsize=self.font_scale*0.6,
          va='center',ha='center') 
        
        ax_oc.text(11.4,0.9,self.latex_float(self.rho_114),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_oc.text(11.5,0.9,self.latex_float(self.rho_115),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_oc.text(11.6,0.9,self.latex_float(self.rho_116),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        ax_oc.text(11.69,0.9,r'$\rho=$'+self.latex_float(self.rho_117),
                   fontsize=self.font_scale*0.6,
          va='top',ha='center',rotation=90)
        
        # Outer crust labels
        plot.text(11.52,0.33,r'$\Leftarrow$ outer crust',
                  fontsize=self.font_scale*0.6,color='black',
                     va='center',ha='center',zorder=ord+2,
                     bbox=dict(facecolor=self.crust_color,lw=0))
        
        ax_oc.text(11.35,0.5,'neutron drip',fontsize=self.font_scale*0.6,
                   color='black',
                   rotation='90',va='center',ha='center',zorder=ord+2,
                   bbox=dict(facecolor=self.crust_color,lw=0))
        
        return
        
    """
    Box for various properties
    
    These limits are from Steiner et al. (2015)
    http://dx.doi.org/10.1103/PhysRevC.91.015804
    """
    def mass_limits(self,ord):
        self.ax.text(0.58,0.225,
                     (r'$\lambda=(0.2-6){\times}10^{36}~'+
                      r'\mathrm{g}~\mathrm{cm}^2~\mathrm{s}^2$'),
                     fontsize=self.font_scale*0.7,
                     color=self.text_color,va='center',
                     ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.58,0.175,
                     r'$I=50-200~\mathrm{M}_{\odot}~\mathrm{km}^2$',
                     fontsize=self.font_scale*0.7,
                     color=self.text_color,va='center',
                     ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.58,0.125,(r'$\varepsilon_{\mathrm{core}}='+
                                 r'500-1600~\mathrm{MeV}/\mathrm{fm}^{3}$'),
                     fontsize=self.font_scale*0.7,
                     color=self.text_color,va='center',
                     ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.58,0.075,(r'$n_{B,\mathrm{max}}='+
                                 r'0.6-1.3~\mathrm{fm}^{-3}$'),
                     fontsize=self.font_scale*0.7,
                     color=self.text_color,va='center',
                     ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
        self.ax.text(0.58,0.025,
                     (r'$M_{\mathrm{min}}{\approx}1\mathrm{M}_{\odot}$ ;'+
                      r' $M_{\mathrm{max}}>2\mathrm{M}_{\odot}$'),
                     fontsize=self.font_scale*0.7,
                     color=self.text_color,va='center',
                     ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))
            
    """
    Plot title on upper left
    """
    def title(self,ord):
        self.ax.text(0.05,0.95,'A neutron star',
                     fontsize=30,color=self.text_color,
                     va='center',ha='left',zorder=ord,
                     bbox=dict(facecolor=self.bkgd_color,lw=0))

    """ -------------------------------------------------------------------
    Main plotting function
    """
    def run(self):
        self.init()
        self.bkgd()
        self.base_star()
        self.mag_field(2)
        self.rotation(2)
        self.cutaway(1.0,self.atmos_color,5)
        self.cutaway(0.98,self.crust_color,6)
        self.cutaway(0.9,self.core_color,7)
        self.cutaway(0.5,self.inner_color,8)
        self.cutaway_axes(9)
        self.cut_labels(9)
        self.crust_box2(10)
        self.mass_limits(13)
        self.title(15)

np=nstar_plot()
np.run()
if update_plot_files==True:
    plot.savefig('nstar_plot.eps')
    """
    Unfortunately the cutaway fills don't render properly on png
    output for some backends, so I use imagemagick to make .png
    instead.
    """
    os.system('convert nstar_plot.eps nstar_plot.png')
plot.show()

# np.init()
# np.bkgd()
# np.base_star()
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage1.eps')

# np.init()
# np.bkgd()
# np.base_star()
# np.cutaway(1.0,np.atmos_color,5)
# np.cutaway(0.98,np.crust_color,6)
# np.cutaway(0.9,np.core_color,7)
# np.cutaway(0.5,np.inner_color,8)
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage2.eps')

# np.init()
# np.bkgd()
# np.base_star()
# np.cutaway(1.0,np.atmos_color,5)
# np.cutaway(0.98,np.crust_color,6)
# np.cutaway(0.9,np.core_color,7)
# np.cutaway(0.5,np.inner_color,8)
# np.cutaway_axes(9)
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage3.eps')

# np.init()
# np.bkgd()
# np.base_star()
# np.cutaway(1.0,np.atmos_color,5)
# np.cutaway(0.98,np.crust_color,6)
# np.cutaway(0.9,np.core_color,7)
# np.cutaway(0.5,np.inner_color,8)
# np.cutaway_axes(9)
# np.cut_labels(9)
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage4.eps')

# np.init()
# np.bkgd()
# np.base_star()
# np.cutaway(1.0,np.atmos_color,5)
# np.cutaway(0.98,np.crust_color,6)
# np.cutaway(0.9,np.core_color,7)
# np.cutaway(0.5,np.inner_color,8)
# np.cutaway_axes(9)
# np.cut_labels(9)
# np.crust_box2(10)
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage5.eps')

# np.init()
# np.bkgd()
# np.base_star()
# np.mag_field(2)
# np.rotation(2)
# np.cutaway(1.0,np.atmos_color,5)
# np.cutaway(0.98,np.crust_color,6)
# np.cutaway(0.9,np.core_color,7)
# np.cutaway(0.5,np.inner_color,8)
# np.cutaway_axes(9)
# np.cut_labels(9)
# np.crust_box2(10)
# np.title(15)
# if update_plot_files==True:
#     plot.savefig('nstar_plot_stage6.eps')

# if update_plot_files==True:
#     os.system('convert nstar_plot_stage1.eps nstar_plot_stage1.png')
#     os.system('convert nstar_plot_stage2.eps nstar_plot_stage2.png')
#     os.system('convert nstar_plot_stage3.eps nstar_plot_stage3.png')
#     os.system('convert nstar_plot_stage4.eps nstar_plot_stage4.png')
#     os.system('convert nstar_plot_stage5.eps nstar_plot_stage5.png')
#     os.system('convert nstar_plot_stage6.eps nstar_plot_stage6.png')    

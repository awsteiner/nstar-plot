"""
-------------------------------------------------------------------

Copyright (C) 2015-2020, Andrew W. Steiner

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

import h5py
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plot
import o2sclpy
import os

""" -------------------------------------------------------------------
Class definition
"""
class eos_mvsr_plot:
    
    # Main run()
    def run(self):

        pb.xlimits(0,1)
        pb.ylimits(0,1)

        self.link=o2sclpy.linker()
        self.link.link_o2scl()

        pb.subplots(2,1)
        pb.fig.subplots_adjust(wspace=0.27,left=0.10,right=0.98,
                               bottom=0.15,top=0.97)

        ax1=pb.axes_dict['subplot0']
        ax2=pb.axes_dict['subplot1']
        ax1.minorticks_on()
        ax1.tick_params('both',length=10,width=1,which='major')
        ax1.tick_params('both',length=5,width=1,which='minor')
        ax1.tick_params(labelsize=20)
        ax2.minorticks_on()
        ax2.tick_params('both',length=10,width=1,which='major')
        ax2.tick_params('both',length=5,width=1,which='minor')
        ax2.tick_params(labelsize=20)
        pb.fig.set_facecolor('white')

        hf=o2sclpy.hdf_file(self.link)
        hf.open('eos_mvsr.o2')
        name=o2sclpy.std_string(self.link)
        name.init_bytes(b'eos')
        tab=o2sclpy.table(self.link)
        o2sclpy.hdf_input_n_table(self.link,hf,nn_tab,name)
        hf.close()
        
        # Convert to MeV/fm^3
        ed2=[tab['ed'][i]*197.33 for i in 
             range(0,len(tab['ed']))]
        pr2=[tab['pr'][i]*197.33 for i in 
             range(0,len(tab['pr']))]
        ax1.set_ylim([1.0e-1,1.0e3])
        ax1.set_xlim([0,1600])
        ax1.semilogy(ed2,pr2,lw=2)
        ax1.text(0.5,-0.12,
                      r'$\varepsilon~(\mathrm{MeV}/\mathrm{fm}^3)$',
                      fontsize=24,va='center',ha='center',
                      transform=ax1.transAxes)
        ax1.text(-0.2,0.5,
                      r'$P~(\mathrm{MeV}/\mathrm{fm}^3)$',
                      fontsize=24,va='center',ha='center',
                      transform=ax1.transAxes,rotation=90)
        dset=h5r.h5read_type_named('eos_mvsr.o2','table','mvsr')
        ax2.set_ylim([0.0,2.1])
        ax2.set_xlim([8,24])
        ax2.plot(tab['r'],tab['gm'],lw=2)
        ax2.text(0.5,-0.12,'$R~(\mathrm{km})$',
                      fontsize=24,va='center',ha='center',
                      transform=ax2.transAxes)
        ax2.text(-0.2,0.6,'$M~(\mathrm{M}_{\odot})$',
                      fontsize=24,va='center',ha='center',
                      transform=ax2.transAxes,rotation=90)
        #
        pb.fig.text(0.42,0.37,(r'$\leftarrow \stackrel{\frac{dP}{dr}='+
                                 r'-\frac{G m \varepsilon}'+
                                 r'{r^2}\left(1+\frac{P}{\varepsilon}\right)'+
                                 r'\left(1+\frac{4 \pi P r^3}{m}\right)'+
                                 r'\left(1-\frac{2 G m}{r}\right)^{-1}}'+
                                 r'{\scriptstyle{1-1~~'+
                                 r'\mathrm{correspondence}}}'+
                                 r'\rightarrow$'),
                      fontsize=28,va='center',ha='center',
                      zorder=10,
                      bbox=dict(facecolor=(0.75,0.75,1.0),lw=0))
        plot.savefig('eos_mvsr.pdf')
        plot.show()

""" -------------------------------------------------------------------
Create the plot
"""

em=eos_mvsr_plot()
em.run()

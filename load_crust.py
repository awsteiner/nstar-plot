"""
-------------------------------------------------------------------

Copyright (C) 2015-2016, Andrew W. Steiner

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

import o2sclpy
import numpy
    
class load_crust:

    # Crust data
    w_nn=[]
    r_nn=[]

    w_nnuc=[]
    r_nnuc=[]
    Rn_nnuc=[]
    A_nnuc=[]
    nb_nnuc=[]

    w_nnuc_outer=[]
    r_nnuc_outer=[]
    Rn_nnuc_outer=[]
    A_nnuc_outer=[]
    nb_nnuc_outer=[]

    rho_108=0
    rho_109=0
    rho_110=0
    rho_111=0
    rho_112=0
    rho_113=0

    rho_114=0
    rho_115=0
    rho_116=0
    rho_117=0

    def load(self):
    
        # Read inner crust data for neutrons
        if len(self.w_nn)==0:
            hr=o2sclpy.hdf5_reader()
            (nn_tab,loc_type)=hr.h5read_name('inner_nn.o2',
                                             'inner_nn')
            self.w_nn=nn_tab['data/w']
            self.r_nn=nn_tab['data/r']
            self.w_nn=self.w_nn[:100000]
            self.r_nn=self.r_nn[:100000]
            print('Loaded',len(self.w_nn),'nucleons.')
            
        # Read inner crust data for nuclei
        if len(self.w_nnuc)==0:
            (nnuc_tab,loc_type)=hr.h5read_name('inner_nnuc.o2',
                                               'inner_nnuc')
            self.w_nnuc=nnuc_tab['data/w']
            self.r_nnuc=nnuc_tab['data/r']
            self.Rn_nnuc=nnuc_tab['data/Rn']
            self.A_nnuc=nnuc_tab['data/A']
            self.nb_nnuc=nnuc_tab['data/nb']
            
            nb_nnuc_temp=[abs(self.r_nnuc[i]-10.8)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_108=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            nb_nnuc_temp=[abs(self.r_nnuc[i]-10.9)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_109=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            nb_nnuc_temp=[abs(self.r_nnuc[i]-11.0)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_110=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            nb_nnuc_temp=[abs(self.r_nnuc[i]-11.1)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_111=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            nb_nnuc_temp=[abs(self.r_nnuc[i]-11.2)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_112=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            nb_nnuc_temp=[abs(self.r_nnuc[i]-11.3)
                          for i in range(0,len(self.r_nnuc))]
            self.rho_113=self.nb_nnuc[numpy.argmin(nb_nnuc_temp)]*2.8e14/0.16
            
            print('Loaded',len(self.w_nnuc),
                  'nuclei for inner crust.')


        # Read outer crust data for nuclei
        if len(self.w_nnuc_outer)==0:
            hr=o2sclpy.hdf5_reader()
            (nnuc_tab_outer,loc_type)=hr.h5read_name('outer_nnuc.o2',
                                                     'outer_nnuc')
            self.w_nnuc_outer=nnuc_tab_outer['data/w']
            self.r_nnuc_outer=nnuc_tab_outer['data/r']
            self.Rn_nnuc_outer=nnuc_tab_outer['data/Rn']
            self.A_nnuc_outer=nnuc_tab_outer['data/A']
            self.nb_nnuc_outer=nnuc_tab_outer['data/nb']
            nb_nnuc_temp=[abs(self.r_nnuc_outer[i]-11.4)
                          for i in range(0,len(self.r_nnuc_outer))]
            self.rho_114=(self.nb_nnuc_outer[numpy.argmin(nb_nnuc_temp)]*
                          2.8e14/0.16)
            nb_nnuc_temp=[abs(self.r_nnuc_outer[i]-11.5)
                          for i in range(0,len(self.r_nnuc_outer))]
            self.rho_115=(self.nb_nnuc_outer[numpy.argmin(nb_nnuc_temp)]*
                          2.8e14/0.16)
            nb_nnuc_temp=[abs(self.r_nnuc_outer[i]-11.6)
                          for i in range(0,len(self.r_nnuc_outer))]
            self.rho_116=(self.nb_nnuc_outer[numpy.argmin(nb_nnuc_temp)]*
                          2.8e14/0.16)
            nb_nnuc_temp=[abs(self.r_nnuc_outer[i]-11.7)
                          for i in range(0,len(self.r_nnuc_outer))]
            self.rho_117=(self.nb_nnuc_outer[numpy.argmin(nb_nnuc_temp)]*
                          2.8e14/0.16)
            
            print('Loaded',len(self.w_nnuc_outer),
                  'nuclei for outer crust.')
            

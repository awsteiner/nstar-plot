"""
-------------------------------------------------------------------

Copyright (C) 2015-2022, Andrew W. Steiner

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

    # o2scl dll
    link=0
    
    def load(self):

        hf=o2sclpy.hdf_file(self.link)
        
        # Read inner crust data for neutrons
        if len(self.w_nn)==0:

            hf.open('inner_nn.o2')
            name=o2sclpy.std_string(self.link)
            name.init_bytes(b'inner_nn')
            nn_tab=o2sclpy.table(self.link)
            o2sclpy.hdf_input_n_table(self.link,hf,nn_tab,name)
            hf.close()
            
            self.w_nn=[nn_tab['w'][i] for i in range(0,100000)]
            self.r_nn=[nn_tab['r'][i] for i in range(0,100000)]
            #self.w_nn=self.w_nn[:100000]
            #self.r_nn=self.r_nn[:100000]
            print('Loaded',len(self.w_nn),'nucleons.')
            
        # Read inner crust data for nuclei
        if len(self.w_nnuc)==0:

            hf.open('inner_nnuc.o2')
            name.init_bytes(b'inner_nnuc')
            nnuc_tab=o2sclpy.table(self.link)
            o2sclpy.hdf_input_n_table(self.link,hf,nnuc_tab,name)
            hf.close()

            nt=nnuc_tab.get_nlines()
            print('nt',nt)

            self.w_nnuc=[nnuc_tab['w'] for i in range(0,nt)]
            self.r_nnuc=[nnuc_tab['r'] for i in range(0,nt)]
            self.Rn_nnuc=[nnuc_tab['Rn'] for i in range(0,nt)]
            self.A_nnuc=[nnuc_tab['A'] for i in range(0,nt)]
            self.nb_nnuc=[nnuc_tab['nb'] for i in range(0,nt)]
            
            #self.w_nnuc=self.w_nnuc[:nt]
            #self.r_nnuc=self.r_nnuc[:nt]
            #self.Rn_nnuc=self.Rn_nnuc[:nt]
            #self.A_nnuc=self.A_nnuc[:nt]
            #self.nb_nnuc=self.nb_nnuc[:nt]
            
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
            
            hf.open('outer_nnuc.o2')
            name.init_bytes(b'outer_nnuc')
            nnuc_tab_outer=o2sclpy.table(self.link)
            o2sclpy.hdf_input_n_table(self.link,hf,nnuc_tab_outer,name)
            hf.close()
            
            nt=nnuc_tab_outer.get_nlines()
            print('nt2',nt)
            
            self.w_nnuc_outer=[nnuc_tab_outer['w'][i] for i in range(0,nt)]
            self.r_nnuc_outer=[nnuc_tab_outer['r'][i] for i in range(0,nt)]
            self.Rn_nnuc_outer=[nnuc_tab_outer['Rn'][i] for i in range(0,nt)]
            self.A_nnuc_outer=[nnuc_tab_outer['A'][i] for i in range(0,nt)]
            self.nb_nnuc_outer=[nnuc_tab_outer['nb'][i] for i in range(0,nt)]
            
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
            

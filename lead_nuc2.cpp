#include <iostream>
#include <fstream>

#include <o2scl/hist.h>
#include <o2scl/table.h>
#include <o2scl/uniform_grid.h>
#include <o2scl/prob_dens_func.h>
#include <o2scl/hdf_file.h>
#include <o2scl/hdf_io.h>

using namespace std;
using namespace o2scl;
using namespace o2scl_hdf;

int main(void) {

  size_t n_grid=100;
  
  hist hp, hn;

  // The proton radius of lead (we use a fictitious 1.2 to convert
  // between RMS radius and "squared-off" radius)
  uniform_grid_end<double> rp(0.0,5.5*1.15,n_grid-1);
  // The neutron radius of lead
  uniform_grid_end<double> rn(0.0,5.7*1.15,n_grid-1);

  hp.set_bin_edges(rp);
  hn.set_bin_edges(rn);

  for(size_t i=0;i<rn.get_nbins();i++) {
    hn.set_wgt_i(i,rn[i]*rn[i]);
    hp.set_wgt_i(i,rp[i]*rp[i]);
  }

  table<> tn, tp;
  tn.line_of_names("x y z");
  tp.line_of_names("x y z");

  prob_dens_hist probn, probp;
  probn.init(hn);
  probp.init(hp);

  rng<> rg;
  rg.clock_seed();

  for(size_t i=0;i<126;i++) {
    //for(size_t i=0;i<10;i++) {
    double r=probn();
    double phi=rg.random()*o2scl_const::pi*2.0;
    double theta=acos(1.0-2.0*rg.random());
    double x=r*sin(theta)*cos(phi);
    double y=r*sin(theta)*sin(phi);
    double z=r*cos(theta);
    double line[3]={x,y,z};
    tn.line_of_data(3,line);
  }
  
  for(size_t i=0;i<82;i++) {
    //for(size_t i=0;i<10;i++) {
    double r=probp();
    double phi=rg.random()*o2scl_const::pi*2.0;
    double theta=acos(1.0-2.0*rg.random());
    double x=r*sin(theta)*cos(phi);
    double y=r*sin(theta)*sin(phi);
    double z=r*cos(theta);
    double line[3]={x,y,z};
    tp.line_of_data(3,line);
  }

  hdf_file hf;
  hf.open_or_create("lead_nuc2.o2");
  hdf_output(hf,tn,"neutrons");
  hdf_output(hf,tp,"protons");
  hf.close();

  bool fast_mode=false;
  cout << "Fast mode is " << fast_mode << endl;

  ofstream fout;
  fout.open("lead_nuc2.scr");
  fout << "#!/bin/bash" << endl;
  fout << "# This script automatically generated by lead_nuc2.cpp."
       << endl;
  fout << "o2graph -set xlo \"(0)\" -set xhi 1 \\" << endl;
  fout << "-set ylo \"(0)\" -set yhi 1 \\" << endl;
  fout << "-set zlo \"(0)\" -set zhi 1 \\" << endl;
  fout << "-set td_wdir gltf \\" << endl;
  // Red appears a bit brighter than blue, so we decrease that value
  // a bit. Protons are red, neutrons are blue. 
  fout << "-td-mat prot 0.8 0 0 \"alpha=0.3,alpha_mode=blend\" \\" << endl;
  fout << "-td-mat neut 0 0 1 \"alpha=0.3,alpha_mode=blend\" \\" << endl;

  size_t imax=tn.get_nlines();
  if (fast_mode) imax=40;
  size_t jmax=tp.get_nlines();
  if (fast_mode) jmax=10;

  double scale=12.0;
  
  // Neutrons
  for(size_t i=0;i<imax;i++) {
    fout << "-td-icos \"(" << tn.get("x",i)/scale+0.5 << ")\" \"("
         << tn.get("y",i)/scale+0.5 << ")\" \"("
         << tn.get("z",i)/scale+0.5
         << ")\" \"r=0.06,n_subdiv=2,mat=neut\" \\" << endl;
  }

  // Protons
  for(size_t j=0;j<jmax;j++) {
    fout << "-td-icos \"(" << tp.get("x",j)/scale+0.5 << ")\" \"("
         << tp.get("y",j)/scale+0.5 << ")\" \"("
         << tp.get("z",j)/scale+0.5
         << ")\" \"r=0.06,n_subdiv=2,mat=prot\" \\" << endl;
  }

  fout << "-gltf lead_nuc.gltf -bl-yaw-mp4 200 gltf/lead_nuc.mp4" << endl;

  fout.close();
  
  return 0;
}

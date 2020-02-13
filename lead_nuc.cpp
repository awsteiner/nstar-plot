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

  // The proton radius of lead
  uniform_grid_end<double> rp(0.0,5.5,n_grid-1);
  // The neutron radius of lead
  uniform_grid_end<double> rn(0.0,5.65,n_grid-1);

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

  rng_gsl rg;
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
  hf.open_or_create("lead_nuc.o2");
  hdf_output(hf,tn,"neutrons");
  hdf_output(hf,tp,"protons");
  hf.close();

  ofstream fout;
  fout.open("lead_nuc.scr");
  fout << "o2graph -set xlo \"(-7)\" -set xhi 7 \\" << endl;
  fout << "-set ylo \"(-7)\" -set yhi 7 \\" << endl;
  fout << "-set zlo \"(-7)\" -set zhi 7 \\" << endl;
  fout << "-set yt_position [8.0,8.0,2.0] \\" << endl;
  fout << "-set yt_width [0.9,0.9,0.9] \\" << endl;
  fout << "-set yt_resolution \"(1024,1024)\" \\" << endl;
  fout << "-create tensor_grid 3 101 101 101 \\" << endl;
  fout << "-set-grid 0 \"func:101:i*0.14-7\" \\" << endl;
  fout << "-set-grid 1 \"func:101:i*0.14-7\" \\" << endl;
  fout << "-set-grid 2 \"func:101:i*0.14-7\" \\" << endl;

  bool fast_mode=false;

  size_t imax=tn.get_nlines();
  if (fast_mode) imax=40;
  size_t jmax=10;
  if (fast_mode) jmax=10;
  
  // Neutrons
  for(size_t i=0;i<imax;i+=10) {
    fout << "-function \"";
    for(size_t j=0;j<jmax;j++) {
      if (i+j<tn.get_nlines()) {
	if (j>0) {
	  fout << "+";
	}
	// This function is 1.0 inside the nucleons and then 0.0
	// outside the nucleons. Since the nucleons are typically
	// not overlapping, this stays between 0 and 1.
	fout << "1/(1+exp(-(0.88-sqrt((x0-(" << tn.get("x",i+j)
	     << "))^2+(x1-(" << tn.get("y",i+j)
	     << "))^2+(x2-(" << tn.get("z",i+j)
	     << "))^2))/0.01))";
      }
    }
    fout << "\" \\" << endl;
    fout << "-stats \\" << endl;
    //fout << "-yt-box \"(-7)\" \"(-7)\" \"(-7)\" 7 7 7 \\" << endl;
    fout << "-yt-tf new 0 1 \\" << endl;
    fout << "-yt-tf gauss 0.5 6.0e-4 0.804 0.361 0.361 1.0 \\" << endl;
    fout << "-yt-add-vol \\" << endl;
  }

  // Protons
  if (fast_mode==false) {
    for(size_t i=0;i<tp.get_nlines();i+=10) {
      fout << "-function \"";
      for(size_t j=0;j<10;j++) {
	if (i+j<tp.get_nlines()) {
	  if (j>0) {
	    fout << "+";
	  }
	  fout << "1/(1+exp(-(0.88-sqrt((x0-(" << tp.get("x",i+j)
	       << "))^2+(x1-(" << tp.get("y",i+j)
	       << "))^2+(x2-(" << tp.get("z",i+j)
	       << "))^2))/0.01))";
	}
      }
      fout << "\" \\" << endl;
      fout << "-yt-tf new 0 1 \\" << endl;
      fout << "-yt-tf gauss 0.5 8.0e-4 0.392 0.584 0.929 1.0 \\" << endl;
      fout << "-yt-add-vol \\" << endl;
    }
  }
  /*
    fout << "-yt-axis \\" << endl;
    fout << "-yt-text 0.5 \"(-0.05)\" \"(-0.05)\" \"$ x $\" "
    << "reorient=True \\" << endl;
    fout << "-yt-text \"(-0.05)\" 0.5 \"(-0.05)\" \"$ y $\" "
    << "reorient=True \\" << endl;
    fout << "-yt-text \"(-0.05)\" \"(-0.05)\" 0.5 \"$ z $\" "
    << "reorient=True \\" << endl;
  */
  if (fast_mode) {
    fout << "-yt-render temp.png" << endl;
  } else {
    fout << "-yt-path yaw 101 0.01 \\" << endl;
    fout << "-yt-render \"/tmp/yt_*.png\" lead_nuc.mp4" << endl;
  }

  fout.close();
  
  return 0;
}

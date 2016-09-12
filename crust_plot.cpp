#include <iostream>
#include <string>

#include <o2scl/hdf_io.h>
#include <o2scl/hdf_eos_io.h>
#include <o2scl/nstar_cold.h>
#include <o2scl/vector.h>
#include <o2scl/eos_had_skyrme.h>
#include <o2scl/prob_dens_func.h>

using namespace std;
using namespace o2scl;
using namespace o2scl_hdf;

/** \brief A mini-molecular dynamics simulation
    which minimizes Coulomb repulsion (currently assumes
    equal charge)
*/
class mini_md {

public:

  /// y coordinates
  vector<double> w_nnuc;

  /// Radial coordinates
  vector<double> r_nnuc;

  /// Scale in y direction
  double w_scale;

  /// Scale in radius direction
  double r_scale;

  /// Random number generator
  rng_gsl rg;
  
  /** \brief Compute squared distance, wrapping
      around y coordinate
  */
  double sq_dist(size_t i, size_t j) {
    double d1=pow((w_nnuc[i]-w_nnuc[j])/w_scale,2.0)+
      pow((r_nnuc[i]-r_nnuc[j])/r_scale,2.0);
    double d2=pow((w_nnuc[i]-w_nnuc[j])/w_scale,2.0)+
      pow((r_nnuc[i]+1.0-r_nnuc[j])/r_scale,2.0);
    double d3=pow((w_nnuc[i]-w_nnuc[j])/w_scale,2.0)+
      pow((r_nnuc[i]-1.0-r_nnuc[j])/r_scale,2.0);
    if (d1<d2 && d1<d3) {
      return d1;
    } else if (d3<d2 && d3<d1) {
      return d3;
    }
    return d2;
  }

  /** \brief Total energy
   */
  double energy2() {
    double ret=0.0;
    for(size_t i=0;i<w_nnuc.size();i++) {
      for(size_t j=i+1;j<w_nnuc.size();j++) {
	ret+=1.0/sq_dist(i,j);
      }
    }
    return ret;
  }

  /** \brief Perform the simulation, modifying the y coordinates until
      the energy is minimized
   */
  void solve() {
    w_scale=1.0;
    r_scale=o2scl::vector_max_value<vector<double>,double>(r_nnuc)-
      o2scl::vector_min_value<vector<double>,double>(r_nnuc);
    size_t n=w_nnuc.size()*1;
    size_t pct=1;
    for(size_t i=0;i<n;i++) {
      if (i>=n*pct/100) {
	cout << pct << " percent done." << endl;
	pct++;
      }
      size_t j=rg.random_int(w_nnuc.size());
      while (j>=w_nnuc.size()) {
	j=rg.random_int(w_nnuc.size());
      }
      double e0=energy2();
      w_nnuc[j]+=0.01;
      double ep=energy2();
      w_nnuc[j]-=0.02;
      double em=energy2();
      w_nnuc[j]+=0.01;
      if (em<e0 && em<ep) {
	w_nnuc[j]-=0.01;
      } else if (ep<e0 && ep<em) {
	w_nnuc[j]+=0.01;
      }
      if (w_nnuc[j]>1.0) w_nnuc[j]-=1.0;
      if (w_nnuc[j]<0.0) w_nnuc[j]+=1.0;
    }
    return;
  }
};

int main(void) {

  bool inner=true;
  
  // Read crust results
  table_units<> crust;
  string name;
  hdf_file hf;
  hf.open("crust_SLy4.o2");
  hdf_input(hf,crust,name);
  hf.close();
  crust.set_interp_type(itp_linear);

  // Skyrme EOS for core
  eos_had_skyrme sk;
  skyrme_load(sk,"SLy4");

  // Neutron star structure
  nstar_cold nc;
  nc.set_eos(sk);
  nc.def_eos_tov.s12_low_dens_eos("SLy4");
  nc.calc_eos();
  nc.fixed(1.4);

  // Interpolate crust EOS into TOV results
  std::shared_ptr<table_units<> > prof=nc.get_tov_results();
  prof->set_interp_type(itp_linear);
  prof->add_col_from_table(crust,"nb","nnuc","nb");
  prof->set_unit("nnuc","1/fm^3");
  prof->add_col_from_table(crust,"nb","N","nb");
  prof->add_col_from_table(crust,"nb","Z","nb");
  prof->add_col_from_table(crust,"nb","nn","nb");
  prof->set_unit("nn","1/fm^3");
  prof->add_col_from_table(crust,"nb","Rn","nb");
  prof->set_unit("Rn","fm");
  prof->add_col_from_table(crust,"nb","ne","nb");
  prof->set_unit("ne","1/fm^3");

  // Delete noisy values of "nn"
  for(size_t i=0;i<prof->get_nlines();i++) {
    if (prof->get("nn",i)>0.0 && prof->get("nn",i<1.0e-12)) {
      prof->set("nn",i,0.0);
    }
  }

  // Remove core rows outside of range
  double nb_high=0.08;
  double nb_low=0.16*4.0e11/2.8e14;
  if (inner==false) {
    nb_high=nb_low;
    nb_low=1.0e-8;
  }
  prof->delete_rows(((std::string)"nb>")+o2scl::dtos(nb_high)+
		    " || nb<"+o2scl::dtos(nb_low));

  // Get radius range
  double r_low=prof->min("r");
  double r_high=prof->max("r");

  // Create histograms with refined baryon density grid
  hist h_nnuc, h_N, h_Z, h_nn, h_Rn, h_nb, h_ne, h_ntotal, h_A;
  uniform_grid_end<double> grid(r_low,r_high,500);
  h_nnuc.set_bin_edges(grid);
  h_N.set_bin_edges(grid);
  h_Z.set_bin_edges(grid);
  h_nn.set_bin_edges(grid);
  h_Rn.set_bin_edges(grid);
  h_nb.set_bin_edges(grid);
  h_ne.set_bin_edges(grid);
  h_ntotal.set_bin_edges(grid);
  h_A.set_bin_edges(grid);
  for(size_t i=0;i<h_nnuc.size();i++) {
    double r=h_nnuc.get_rep_i(i);
    h_nnuc[i]=prof->interp("r",r,"nnuc");
    h_nn[i]=prof->interp("r",r,"nn");
    h_N[i]=prof->interp("r",r,"N");
    h_Z[i]=prof->interp("r",r,"Z");
    h_Rn[i]=prof->interp("r",r,"Rn");
    h_nb[i]=prof->interp("r",r,"nb");
    h_ne[i]=prof->interp("r",r,"ne");
    h_ntotal[i]=h_nn[i]+h_nnuc[i];
    h_A[i]=h_Z[i]+h_N[i];
  }

  // Set up the histogram in the total particle density
  rng_gsl rg;
  rg.clock_seed();
  prob_dens_hist pdh;
  pdh.init(h_ntotal);

  // MD simulation
  mini_md md;

  // Coordinate storage
  vector<double> w_nn, r_nn;

  // Sample the histogram to get the coordinates
  size_t big_n=600000;
  if (inner==false) big_n=1200;
  for(size_t i=0;i<big_n;i++) {
    double r=pdh();
    double nnuc=prof->interp("r",r,"nnuc");
    double nn=prof->interp("r",r,"nn");
    double rnd=rg.random();
    double w=rg.random();
    if (i>0 && rnd<nn/(nn+nnuc)) {
      w_nn.push_back(rg.random());
      r_nn.push_back(r);
    } else {
      if (i==0 && inner==false) r=r_high;
      md.w_nnuc.push_back(rg.random());
      md.r_nnuc.push_back(r);
    }
  }
  cout << w_nn.size() << " neutrons and " << md.w_nnuc.size()
       << " nuclei." << endl;

  // Perform the MD simulation
  md.solve();

  // Write the neutrons to a table
  table<> t_nn;
  if (inner) {
    t_nn.set_nlines(w_nn.size());
    t_nn.line_of_names("r w");
    t_nn.swap_column_data("r",r_nn);
    t_nn.swap_column_data("w",w_nn);
  }

  // Write the nuclei to a table
  table<> t_nnuc;
  t_nnuc.set_nlines(md.w_nnuc.size());
  t_nnuc.line_of_names("r w A Rn nb");
  t_nnuc.swap_column_data("r",md.r_nnuc);
  t_nnuc.swap_column_data("w",md.w_nnuc);
  for(size_t i=0;i<t_nnuc.get_nlines();i++) {
    t_nnuc.set("A",i,prof->interp("r",t_nnuc.get("r",i),"N")+
		prof->interp("r",t_nnuc.get("r",i),"Z"));
    t_nnuc.set("Rn",i,prof->interp("r",t_nnuc.get("r",i),"Rn"));
    t_nnuc.set("nb",i,prof->interp("r",t_nnuc.get("r",i),"nb"));
  }

  // Output the table(s) to file(s)
  if (inner) {
    hf.open_or_create("inner_nn.o2");
    hdf_output(hf,t_nn,"inner_nn");
    hf.close();
    hf.open_or_create("inner_nnuc.o2");
    hdf_output(hf,t_nnuc,"inner_nnuc");
    hf.close();
  } else {
    hf.open_or_create("outer_nnuc.o2");
    hdf_output(hf,t_nnuc,"outer_nnuc");
    hf.close();
  }
    
  return 0;
}

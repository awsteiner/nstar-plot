FLAGS = -std=c++0x -ggdb -O3 -DO2SCL_READLINE \
	-I$(O2SCL_INC) -I$(GSL_INC) -I$(HDF5_INC) -I$(BOOST_INC) \
	-I$(EIGEN_INC) 

LIB = -L$(O2SCL_LIB) -L$(GSL_LIB) -L$(HDF5_LIB) -lo2scl_eos \
	-lo2scl_part -lo2scl_hdf -lo2scl -lhdf5 \
	-lgsl -lgslcblas -lreadline -lncurses

#----------------------------------------------------------------------

help:
	@echo "doc"
	@echo "sync-doc"
	@echo "crust_plot"
	@echo "eos_mvsr"
	@echo "qcd_phase.png"

doc:
# Get most recent commit hash
	git rev-parse HEAD | awk \
		'{print "`" $$1 " <http://github.com/awsteiner/nstar-plot/tree/" $$1 ">`_"}' \
		 > sphinx/commit.rst
# Parse bibliography
	cd sphinx/static; cat bib_header.txt > ../bib.rst
	cd sphinx/static; btmanip -parse refs.bib -rst ../bib_temp.rst
	cd sphinx; cat bib_temp.rst >> bib.rst; rm -f bib_temp.rst
# Run sphinx
	cd sphinx; make html

sync-doc:
	rsync -Cavzu sphinx/build/html/* $(STATIC_DOC_DIR)/nstar-plot

crust_plot.o: crust_plot.cpp
	$(CXX) $(FLAGS) -o crust_plot.o -c crust_plot.cpp

crust_plot: crust_plot.o
	$(CXX) $(FLAGS) -o crust_plot crust_plot.o $(LIB)

eos_mvsr.o: eos_mvsr.cpp
	$(CXX) $(FLAGS) -o eos_mvsr.o -c eos_mvsr.cpp

eos_mvsr: eos_mvsr.o
	$(CXX) $(FLAGS) -o eos_mvsr eos_mvsr.o $(LIB)

qcd_phase.png: empty
	o2graph -set font 24 \
                -set fig_dict "fig_size_x=8,fig_size_y=6,left_margin=0.12" \
                -set xlo 0 -set xhi 10 -set ylo 0 -set yhi 200 \
                -rect 0 0 2 100 0 "color=(0.9,0.9,0.9)" \
                -text 0.5 52 "Hadrons" "rotation=90,va=center,ha=center" \
                -rect 1.0 0 8 120 0 "color=(0.9,0.8,0.8)" \
                -text 6.5 100 "Neutron star" "ha=center,va=center,color=red" \
                -text 6.5 90 "mergers" "ha=center,va=center,color=red" \
                -rect 0.0 0 8 5 0 "color=(0.8,0.9,0.8)" \
                -text 4.0 12 "Neutron stars" "ha=center,va=center,color=green" \
                -xtitle "$$ n_B/n_0 $$" \
                -ytitle "$$ T~(\mathrm{MeV}) $$" \
                -create table T func:17:i \
                -function "0.7-T*T*0.0005" nc \
                -plot nc T "color=black,lw=2" \
                -point "0.7-16*16*0.0005" 16 \
                "marker=o,mfc=black,mec=black,ms=4" \
                -text 0.2 22 "Liquid-gas" \
                "ha=left,va=center,fontsize=20" \
                -text 0.8 12 "PT" \
                "ha=left,va=center,fontsize=20" \
                -create table T func:141:i \
                -function "2-T*T*T/2000000" pt1 \
                -function "6-T*T*T*3.9/2000000" pt2 \
                -plot pt1 T "color=indigo,ls=--,lw=2" \
                -plot pt2 T "color=indigo,ls=--,lw=2" \
                -text 6 170 "Strongly-interacting quarks and gluons" \
                "va=center,ha=center" \
                -rect 0 75 2 200 0 "color=(0.8,0.8,0.9)" \
                -text 0.3 140 "Rel. Heavy-Ion Coll." \
                "ha=center,va=center,rotation=90,color=blue" \
                -point 0.6 140 "marker=o,mfc=blue,mec=blue,ms=4" \
                -text 0.7 145 "Critical point" \
                "fontsize=20,ha=left,va=center" \
                -arrow 4.1 50 1.9 50 \
                "arrowstyle=fancy,fc=indigo,ec=indigo,lw=2,head_width=1.0" \
                -arrow 3.9 50 9.8 50 \
                "arrowstyle=fancy,fc=indigo,ec=indigo,lw=2,head_width=1.0" \
                -text 6.0 60 "Variation of deconfinement transition" \
                "color=indigo" \
                -save "qcd_phase.png" -show

empty:

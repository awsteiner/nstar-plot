FLAGS = -std=c++0x -ggdb -O3 -DO2SCL_READLINE \
	-I$(O2SCL_INC) -I$(GSL_INC) -I$(HDF5_INC) -I$(BOOST_INC) \
	-I$(EIGEN_INC) 

LIB = -L$(O2SCL_LIB) -L$(GSL_LIB) -L$(HDF5_LIB) -lo2scl_eos \
	-lo2scl_part -lo2scl_hdf -lo2scl -lhdf5 \
	-lgsl -lgslcblas -lreadline -lncurses

#----------------------------------------------------------------------

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
	sudo cp -r sphinx/build/html/* $(STATIC_DOC_DIR)/nstar-plot

crust_plot.o: crust_plot.cpp
	$(CXX) $(FLAGS) -o crust_plot.o -c crust_plot.cpp

crust_plot: crust_plot.o
	$(CXX) $(FLAGS) -o crust_plot crust_plot.o $(LIB)


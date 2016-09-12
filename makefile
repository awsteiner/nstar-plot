FLAGS = -std=c++0x -ggdb -O3 -DO2SCL_READLINE \
	-I$(O2SCL_INC) -I$(GSL_INC) -I$(HDF5_INC) -I$(BOOST_INC) \
	-I$(EIGEN_INC) 

LIB = -L$(O2SCL_LIB) -L$(GSL_LIB) -L$(HDF5_LIB) -lo2scl_eos \
	-lo2scl_part -lo2scl_hdf -lo2scl -lhdf5 \
	-lgsl -lgslcblas -lreadline -lncurses

#----------------------------------------------------------------------

crust_plot.o: crust_plot.cpp
	$(CXX) $(FLAGS) -o crust_plot.o -c crust_plot.cpp

crust_plot: crust_plot.o
	$(CXX) $(FLAGS) -o crust_plot crust_plot.o $(LIB)


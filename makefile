
#----------------------------------------------------------------------

ifdef UTKNA_MAKEFILE

include $(UTKNA_MAKEFILE)

# UTK configuration
LIBS = $(UTKNA_O2SCL_LIBS) 
LCXX = $(UTKNA_CXX) 
LCFLAGS = $(UTKNA_O2SCL_INCS) $(UTKNA_CFLAGS)

# UTK configuration
MPI_LIBS = $(UTKNA_O2SCL_LIBS) 
MPI_LCXX = $(UTKNA_MPI_CXX) 
MPI_LCFLAGS = $(UTKNA_O2SCL_INCS) $(UTKNA_CFLAGS) $(UTKNA_MPI_CFLAGS) \
	$(UTKNA_OPENMP_FLAGS)

endif

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

lead_nuc.o: lead_nuc.cpp
	$(CXX) $(FLAGS) -o lead_nuc.o -c lead_nuc.cpp

lead_nuc: lead_nuc.o
	$(CXX) $(FLAGS) -o lead_nuc lead_nuc.o $(LIB)

lead_nuc2.o: lead_nuc2.cpp
	$(CXX) $(LCFLAGS) -o lead_nuc2.o -c lead_nuc2.cpp

lead_nuc2: lead_nuc2.o
	$(CXX) $(LCFLAGS) -o lead_nuc2 lead_nuc2.o $(LIBS)

eos_mvsr.o: eos_mvsr.cpp
	$(LCXX) $(LCFLAGS) -o eos_mvsr.o -c eos_mvsr.cpp

eos_mvsr: eos_mvsr.o
	$(LCXX) $(LCFLAGS) -o eos_mvsr eos_mvsr.o $(LIBS)

empty:

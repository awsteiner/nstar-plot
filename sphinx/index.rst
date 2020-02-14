Neutron star-related plots
==========================

This documentation was generated from git commit

.. include:: commit.rst

Licensing
---------

The C++ and python code provided here is license under the
:download:`GNU General Public License (v3)<static/gpl_license.txt>`
and the plots themselves, as provided in the repository, are
licensed as :download:`CC-BY-NC (4.0)<static/cc_by_nc_4.md>`.
	     
General notes
-------------

Some of the plots use data which is generated using C++ code which
requires `O2scl
<https://isospin.roam.utk.edu/static/code/o2scl>`_.
The python plots often require `O2sclpy
<https://isospin.roam.utk.edu/static/code/o2sclpy>`_ (only
those that use the ``o2graph_plotter`` class require `O2scl
<https://isospin.roam.utk.edu/static/code/o2scl>`_).

Plots
-----

.. list-table::
   :header-rows: 0
   :widths: 30 30

   * - .. image:: ../nstar_plot.png
     
       :ref:`Neutron star plot`

     - .. image:: ../eos_mvsr.png

       :ref:`EOS and M-R curve plot`

   * - .. image:: ../crust_plot.png
     
       :ref:`Neutron star crust`

     - .. image:: ../sfluid3.png

       :ref:`History of Superconductivity`

   * - .. image:: ../periodic_table.png
     
       :ref:`Origin of the elements`

     - .. image:: ../ppdot.png

       :ref:`P pdot diagram`

   * - .. raw:: html
	 
          <video width="256" height="256" controls><source src="https://neutronstars.utk.edu/code/nstar-plot/_static/lead_nuc.mp4" type="video/mp4"></video>
     
       :ref:`Lead nucleus cartoon`

     - 

Contents
--------
     
.. toctree::
   :maxdepth: 2

   nstar_plot
   eos_mvsr
   ns_crust
   sc_hist
   periodic_table
   ppdot
   lead_nuc
   bib

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

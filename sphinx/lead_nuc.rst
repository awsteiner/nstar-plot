Lead nucleus cartoon
--------------------

This is a visualization of 82 protons (blue) and 126 neutrons (red)
selected according to their probability distributions inside a lead
nucleus. The radius of the proton is taken to be 0.88 fm and the RMS
proton radius of the lead nucleus is taken to be 5.5 fm. The neutron
skin thickness is chosen to be 0.15 fm. The position of the nucleons
is chosen to be time-independent, the movie just rotates around these
fixed positions.

C++ code in `lead_nuc.cpp
<https://github.com/awsteiner/nstar-plot/blob/master/lead_nuc.cpp>`_
is used to generate the nucleon positions and the `o2graph
<https://neutronstars.utk.edu/code/o2sclpy/o2graph.html>`_ script in
`lead_nuc.scr
<https://github.com/awsteiner/nstar-plot/blob/master/lead_nuc.scr>`_
which uses `o2sclpy <https://neutronstars.utk.edu/code/o2sclpy/>`_
which, in turn, uses `yt <https://yt-project.org>`_ to do the
visualization.

.. raw:: html
	 
   <video width="512" height="512" controls><source src="https://neutronstars.utk.edu/code/nstar-plot/_static/lead_nuc.mp4" type="video/mp4"></video>

	   

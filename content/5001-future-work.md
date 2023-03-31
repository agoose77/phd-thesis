ax.xaxis.labelpad = 20---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Future Work
The data analysed in this thesis are amenable to further investigation. A particular challenge in this work has been the measurement of the ion stopping powers in the TPC gas, which are fundamental to the reconstruction of the reaction kinematics. Future efforts to measure these stopping powers in order to accurately model energy loss in the gas would likely bring the different beam-energy reconstruction approaches outlined in {numref}`expt:beam-energy-estimation` into agreement, subject to the energy and angular straggling incurred by the beam as it moves through the TexAT TPC entrance window. 

The problem of ringing in the MicroMeGaS signals may also be further addressed in future works. Whilst the methods outlined in this thesis address many of these waveforms, a more robust approach could be introduced to better classify non-significant waveform regions. Machine learning methods are of an increasing relevance in the space of signal classification, and future works may be well positioned to take advantage of the rapid pace of contemporary developments in this space. 

The ability to separate the elastic and inelastic contributions to the zero-degree reconstruction outlined in {numref}`expt:zero-degree-scattering` depends upon the ability to identify the interaction vertex. Without a well defined Bragg peak, one could instead identify a step change in the {math}`\dv{E}{x}` of the pads region which corresponds to the interaction vertex. Otherwise, it may also be possible to identify the position at which the energy lost in the MicroMeGaS no longer includes contributions from the heavy-scatter track. In such a scenario it would be kinematically possible to identify the interaction vertex, and thus discriminate elastic and inelastic scatters. 

With these data, future work may compute differential cross sections to aid in the assignment of spins and parities to the observed levels, in order to support theoretical predictions of the structure of excited states.

It would be beneficial to build upon the success of the TexAT TPC detector to improve the position resolution, and reduce the artefacts originating from inhomogeneity in the MicroMeGaS anode. Replacing the thick silicon quadrant detectors with particle telescopes (e.g. thin silicon, thick scintillator) would remove a degree of ambiguity in the particle identification procedure that derives from the poor charge sensitivity of the MicroMeGaS anode. Furthermore, increasing the coverage of the particle detectors to {math}`2\pi` would improve the efficiency of the detector, enhancing the statistics of the dataset and its derived measures. By replacing the strip-chain layout of the MicroMeGaS with an homogenous pixelated anode would eliminate the challenges of track reconstruction that pertain to the interaction between the central and side regions of the anode. This could be further enhanced with the introduction of a resistive strip anode, which would provide sub-pad resolution of charge clusters measured in the TPC {cite:ps}`bortfeld_jonathan_development_nodate`.
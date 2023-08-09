---
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

(experiment)=
# Resonant Elastic Scattering of $\alpha$-particles with ${}^{10}\text{C}$

+++

This chapter outlines an analysis workflow that has been developed to reconstruct experimental data taken from an experiment conducted at Texas A&M University in 2018 using the TeXAT detector at the Cyclotron Institute. For much of this analysis work, there were no public references for best-practice or existing analysis techniques beyond high-level discussions in a preliminary paper published by the physics group at Texas A&M University. As such, all methods described here are original work, although the group at Texas A&M were helpful in resolving particular lines of questioning concerning detector function and other analysis techniques being developed. Reconstruction of the GET response function, and its use in signal fitting; track fitting using the PeARL method; and ringing elimination may be considered to be particularly novel contributions. Application of kinematic fitting to the reconstructed kinematics was also a novel contribution to this kind of analysis, although a summary of the results from this work is not included following a refocussing on the challenges associated with signal ringing in the detector. The development of this analysis using modern high-energy physics packages, and the Dask parallel computing library was also novel, although discussion of this work was omitted here for brevity.

The analysis process described in this chapter was performed in a series of discrete stages (see {numref}`analysis-flowchart`).

:::{mermaid}
:caption: Process diagram of the TexAT analysis.
:align: center
:name: analysis-flowchart

flowchart TD

baseline_removal --> response[Response Estimation*]
baseline_removal --> gain_matching[Gain Matching*]
signal --> calibrate[Silicon Calibration*]
gain_matching --> signal
calibrate --> kinematic_fitting
response --> signal
get[/GET MFM/] --> mfm2root[ROOT Conversion]
mfm2root --> partitioning[Partitioning] 
partitioning--> noise_removal[Noise Removal] 
noise_removal--> baseline_removal[Baseline Removal] 
baseline_removal--> signal[Signal Fitting] 
signal--> origin[Origin Fitting] 
origin--> event[Cluster Reconstruction] 
event--> fit[Track Fitting] 
signal -->pid[Particle Identification]
event -->pid
fit--> kinematic_fitting[Kinematic Fitting] 
kinematic_fitting--> kinematics[/Kinematics/]
pid --> kinematics
gas_parameters[/Gas Parameters/] --> gas_simulation[Gas Simulation] 
gas_simulation--> event

click get "#" "The raw event binary messages from GET"
click mfm2root "#" "Conversion from MFM format to ROOT TTrees"
click partitioning "2601-partitioning.html" "Partitioning of the GET events into memory-balanced chunks"
click baseline_removal "2602-noise-and-baseline-removal.html" "Removal of electronic noise from the GET waveforms"
click noise_removal "2602-noise-and-baseline-removal.html" "Removal of constant baseline signal components"
click response "2603-response-estimation.html" "Estimation of the GET response function. Aggregated over the entire dataset prior to reconstruction"
click gain_matching "2604-gain-matching.html" "Relative gain matching between MicroMeGaS regions. Aggregated over the entire dataset prior to reconstruction"
click signal "2605-signal-fitting.html" "Energy-time fitting of the GET waveforms"
click calibrate "2607-silicon-calibration.html" "Energy calibration of the silicon detectors. Aggregated over the entire dataset prior to reconstruction"
click gas_simulation "2608-gas-simulation.html" "Simulation of the gas properties using Garfield++ / Magboltz"
click origin "2609-beam-origin.html" "Determining beam origin from MicroMeGaS point cloud"
click event "2610-cluster-reconstruction.html" "Charge cluster and silicon hit reconstruction from fit waveforms"
click fit "2611-track-fitting.html" "Fitting particle tracks to charge clusters"
click pid "2612-particle-identification.html" "Identifying alpha particles from the signature left in the silicon and MicroMeGaS detectors"
click kinematic_fitting "2613-kinematic-fitting.html" "Fitting kinematics to particle tracks using physical constraints"
click gas_parameters "#" "The known parameters for the active-target gas (96% He, 4% CO2)"
click kinematics "2614-kinematics.html" "Reconstructing event information from kinematical constraints"
:::


:::{container} mermaidTooltip
% Tooltip 
:::

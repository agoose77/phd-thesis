---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Introduction

Experimental nuclear physics is fundamentally a discipline that is concerned with the strong interaction between quarks. At the low-energy scale, it is not the strong interaction itself, but the _residual_ strong interaction that acts between nucleons, that is of interest. Investigations into the nature of this interaction, and the physics that emerges from its presence in the many-body system of the nucleus, lie at the heart of the field. An introduction to the contemporary understanding of the nucleus, and the role of the strong interaction in its behavior, is given in {numref}`content:nuclear-models`.

Experiments that probe the nature of the residual strong interaction must ultimately proceed through scattering experiments, whereby systems of nucleons are brought together in order to glimpse the properties of the ensuing interaction through measurement of the products. These scattering reactions prove to be experimentally challenging; for example, one or more of the interacting systems may have microscopic lifetimes, or a range of interaction energies must be explored. A cornerstone technique in the exploration of these novel systems has been the use of time-projection chambers (TPC), such as that used in ALICE {cite:ps}`alme_alice_2010`, in which the trajectories of particles moving through the chamber can be reconstructed. A discussion of TPCs, and the physics which governs their use, is conducted in {numref}`expt:thick-target-experiments`. 

Associated with the use of TPCs is the task of identifying the tracks left by particles moving within the detector chamber, and subsequently determining their kinematic properties. These two processes of track _identification_ and track _fitting_ are introduced in {numref}`expt:track-finding-and-fitting`. Existing techniques include sequential RANdom SAmple Concensus (RANSAC) and the sequential  Hough transform, which suffer from greedy fitting. A reframing of the track-fitting problem as an uncapacitated facility location problem (UFLP) is given in {numref}`facility-location-problem`. There, the Propose Expand and Re-estimate Labels (PEaRL) algorithm is introduced as an approach to solving the UFLP for geometric track fitting, with a discussion of its performance when applied to several simulated track observations. 

A scattering experiment was performed by the Texas A&M group in 2018, before the work in this thesis began. The TexAT TPC was used in conjunction with a radioactive beamline to perform (elastic) scattering of {math}`{}^{10}\mathrm{C}` upon {math}`{}^{4}\mathrm{He}`, which would facilitate an investigation into the presumed molecular structures in {math}`{}^{14}\mathrm{O}`. An overview of the existing literature upon {math}`{}^{14}\mathrm{O}` and its mirror nucleus {math}`{}^{14}\mathrm{C}`
is given in {numref}`content:carbon-oxygen-mirror-nuclei`. The workflow for an analysis of these (and similar) data is described in {numref}`experiment`, with a focus upon the analysis challenges imposed by the early data from the TexAT TPC. These challenges include the handling of ringing artefacts, which must be distinguished from true MicroMeGaS measurements, and fitting of the GET-shaped waveforms in the absence of a measured response function. 

Further developments to this analysis were impeded by the onset of the COVID-19 pandemic, which detracted from the collaborative nature of research in every way imaginable. During this time, a need for teaching laboratory skills in the face of legal and ethical barriers to in-person demonstration was identified. This led to the development of the Online nuclear LABoratory (O-Lab), whose development, features, and usage statistics are outlined in {numref}`content:olab`.

Underpinning the work in this thesis is a considerable body of software that was developed in order to perform the analysis work described in {numref}`experiment`, and develop the fitting method described in {numref}`expt:track-finding-and-fitting`. These software will be made publically available under an open-source license.
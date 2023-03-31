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

# Conclusions
A workflow for feature analysis of the raw GET waveforms was established, using modern columnar analysis tools and techniques to ensure high throughput and convenient re-analysis. Alongside this analysis, a suite of investigative tools was developed to aid the investigation of single events at different stages of the analysis workflow, such as 3D event viewers, 2D hit-map reconstruction, and 1D waveform analysis. An understanding of the limitations associated with the TexAT detector was developed, with particular focus upon the problem of "ringing" in the high-gain MicroMeGaS regions, and the challenge associated with strip-chain agreement for near-planar events. Though amenable to recovery using symmetries of the detector, poor performance of the silicon detector array was observed to diminish the statistics of subsequent analysis work.

Simulations of the properties of the {math}`{}^{4}\mathrm{He} + \mathrm{CO}_2` gas mixture were made to support simulation and analysis of novel reconstruction approaches in the {math}`{}^{4}\mathrm{He} + {}^{10}\mathrm{C}` scattering reaction. The drift velocity, drift resolution, and stopping powers of relevant ions were computed for the gas mixture; both SRIM and MSTAR were investigated for the heavy ion ({math}`{}^{10}\mathrm{C}`) energy loss calculations. Investigations into the use of graph-cut track finding and fitting methods were performed, and the findings used to reconstruct particle tracks recorded by the TexAT TPC detector at the Texas A & M Cyclotron Institute, College Station, United States. The theory behind constrained optimisation was explored. An exploration of the literature was conducted to determine the structures that might be populated in the elastic alpha-scattering entrance channel of the {math}`{}^{14}\mathrm{O}` nucleus. An initial, highly preliminary exploration of the experimental results was made towards investigating the states populated in {math}`{}^{14}\mathrm{O}` via the elastic scattering channel. An excitation function was derived for the different reconstruction methods, and an tentative discussion was opened into the agreement between these early results, the predicted molecular states, and existing experimental levels recorded in nuclear databases.

In the second half of this thesis, a virtual online laboratory for nuclear physics students was developed, with a strong focus on reducing the time-to-deployment, familiarity to existing laboratory users, and integration with existing Learning Tools Interoperability (LTI)-aware Virtual Learning Environments (VLE)s. A series of virtual laboratory experiments were designed around existing in-person experiences, with requisite support material to facilitate self-sufficient learning. A cloud-based JupyterHub deployment was developed using Kubernetes to provide distance-learning and self-isolating students with access to per-user compute environments outside of the University campus network. Provision was made for future extensions of the laboratory including cloud-based analysis to facilitate future extensions into hybrid-learning. The high-level usage data for an initial cohort of students were recorded and analysed to infer usage patterns, and task engagement.

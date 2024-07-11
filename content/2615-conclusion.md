# Conclusion

In this chapter, the workflow for an analysis of the experimental data recorded by the TexAT TPC was introduced and
discussed. In the process of developing this workflow, a range of problems associated with the early variant of the
TexAT detector were identified, such as the poor performance of the silicon detector array, the considerable problem
of signal ringing and its indistinguisability from valid signals, and the challenging nature of the inhomogenous pixellated
MicroMeGaS. The raw GET data files that this analysis was built to ingest are typically of considerable size; even with a
partial read-out mode, a single event nominally contains on the order of 300 waveforms of 512 samples. The workflow
described in this chapter was designed to make such a problem tractable; breaking down the data into compute-friendly
chunks, and leveraging modern distributed computation frameworks to facilitate its analysis. Each stage of the workflow

given in {numref}`analysis-flowchart` was original work, with the exception of the ROOT Conversion tool, which was improved but other-
wise pre-existing; and the gas-simulation tool described in Section 8.8, which was strongly inspired by the Texas A&M

approach.
The track-fitting technique established in this thesis was used to perform preliminary steps towards an investigation of
the structure of {math}`{}^{14}\mathrm{O}`. With the challenges posed by COVID-19 and the quirks with the aforementioned TexAT data,
this analysis was not carried beyond an initial exploration of the problem space. During this process, limitations of the
data were identified, such as the missing Bragg peak of the heavy scattered beam that would be required for zero-degree
reconstruction. Before the COVID pandemic, a future iteration of the TexAT detector was in its development phase, and
this author made some contributions to the discussions and planning around future analysis software. This new detector,
TeBAT, will solve many of the problems encountered in this analysis, such as the strip-chain matching for planar events,
and the poor resolution of the central columnar region. Future efforts to finalise the analysis of the data discussed in
this chapter should look to resolving the question of the zero-degree elastic-inelastic discrimination, before proceeding to
account for the silicon detector efficiencies in the cross-section reconstruction of the reconstructed data. The preliminary
excitation function shown in Section {numref}`content:excitation-functions` indicates that the prediction of a linear-chain state in the 14 MeV—19 MeV
region may be feasibly identified in these data, should it exist.

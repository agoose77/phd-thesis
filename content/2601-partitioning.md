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

# Partitioning
The GET acquisition system serialises data using the MultiFrame Metaformat (MFM), which is described as: {cite:ps}`anvar_multiframe_nodate`
> a binary format for data acquisition and serialization that are self-contained, layered, adapted to network transfers[,] and evolving. 

This file format is more suitable for disk storage than in-memory representation of data, as it is a hierarchical format in which each _frame_ must be read, regardless of whether it is needed. The use of separate header and data sections means that the cost of skipping a frame is limited to parsing the header, but MFM is still a struct-based format. In many cases, columnar processing is both more performant and more expressive than an equivalent event-loop based approach {cite:ps}`smith_case_2019`. 

At the earliest stages of the reconstruction pipeline, performance is primarily bounded by available memory, and therefore it is sensible to partition the data by the event multiplicity: the number of waveforms stored for each event. This process constitutes the first two stages of this analysis, seen in {numref}`analysis-flowchart`. In the ROOT dataset, the `mmMul` branch contains the per-event multiplicity. To regularise the dataset according to this multiplicity, it was partitioned into approximate chunks of a given aggregate multiplicity. Given that the memory of an MFM event is primarily determined by the number of waveforms that it contains, this effectively balances the memory footprint of each partition.

In subsequent stages, the memory bound gives way to compute costs, and so the partition size is refined to balance naive parallelisation against parallelisation overhead. Where data is written to disk, the Hierarchical Data Format version 5 (HDF5) format {cite:ps}`the_hdf5_group_hierarchical_1997` is used as a consequence of its good language support, high compression ratios (with GZip {cite:ps}`deutsch_gzip_1996`), and columnar representation. The Parquet format {cite:ps}`noauthor_apache_nodate` is another strong format for columnar representation but, due to some library constraints, HDF5 was preferred.

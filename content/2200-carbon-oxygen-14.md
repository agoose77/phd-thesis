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

# {math}`{}^{14}C` and {math}`{}^{14}O` Mirror Nuclei

+++

% TODO motivations

+++

## Mirror Nuclei

In {ref}`liquid-drop-model`, the semi-empirical mass formula was introduced. Notably, it is only the Coulomb term of {eq}`semi-empirical-mass-formula` that explicitly depends upon a nucleon flavour (the proton). This hints at a symmetry of the strong interaction - that the Hamiltonian is degenerate with respect to nucleon charge. It is not an _exact_ symmetry; the mass of the neutron is slightly greater than that of the proton, and thus the eigenvalues of the strong Hamiltonian are distinct. This difference can be treated as a _perturbation_ of an exact symmetry, called Isospin {math}`I` for its close resemblance of the spin-{math}`\frac{1}{2}` representation.{cite:ps}`wigner_consequences_1937` In this model, protons and neutrons form eigenstates of the spin-doublet system with {math}`3` projection {math}`I_3 \pm \frac{1}{2}`.

+++

There are two interpretations of isospin symmetry:

Charge-symmetry
: Charge-_symmetry_ holds that the _pp_ interaction is indistinguishable from that of the _nn_ interaction. In terms of the isospin 
    :::{math}
    :label: charge-symmetry
    
    \comm{\hat{H}}{\exp(\frac{i\pi \hat{I}_i}{\hbar})} = 0\,,
    :::
    where {math}`\hat{I}_i` is the operator that measures the {math}`i\neq 3` projection of the isospin {math}`I`, and {math}`\hat{H}` is the strong Hamiltonian. The {math}`\exp(\frac{i\pi \hat{I}_i}{\hbar})` rotation operator negates the {math}`\hat{I}_3` expectation value.
    
    % Most of the mass of the proton/neutron comes from strong interaction between quarks. Quarks in p and n have equal mass, so strong interaction Hamiltonian determines

+++

Charge-independence
: Charge-_independence_ holds that the _pp_, _nn_, and _pn_ interactions are indistinguishable, i.e.
    :::{math}
    :label: charge-independence
    
    \comm{\hat{H}}{\exp(\frac{i \theta \hat{I}_i}{\hbar})} = 0\,,
    :::
    where {math}`\theta` is an arbitrary rotation in isospin space. It is therefore a stronger statement of charge-_symmetry_. The eigenstates correspond to a set of _isobaric_ nuclei; nuclei with the same total number of nucleons.

+++

% Rotations about I2 and I1 correspond to shifts in I3 projection (need to show this mathematically). I2 can be formed from ladder operators (identity L+- = L1 +- iL2 (?)), so there is *some* clear relation.
As implied from the construction of {eq}`semi-empirical-mass-formula`, there is good evidence from measurements of nucleon-nucleon scattering lengths that the strong interaction is approximately charge-symmetric.{cite:ps}`machleidt_high-precision_2001` These same data indicate a stronger degree of charge-independence breaking, suggested by a larger (absolute) value for the _pn_ scattering length. It follows that _mirror_ nuclei, nuclei with exchanged proton and neutron numbers such as {math}`{ }^{11} \mathrm{C}` and {math}`{ }^{11} \mathrm{B}`, or {math}`{ }^{14} \mathrm{O}` and {math}`{ }^{14} \mathrm{C}`, should exhibit similar structures subject to modulation by the Coulomb interaction. 

The level schemes for a pair of mirror nuclei are shown in {numref}`level-scheme-11c-11b`. It is clear that the two nuclei posses very similar structures; the ordering between levels is closely matched, with a general decrease in excitation energy associated with the addition long-range spin-independent Coulomb potential seen in {math}`{}^{11}B`. For this reason, mirror nuclei can serve as useful tools for probing the structure of hard-to-measure nuclei, and elucidating the role of valence nucleons in stabilising deformed structures.

+++

:::{figure} image/placeholder/level-scheme-11c-11b.svg
:name: level-scheme-11c-11b

Level schemes of the {math}`{}^{11}C` and {math}`{}^{11}B` nuclei. The order and spacing between the levels is well preserved under exchange of the protons and neutrons, with only the {math}`\frac{7}{2}^{-}` and {math}`\frac{7}{2}^{-}` states changing in order. The states of the {math}`{}^{11}C` nucleus are observed to have lower energies (are more weakly bound), which follows from the increased long-range Coulomb repulsion between protons. Generated from data taken from the ENSDF database as of March 24th, 2023. Version available at <http://www.nndc.bnl.gov/ensarchivals/>
:::

+++

## Predicted Structures in {math}`{}^{14}C` and {math}`{}^{14}O`

+++

{ref}`Later in this chapter <experiment>`, an experimental measurement of the structure of {math}`{}^{14}O` is discussed. As the mirror of {math}`{}^{14}O`, {math}`{}^{14}C` is well studied. It therefore serves as a good foil against which to evaluate the performance of the measurement, in addition to the effects of charge-symmetry breaking upon the observed structure of the nucleus. As such, it is of interest to evaluate the landscape of structure predictions concerning the carbon analogue for which there is a greater body of research.

:::{figure} image/placeholder/a-14-isobar-levels.png
:align: center
:name: a-14-isobar-levels
:width: 400px

Lower energy levels of {math}`A=14` isobars, with adjusted energies relative to {math}`{}^{14}\mathrm{N}`. Levels in {math}`{}^{14}\mathrm{C}` and {math}`{}^{14}\mathrm{O}` have {math}`T=1`, whilst those in {math}`{}^{14}\mathrm{N}` have {math}`T=0` apart from those levels in common with the other members of the isobar. Figure taken from {cite:ps}`krane_introductory_1987`.
:::

+++

An exploration of the relationship between clustering and the deformed harmonic oscillator (DHO) model has been performed by {cite:authorpars}`freer_relationship_1995`, demonstrating that spherical harmonic oscillator (SHO) shell-model structure appears within the DHO for integer deformation ratios ({math}`\omega_x : \omega_y : \omega_z\,,\omega_i\in\mathcal{Z}`). The symmetries observed in these integral deformation ratios suggest that the deformed potential may instead be expressed in term of overlapping spherical oscillators. This provides a lens through which clustered structures may be understood as multi-centre spherical potentials. Subsequent work has applied this concept to propose the existence of a linear chain structure at a {math}`3:1` deformation. In this configuration, three quartets of paired protons and neutrons occupy the leading, degenerate SHO _s_ shells; whilst the two valence neutrons lie on perpendicular orbitals given by the shared {math}`p_\frac{3}{2}` state (see {numref}`dho-predicted-structures`). This chain is predicted to form a {math}`\pi`-orbital, which the DHO model associated with the lowest-energy linear chain system by minimising the axial deformation.{cite:ps}`von_oertzen_nuclear_2006` See {numref}`pi-sigma-bonds-13c` for the Hückel wave-function amplitudes that correspond to the valence nucleon orbits in {math}`{}^{13}C`.

:::{figure} image/placeholder/dho-predicted-structures.png
:align: center
:name: dho-predicted-structures
:width: 400px

Energy diagram of shell-model degeneracies for integer deformation ratios in an axially deformed harmonic oscillator. The open circles indicate the shells occupied by valence neutrons, whilst the shaded dots denote the shells occupied by the isospin-degenerate {math}`J_z=0` nucleon pairs that form an {math}`\alpha`-particle. Figure taken from {cite:ps}`von_oertzen_nuclear_2006`.
:::

% I *think* all of these are pi bonding, from the text:
% > In (a) and (b) the wavefunction comprises linear combinations of [001] singleparticle orbits which give rise to σ -bonding. In all other plots they comprise [100] orbits which generate π -bonds.
% This is *only* in huckel

:::{figure} image/placeholder/pi-sigma-bonds-13c.png
:align: center
:name: pi-sigma-bonds-13c
:width: 400px

One-dimensional molecular orbits for cluster states in {math}`{}^{13}\mathrm{C}`; showing {math}`\pi`. Note that the number of nodes {math}`[n_1 n_2 n_3]` increases with increasing oscillator quanta. In this 2D projection, the deformation axis lies in parallel to the plane normal. Figure adapted from {cite:ps}`mcewan_characterization_2004`.
:::

:::{note}
:class: margin

The term "multimer" refers to units of protein molecules comprised of two or more polypeptide chains. A "dimer" is a two-unit molecule.
:::

One of the earliest conjectures as to the existence of molecular structures in {math}`{}^{14}\text{C}` was that of a near-threshold {math}`{}^{9}\mathrm{Be} + {}^{5}\mathrm{He}` isomeric state at ~17.24 MeV given by {cite:authorpars}`von_oertzen_two-center_1996` (see (x) in {numref}`states-in-carbon-oertzen`). This prediction followed from the postulate that bound _multimers_ could be formed by adding helium isotopes to the known beryllium dimer structures, whereby the additional valence neutrons would form covalent bonds between the next two {math}`\alpha`-particles. 


:::{figure} image/states-in-carbon-oertzen.png
:align: center
:name: states-in-carbon-oertzen
:width: 400px

Energy diagrams of molecular chain states in carbon isotopes, adapted from {cite:ps}`von_oertzen_dimers_1997`. The predicted configurations for {math}`{}^{14}\mathrm{C}` are shown in the blue box.
:::

Extending the concept of near-threshold states, {cite:authorpars}`von_oertzen_dimers_1997` further anticipate resonances in the {math}`{}^{10}\mathrm{Be}^* + \alpha` system at 18 MeV. These resonances lie, below the ~18.8 MeV {math}`{}^8\mathrm{Be}+2n+\alpha` threshold, due to the covalent binding of the valence neutrons.{cite:ps}`von_oertzen_nuclear_2006` It was predicted that a series of four states would arise from the group of states at 6 MeV in {math}`{}^{10}Be^*` with spins {math}`0^+`, {math}`2^+`, {math}`1^-`, and {math}`2^-`. The reflection-symmetric {math}`\sigma`-orbit configuration, with valence nucleons distributed equally among the alpha particles (see (x) in {numref}`states-in-carbon-oertzen`), is expected to be found at lower energies than the asymmetric {math}`\pi`-orbit configuration due to the stronger binding effect of each valence neutron. It is anticipated to form a rotational band of {math}`0^+`, {math}`2^+`, and {math}`4^+`.{cite:ps}`von_oertzen_dimers_1997`

+++

The prolate linear-chain structures described above have two deformation modes, shown in {numref}`linear-chain-modes`. In the alpha-conjugate nucleus {math}`{}^{12}\mathrm{C}`, there is an absence of experimental evidence for pure linear chain structures, indicating that it is unstable with respect to these bending and breathing modes. {cite:authorpars}`itagaki_molecular-orbital_2001` have applied the Molecular Orbital model, discussed briefly in {ref}`content:nuclear-molecules`, to predict the behaviour of these conjected structures. The orbitals that are obtained by this method are classified in terms of their angular momentum projection and parity, {math}`K^\pi`.

:::{figure} image/linear-chain-modes.png
:align: center
:name: linear-chain-modes
:width: 300px

Schematic illustration of the deformation modes of linear-chain states. (a) shows the _breathing_ mode in which the center-separation {math}`d` varies, whilst (b) depicts the _bending_ mode that depends upon the bending angle {math}`\theta`. Figure taken from {cite:ps}`itagaki_molecular-orbital_2001`.
:::

:::{note}
:class: margin

The excitation energy is naively expected to increase with respect to the number of nodes along the molecular axis. Yet the {math}`{}^{14}\mathrm{C}\pqty{1/2^-_\sigma}^2` configuration is only 14 MeV higher than the {math}`\pqty{3/2_\pi^-}^2` configuration. This is likely a result of clustering of the core, due to the prolonged shape along the molecular axis.{cite}`itagaki_molecular-orbital_2001`
:::
Calculations of {math}`{}^{14}\mathrm{C}` for the given configurations identify minima in the binding energy with respect to molecular center separation; the {math}`{}^{14}\mathrm{C}\pqty{3/2^-_\pi}^2` configuration appears minimal at an excitation energy of ~18 MeV.{cite:ps}`itagaki_molecular-orbital_2001` Whilst the {math}`{}^{14}\mathrm{C}\pqty{1/2^-_\sigma}^2` configuration is predicted to exhibit a minimum at ~32 MeV, it is not sufficiently deep enough to be associates with stability against breathing-mode deformation. Against bending-mode deformation, {cite:authorpars}`itagaki_molecular-orbital_2001` do not predict stability for any of the molecular configurations in {math}`{}^{14}\mathrm{C}`. Such stability is only predicted for {math}`{}^{16}\mathrm{C}\pqty{\pqty{3/2^-_\pi}^2\pqty{1/2^-_\sigma}^2}`, due to the overlap between the two neutrons in the {math}`\pi` orbit and the two neutrons in the {math}`\sigma`; an increase in mutual overlap between the valence orbitals leads to a decrease in the total-wavefunction overlap component due to Pauli blocking.{cite:ps}`itagaki_molecular-orbital_2001`

+++

{cite:authorpars}`milin_search_2002` briefly predict the existence of three-center states in {math}`{}^{14}\mathrm{C}` that build upon the molecular orbital structures identified for {math}`{}^{13}\mathrm{C}`; {math}`\pqty{\pi}^2`, {math}`\pqty{\sigma}^2`, and {math}`\pqty{\pi\otimes \sigma}`. The dominant structures are conjectured to be based upon the ground state {math}`K = 0 \pqty{\pi}^2`, the excited state {math}`K = 0 \pqty{\sigma}^2`, and the {math}`K = 1^-\pqty{\sigma \times \pi}` state of {math}`{10}\mathrm{Be}.`

+++

A long conjectured state in three-alpha systems is that of an equilateral triangle configuration, which would exhibit a series of rotational bands starting at {math}`3^-` and {math}`0^+`.{cite:ps}`bijker_algebraic_2002`{cite:ps}`itagaki_equilateral-triangular_2004` Though such a state lies above the three-alpha threshold in {math}`{}^{12}\mathrm{C}`, it is expected that the valence neutrons of {math}`{}^{14}\mathrm{C}` should stabilise the triangular configuration. Using the Generator Coordinate Method (GCM, see {ref}`content:models-excited-states`), {cite:authorpars}`itagaki_equilateral-triangular_2004` make a series of predictions for the energy levels in {math}`{}^{14}\mathrm{C}`, identifying the two aforementioned rotational bands (see {numref}`equilateral-levels-parity`. It is observed experimentally that the second {math}`3^-` band is easily excited by {math}`\alpha` transfer, which indicates an alpha-cluster structure. Simultaneously, the band based upon the (fourth) {math}`0^+` state is observed to exhibit strong B(E2) transition rates, supporting the indication of a rotational band. The authors emphasise the difference between the Ikeda near-threshold clustering, with localised excess neutrons, and the crystalline alpha-condensate structures that can form well below the threshold energy due to the stabilisation of the delocalised valence neutrons. This observation represents a distinct mechanism for cluster states beyond the localised molecular orbits seen in the linear-chain structures.

::::{subfigure} AAABBBBBB
:layout-sm: A|B
:gap: 8px
:subcaptions: below
:name: equilateral-levels-parity

:::{image} image/equilateral-levels-positive.png
:alt: (a)

:::

:::{image} image/equilateral-levels-negative.png
:alt: (b)
:::

Energy levels in {math}`{}^{14}\mathrm{C}` for negative (a) and positive (b) parity states. Energies are measured relative to the {math}`{}^{10}\mathrm{Be} + \alpha` threshold, and the experimental states are plotted against the predictions for comparison. Figure taken from {cite:ps}`itagaki_equilateral-triangular_2004`.
::::

+++

In a large work that undertakes a systematic review of experimental data, {cite:authorpars}`von_oertzen_search_2004` identify single-particle states with oblate shapes, and prolate states with nontrivial structure associated with the low-lying oblate structure of {math}`{}^{12}C`. These latter states are proposed to have strong {math}`\alpha`-clustering and form rotational bands with signature parity inversion doublets and a high moment of inertia. The complete set of anticipated structures is schematically depicted in {numref}`cluster-structures-14c`. This work finds itself in agreement with {cite:ps}`itagaki_equilateral-triangular_2004` as to the existence of an oblate triangular configuration with {math}`K^\pi = 0^+,\,3^-` band heads. {cite:authorpars}`von_oertzen_search_2004` ascribe the prolate structures at {math}`0_3^+,\,1_2^-` to chain structures, though do not go so far as to identify these as either the symmetric or anti-symmetric structures described above.

+++

:::{figure} image/cluster-structures-14c.svg
:align: center
:name: cluster-structures-14c
:width: 300px

Schematic illustration of the cluster structures anticipated in {math}`{}^{14}\mathrm{C}` for various valence neutron configurations. (a) depicts the symmetric, positive parity {math}`\alpha+n+\alpha+n+\alpha` configuration with the valence neutrons distributed outside of the symmetry axis; (b) shows the reflection-asymmetric inversion doublets, based upon {math}`{}^{10}\mathrm{Be}+\alpha` structure with the valence neutrons in the same covalent {math}`\pi`-bond; and (c) illustrates the oblate traignular-cluster states with {math}`\sigma`-bonds between two {math}`\alpha`-particles.
:::

+++

Results of performing AMD simulations of the negative parity and positive parity states are given in {cite:ps}`suhara_cluster_2011`. The findings agree with the existing experimental level assignments such as those described in {cite:ps}`von_oertzen_search_2004`.  In particular, both shell-model and oblate/triaxial structures are identified at low energies below the {math}`{}^{10}\mathrm{Be}+\alpha` threshold. The triaxial structures are observed in {math}`K^\pi=0^+` and {math}`K^\pi=2^+` bands, with the excess neutrons occupying the _sd_-like orbitals.{cite:ps}`suhara_cluster_2011` A prolate {math}`K^\pi=0^+` band is also identified thereafter, with valence neutrons localised about two of the three alpha clusters. Such a configuration suggests a {math}`{}^{!0}\mathrm{Be}` correlation, in agreement with prior experiment. An investigation of the above-threshold decay in {math}`{}^4\mathrm{He}\pqty{{}^{10}\mathrm{Be},\alpha}{}^{10}\mathrm{Be}` by {cite:authorpars}`freer_resonances_2014-1` provides some agreement with this structure determination, but notes that lower excitation energies would be useful to observe the angular distributions required to resolve the structural identity with more detail.{cite:ps}`freer_resonances_2014-1` Further AMD work by {cite:authorpars}`baba_structure_2016` adds to the theoretical support for linear-chain structures in {math}`{}^{14}\mathrm{C}`, and remarks that the observation of decays to both the ground and {math}`2^+` states in {math}`{}^{10}\mathrm{Be}` would serve as additional evidence for linear chain formation. With these results, there is still little evidence for linear chain structures in negative parity.{cite:ps}`baba_structure_2016` A recent experimental work{cite:ps}`yamaguchi_experimental_2017` has been performed in a similar manner to this work, using resonant scattering in inverse kinematics. The findings of this work indicate the existence of several alpha-cluster-like states in the 14 MeV–19 MeV excitation energy region. The observed spin-parities, and level separation, is given as a strong indication of the linear-chain cluster state (LCCS) structure.

+++

Of particular relevance to this work is that of {cite:authorpars}`baba_coulomb_2019` which considers the Coulomb shift of the mirror pair {math}`{}^{14}C` and {math}`{}^{14}O`. The AMD calculations performed in this work suggest that the excitation energy of the {math}`\pi`-bond linear chains seen in {math}`{}^{14}C` should lie close to those in {math}`{}^{14}O`, with similar decay widths. The findings for the {math}`\sigma`-bond chain are somewhat different; it is anticipated that the levels in {math}`{}^{14}C` have both larger decay widths, and distinctly higher excitation energies, which are ascribed to a large Thomas-Ehrman shift (see {numref}`states-in-14c-14o`).

::::{subfigure} AAABBBBBB
:layout-sm: A|B
:gap: 8px
:subcaptions: below
:name: states-in-14c-14o

:::{image} image/states-in-2+-14c-14o.png.svg
:alt: (a)

:::

:::{image} image/states-in-4+-14c-14o.png.svg
:alt: (b)
:::

States in {math}`{}^{14}\mathrm{C}` and {math}`{}^{14}\mathrm{O}` determined by AMD calculation. Close correspondence between the {math}`\pi`-bond chain states is observed, whilst the {math}`\sigma`-bond levels are expected to differ significantly in excitation energy and decay width. Figure taken from {cite:ps}`baba_coulomb_2019`.
::::

```{code-cell}

```

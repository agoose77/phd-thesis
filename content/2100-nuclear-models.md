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

# Nuclear Models

When describing the nucleus, it may appear that the most natural degrees of freedom are those of the constituent nucleons: their spins, isospins, and positions. From these parameters arises a set of microscopic models, which vary according to the assumptions and symmetries used to render an otherwise intractable computation feasible. These models are sensitive to the nucleon-nucleon interaction, for which there is no analytical theory. It is also possible to describe the nucleus in terms of the _collective_ degrees of freedom, such as the centre-of-mass, or quadrupole moment. The challenge of aligning these two descriptions of the nucleus is a significant, on-going effort in the research community.

+++

## Macroscopic Models

(liquid-drop-model)=
### Liquid Drop Model
First described in 1935, the Semi Empirical Mass Formula (SEMF) is an approximation for the ground-state binding energy of a nucleus according to its proton and neutron numbers {cite:ps}`weizsacker_zur_1935`. Inspired by the liquid drop model, which considers the nucleus as a drop of incompressible fluid, it comprises of several theoretically-motivated terms (see {numref}`liquid-drop-schematic`):

:::{math}
:label: semi-empirical-mass-formula

E_B = \underbrace{a_VA}_{\text{volume}} - \underbrace{a_SA^{\frac{2}{3}}}_{\text{surface}} - \underbrace{a_C\frac{Z(Z-1)}{A^{\frac{1}{3}}}}_{\text{coulomb}} - \underbrace{a_A\frac{(N-Z)^2}{A}}_{\text{asymmetry}} + \underbrace{\delta(N, Z)}_{\text{pairing}}\,.
:::

Volume energy
: The attractive-repulsive potential of the strong force. The short effective range of the strong interaction means that it is effectively constrained to a constant number of neighbours.

Surface energy
: A corrective term to account for nucleons at the surface of the nucleus, which have fewer neighbours than those at the centre of the drop.

Coulomb energy
: Coulombic repulsion between positively charged protons reduces the binding energy.

Asymmetry energy
: Given the Paul exclusion principle, nuclei of {math}`N = Z` should have higher binding energies than those for which {math}`N \neq Z`. 

Pairing energy
: Identical nucleons with anti-aligned spins in the same spatial state have maximal wavefunction overlap, and correspondingly an enhanced binding energy.

It will be useful to discuss some of the features of this model in subsequent sections. For now, it suffices to say that the liquid-drop model (or semi-empirical mass formula) produces a reasonable prediction of the binding energy of a wide range of nuclei, particularly for heavier nuclei.

+++

:::{figure} image/liquid-drop-model.svg
:name: liquid-drop-schematic
:width: 512px
:align: center

Illustration of the physical interpretation of the terms that comprise the liquid-drop nature of the SEMF.
Figure by Daniel FR, distributed under a [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en) license.
:::

+++

(nuclear-models:rotor-model)=
### Rotor Model
Under the symmetry of the spherical shell model, eigenstates {math}`\ket{j m}` of the angular-momentum projection operator are degenerate with respect to the Hamiltonian; it is only the total momentum {math}`j` that, under the spin-orbit interaction, yields distinct eigenvalues. Within a _deformed_ system, however, it becomes possible to define an orientation, and the degeneracy of {math}`\ket{j m}` is lifted. This deformation may be invariant with respect to particular rotational subgroup(s), e.g. axially symmetric deformations, such that the orientation of the system is only partially defined and restrictions are imposed on the rotational degrees of freedom. 

The lowest-order measure of stable deformation of a state is given by the (electric) quadrupole moment {math}`Q = \expval{\hat{Q}_0}{JM=J}` of the nucleus, which is measured such that the space-fixed {math}`\hat{z}` component is maximal. When measuring these values for the 2+ states even-even nuclei, a trend towards large, negative values is observed in the mid-shell region, whilst near to shell closures the quadrupole moment is significant diminished. Odd-mass singly-near-singly closed nuclei demonstrate small negative Q values, corresponding to valence nucleons polarising a spherical core, whereas large _prolate_ deformations are seen in the mid-shell region {cite:ps}`rowe_fundamentals_2010`.

When a charged object with a quadrupole moment undergoes rotation, it emits quadrupole (E2) radiation. It follows that the E2 transition rates serve as an indicator of deformation; when the reduced transition rate (B(E2)) values are expressed in terms of single-particle (Weisskopf) strengths (the typical strengths observed for single-nucleon transitions), it is clear that some of these transitions must involve _collective_ excitations of many correlated nucleons. It transpires that both the large prolate and large oblate Q values observed in doubly-open mid-shell even-even and odd-mass nuclei can be explained through the _rotor model_ (see {numref}`prolate-oblate-rotor`).

+++

::::{subfigure} AAABBBBBB
:layout-sm: A|B
:gap: 8px
:subcaptions: below
:name: prolate-oblate-rotor

:::{image} image/prolate-rotor.svg
:alt: (a)

:::

:::{image} image/oblate-rotor.svg
:alt: (b)
:::

Schematic illustration of the measured quadrupole moment {math}`Q` for an axially symmetric rotor. (a) shows the configuration in which the rotor symmetry axis {math}`3` is maximally aligned with the space-fixed axis {math}`z`. (b) depicts a state in which the {math}`3` axis is approximately perpendicular to the {math}`z` axis; in this case, the {math}`3`-projected momentum is zero. Under the rotor model, both the oblate doubly-even and prolate odd-mass nuclei measurements are explained by an intrinsic prolate deformation. Adapted from Ref. {cite:ps}`rowe_fundamentals_2010`.
::::

+++

A quantum mechanical rotor has the Hamiltonian
:::{math}
\hat{H}_\text{rot} = \frac{\hbar^2}{2}\bqty{
    \frac{\hat{R}_1^2}{\mathcal{I}_1} + \frac{\hat{R}_2^2}{\mathcal{I}_2} + \frac{\hat{R}_3^2}{\mathcal{I}_3}
}\,.
:::
With the inclusion of intrinsic degrees of freedom, this Hamiltonian would also possess an intrinsic term that couples with the extrinisic components; if the nucleus has intrinsic angular momentum {math}`\vb{J}`, then the total angular momentum is given by the vector sum
:::{math}
\hat{\vb{I}} = \hat{\vb{R}} + \hat{\vb{J}}\,.
:::
It can be shown that the Hamiltonian factors into intrinsic, rotational, and Coriolis terms
:::{math}
\underbrace{
    \hat{H}'_\text{rot}
}_\text{rotational} +
\underbrace{
    \hat{H}_\text{intr}
}_\text{intrinsic} - 
\underbrace{
    \sum_i{
        \frac{\hbar^2}{\mathcal{I_i}}\hat{I}_i\hat{J}_i
    }
}_\text{Coriolis interaction}
\,,
:::
where 
:::{math}
\hat{H'}_\text{rot} = \sum_i{
    \frac{\hbar^2}{2\mathcal{I_i}}\hat{I}^2_i
}
\,
:::
(see {cite:ps}`rowe_fundamentals_2010`).

+++

An _additional_ coupling term arises if the moments of inertia depends upon the intrinsic variables. However, one can ignore both of these coupling interactions to define the _adiabatic approximation_ which omits the coupling terms. For an _axially symmetric_ rotor, {math}`\hat{H}'_\text{rot}` admits analytical solutions for the ground-state band, with energy eigenvalues
:::{math}
:label: rotor-energies
E'_{KI} = \frac{\hbar^2}{2}\bqty{\frac{I(I+1)}{\mathcal{I}} + \pqty{\frac{1}{\mathcal{I}_3} - \frac{1}{\mathcal{I}}}K^2}\,,
:::
and corresponding eigenvectors satisfying
:::{math}
\hat{I}^2\ket{KIM} = I(I+1)\ket{KIM}

\hat{I}_z\ket{KIM} = M\ket{KIM}

\hat{I}_3\ket{KIM} = K\ket{KIM}
:::
where {math}`K` is the eigenvalue of the {math}`\hat{I}_3` operator (see {numref}`rotor-frame`). In this model, {math}`M` and {math}`K` are good quantum numbers, and {math}`K` defines a band of states for increasing {math}`I`. For excited states, the {math}`K` and {math}`\mathcal{I}` parameters may differ from the ground state, generalising {eq}`rotor-energies` to
:::{math}
:label: rotor-energies-excited
E_{\alpha KI} = \frac{\hbar^2}{2\mathcal{I}_{\alpha}}{I(I+1)} + E_{\alpha K}\,,
:::
where {math}`\alpha` indicates the excited state.

+++

:::{figure} image/rotor-frame.svg
:name: rotor-frame
:width: 256px
:align: center

Relationship between the total angular momentum {math}`\vb{I}`, the intrinsic angular momentum {math}`\vb{J}`, the rotor angular momentum {math}`\vb{R}`, and the components {math}`M` of {math}`\vb{I}` along the fixed axis {math}`z`; and {math}`K` the symmetry axis. Adapted from Ref. {cite:ps}`rowe_fundamentals_2010`.
:::

+++

Under the adiabatic limit, it is reasonable to consider the intrinsic structure of the nucleus to be independent of extrinsic rotational angular momentum {cite:ps}`rowe_nuclear_2010`. We may partition the quantum state of the system into intrinsic ({math}`K`) and extrinsic ({math}`I,M`) Yet, the same cannot be said for the _symmetries_ of each frame. For an axially symmetric rotor with reflection symmetry (in the plane whose normal is co-linear with the symmetry axis), it is not possible to distinguish rotations about the symmetry axis of the intrinsic frame. It follows that the total angular momentum component {math}`I_3` is given by the projection {math}`J_3` of the _intrinsic_ angular momentum onto the symmetry axis, i.e. it is exclusively a function of the intrinsic state. This eliminates the degree of freedom associated with rotation around {math}`\vu{3}`.

+++

(expt:parity-doublets)=
#### Parity Doublets
Simultaneously, if the intrinsic Hamiltonian is invariant with respect to a rotation {math}`\mathcal{R}_2(\pi)` about an axis perpendicular to the symmetry axis, a further reduction in the rotational (extrinsic) degrees of freedom is possible. This intrinsic symmetry operator {math}`\mathcal{R}_i = \mathcal{R}_2(\pi)` has corresponding eigenvalues {math}`r = \pm 1` as {math}`\mathcal{R}_i^2 = \mathcal{R}_2(2\pi) = +1`. The {math}`K=0` state is an eigenfunction of this operator. Meanwhile, the same symmetry in the extrinsic frame {math}`\mathcal{R}_e = \mathcal{R}_i` yields eigenvalues of {math}`-1^I` for this {math}`K=0` state, which follows from the behaviour of the spherical harmonics {cite:ps}`bohr_nuclear_1977`, such that we have 
:::{math}
:label: rot-eigen
r = -1^I
::: 
{eq}`rot-eigen` admits two families of solutions; {math}`I=0,2,4,\dots` for the positive {math}`r=+1` eigenvalue of {math}`\mathcal{R}_i`, and {math}`I=1,3,5,\dots` for the negative {math}`r=-1`  counterpart. For reflection-symmetric axially-asymmetric structures, this gives rise to a phenomenon known as "parity inversion doublets", in which both solutions are seen with an associated energy splitting {cite:ps}`beck_clusters_2014`.

For the {math}`K \neq 0` states, it does not hold that they are eigenfunctions of {math}`\mathcal{R}_i`. Upon expanding the intrinsic state in components of the total angular momentum, it can be shown that in order for {math}`\mathcal{R}_i = \mathcal{R}_e`, a superposition of {math}`K,\overline{K}` solutions (where {math}`\overline{K}=-K`) is required such that from two intrinsic states {math}`K,\overline{K}` a single rotational state is defined.

+++

## Microscopic Models
% Reference: TIME EVOLUTION IN QUANTUM DOTS, Sigve Bøe Skattum

+++

### Many Body Systems

+++

For a system of {math}`N` indistinguishable particles, the canonical many-particle basis is given by the direct-product of the single-particle states:
:::{math}
\ket{\lambda_1 \lambda_2 \dots \lambda_N}_{\text{C}} &= \ket{\lambda_1} \otimes \ket{\lambda_2} \otimes \dots \otimes \ket{\lambda_N}

                        &= \ket{\lambda_1}\ket{\lambda_2}\dots\ket{\lambda_N}\,.
:::
However, an arbitrary state in this basis is not guaranteed to satisfy the anti-symmetry requirements of a fermionic system such as the nucleus (under isospin symmetry). These anti-symmetric states are given by _permutations_ of the canonical basis vectors (via the anti-symmetrisation operator {math}`\hat{\mathcal{A}}`)
:::{math}
\ket{\lambda_1 \lambda_2 \dots \lambda_N}_{\text{AS}} 
&= \hat{\mathcal{A}}\Bqty{\ket{\lambda_1} \otimes \ket{\lambda_2} \otimes \dots \otimes \ket{\lambda_N}}

&= \frac{1}{N !} \sum_{P \in S_{N}}(-1)^{\pi} \hat{P}\pqty{\ket{\lambda_1}\otimes\ket{\lambda_2} \otimes \dots \otimes \ket{\lambda_N}} \,.
:::

+++

It is usually more convenient to explore nuclear theory in terms of the language of second quantisation, which intrinsically embodies the anti-symmetrisation requirement through the creation and annihilation operators {cite:ps}`eisenberg_microscopic_1976`. Subsequently, states are most naturally described using occupation number representation
:::{math}
\ket{n_1 n_2 \dots}_{\text{OR}}\,,
:::
where {math}`n_1` indicates the number of particles in the single-particle state {math}`1`.

+++

The Hamiltonian of a quantum system is the operator {math}`\hat{H}`, conventionally given as the sum of kinetic and potential energy operators
:::{math}
:label: hamiltonian
\hat{H} = \hat{T} + \hat{V}\,,
:::
whose eigenvalues correspond to the set of measurable energies. Considering up-to two-body interactions, we can write {eq}`hamiltonian` in second quantization form as

:::{math}
:label: hamiltonian-2q

\hat{H} = 
\sum_{\alpha\beta}T_{\alpha \beta}\underbrace{\hat{a}^\dagger_\alpha\hat{a}_\beta}_\text{one-body} + 
\frac{1}{2}\sum_{\alpha\beta\gamma\delta}V_{\alpha\beta\gamma\delta}\underbrace{\hat{a}^\dagger_\alpha\hat{a}^\dagger_\beta\hat{a}_\delta\hat{a}_\gamma}_\text{two-body}\,,
:::
where {math}`\hat{T}` is the kinetic energy operator and {math}`\hat{V}` is the two-body inter-nucleon interaction.

:::{note}
:class: margin

See {cite:ps}`constantinou_natural_2017` for a discussion of alternate representations of 
{math}`\frac{1}{2}\sum_{\alpha\beta\gamma\delta}V_{\alpha\beta\gamma\delta}{\hat{a}^\dagger_\alpha\hat{a}^\dagger_\beta\hat{a}_\delta\hat{a}_\gamma}`, e.g. 
{math}`\frac{1}{4}\sum_{\alpha\beta\gamma\delta}\overline{V}_{\alpha\beta\gamma\delta}{\hat{a}^\dagger_\alpha\hat{a}^\dagger_\beta\hat{a}_\delta\hat{a}_\gamma}`
:::

+++

### Mean Field Theory
{eq}`hamiltonian-2q` could be recast in terms of an artificial single-particle potential {math}`\hat{U}`

:::{math}
:label: hamiltonian-2q-mean-field

\hat{H} &= 
\underbrace{\sum_{\alpha\beta}\pqty{T_{\alpha \beta} + U_{\alpha\beta}}\hat{a}^\dagger_\alpha\hat{a}_\beta}_\text{single particle Hamiltonian} + 
\underbrace{
    \frac{1}{2}
    \sum_{\alpha\beta\gamma\delta}
        V_{\alpha\beta\gamma\delta} 
            \hat{a}^\dagger_\alpha\hat{a}^\dagger_\beta\hat{a}_\delta\hat{a}_\gamma - 
    \sum_{\alpha\beta}
        U_{\alpha\beta}
            \hat{a}^\dagger_\alpha\hat{a}_\beta
}_\text{residual interaction}\,,

        &= \hat{H}^{[1]} + \hat{V'}\,,
:::
where {math}`\hat{H}^{[1]}` is the single-particle Hamiltonian, and {math}`\hat{V'}` is a _residual_ interaction between nucleons. In the event that this residual interaction is small, it can be treated as a perturbation of the single-particle Hamiltonian. Under this simplification, the problem of solving the many-body Schrodinger equation is reduced to that of solving the single-particle Schrödinger equation for an external potential

:::{math}
:label: mean-field-single-particle-hamiltonian
\hat{H}^{[1]}\ket{\phi_k} = E_k\ket{\phi_k}\,.
:::

:::{note}
:class: margin
Some authors use the term "quasiparticles", which conflicts with the same term used to describe Bogoliubov quasiparticles in HFB pairing correlation theory. In any case, "particles" distinguishes between bare nucleons and those which are "dressed" by the interaction that has already been accounted for by the mean field {cite:ps}`zelevinsky_physics_2017`.
:::

Hence, the introduction of a particular single-particle potential transforms the problem from a strongly interacting system of nucleons to a weakly interacting system of particles {cite:ps}`suhonen_nucleons_2007`. The residual interaction {math}`\hat{V'}`, whose matrix elements are much reduced in amplitude with respect to the bare two-nucleon potential, is responsible for configuration mixing between single-particle states, i.e. correlating otherwise independent nucleons {cite:ps}`rowe_fundamentals_2010`.

+++

In the context of the nucleus, the existence of a single-particle potential corresponds to a _mean-field_, whose origin is the motion of the nucleons themselves. The physical justification for introducing a mean-field potential {math}`\hat{U}` depends upon whether one-body behavior or two-body collisions dominate within the nucleus, i.e. whether the nucleon mean-free-path is much greater than, or lesser than the nuclear size {cite:ps}`negele_mean-field_1982`. Despite the strong short-range repulsive nature of the strong nuclear force, through Pauli blocking of states close to the Fermi surface it can be shown that nucleons behave to first approximation as independent particles i.e. comprise an Independent Particle Model (IPM) {cite:ps}`fetter_quantum_1972`.

In occupation representation, a general state {math}`\ket{\phi}` is written as
:::{math}
:label: general-wavefunction
\ket{\phi} = \sum_{i_1i_2\dots i_N}c_{i_1i_2\dots i_N}\hat{a}^\dagger_{i_1}\hat{a}^\dagger_{i_2}\dots \hat{a}^\dagger_{i_N}\ket{0}\,,
:::
where {math}`\ket{0}` is the vacuum state, and the number of combinations of {math}`i_1i_2\dots i_N` is given by {math}`{N_c \choose N}`. Clearly, despite the introduction of a single-particle approximation (imposed by the supposition of a mean-field), {eq}`mean-field-single-particle-hamiltonian` remains an intractable problem unless a simplification is used reduce the size of the model space. There are two predominant mechanisms for proceeding: 
- Restrict the number of active particles and states (constrain {math}`N_c` and {math}`N`)
- Choose a restricted many-particle form (constrain {math}`\ket{\phi}`) {cite:ps}`rowe_fundamentals_2010`.

The former approach underpins the shell model, whilst the latter describes the high-level procedure of the Hartree-Fock Approximation.

% TODO HF still useful for SM to give a good basis?

+++

### Hartree Fock

The question that follows {eq}`hamiltonian-2q-mean-field` is that of how to determine {math}`\hat{U}` such that {math}`\hat{V}'` is minimised. A natural candidate would be one of the phenomenological potentials, such as the Woods-Saxon model, or an analytical potential such as the Harmonic Oscillator. However, these are ultimately simplifications of the nuclear potential. A proper treatment of the mean field must produce a _self-consistent_ solution in which the field generated by the motion of the nucleons agrees with that used to derive the wavefunction of the system {cite:ps}`zelevinsky_physics_2017`. One such treatment is the Hartree-Fock (HF) approximation method. 

Though a detailed discussion of HF will not be performed here, it suffices to establish the assumptions and conclusions of the method. In order to restrict the model space of the many-particle problem to a tractable subset, the HF method assumes that the ground state of the system is described by a single Slater-determinant of single-particle eigenfunctions. Therefore, instead of {eq}`general-wavefunction`, we have
:::{math}
\ket{\text{HF}} = \hat{a}^\dagger_{i_1}\hat{a}^\dagger_{i_2}\dots \hat{a}^\dagger_{i_N}\ket{0}\,.
:::
This assumption is most appropriate for doubly-closed nuclei, where there is a large energy gap between the first unfilled single-particle level and the ground state {math}`\ket{\text{HF}}` such that the gound state is reasonably stable {cite:ps}`ring_nuclear_2004` {cite:ps}`rowe_nuclear_2010`.
:::{note}
:class: margin
Details on the HF method are given in {cite:ps}`ring_nuclear_2004`. Historically calculations have been performed using a suitable, complete basis e.g. the Harmonic Oscillator basis, [truncated to a required accuracy](https://web.ornl.gov/~kentpr/thesis/pkthnode13.html#SECTION00730100000000000000). In recent times, discretised finite-element calculations have been used in atomic physics to directly compute the solution.
:::

+++

#### Variational Principle

The mean field is ultimately derived through the variational principle, which seeks to determine {math}`\ket{\phi}` such that {math}`\hat{H}^{[1]}` is minimised with respect to small admixtures of Slater determinants:
:::{math}
:label: variational-principle
\delta\pqty{\expval{\hat{H}}{\phi} -E\braket{\phi}} = \matrixel{\delta\psi}{\hat{H}}{\psi} - E\braket{\delta\psi}{\psi} = 0\,,
:::
where {math}`\ket{\delta\psi} = \varepsilon \hat{a}^\dagger_k\hat{a}_j\ket{\psi}` for some arbitrary {math}`\varepsilon`, and {math}`k>N,j\leq N` {cite:ps}`rowe_fundamentals_2010` {cite:ps}`greiner_nuclear_1996`. If the {math}`N`-lowest energy single-particle eigenfunctions are taken as the HF ground-state, then these admixtures correspond to single "particle-hole" (1p1h) excitations of the closed "core" that lies below the sharp Fermi surface (see {numref}`sharp-fermi-surface`).
:::{note}
:class: margin

The single-particle eigenfunctions form a complete basis (subject to truncation), which facilitates the introduction of excited states above the ground state. 
:::

:::{figure} image/placeholder/sharp-fermi-surface.png
:width: 384px
:name: sharp-fermi-surface

Labelling of particle and hole states relative to a sharp Fermi surface, that follows from the restricted Slater determinant form of the HF ground state {math}`\ket{\text{HF}}`. Figure taken from Ref. {cite:ps}`rowe_nuclear_2010`.
:::

The process of determining the eigenstates of {math}`\hat{H}^{[1]}` is given by the following recurrence relation {cite:ps}`rowe_nuclear_2010`:
:::{math}
\left\{\ket{\text{HF}_\pqty{0}}\right\} \rightarrow \hat{U}^\pqty{0} \rightarrow \left\{\ket{\text{HF}_\pqty{1}}\right\} \rightarrow \hat{U}^\pqty{1} \rightarrow \dots
:::

+++

:::{note}
:class: margin
The anti-symmetrised form {math}`\overline{V}_{\alpha\gamma\beta\gamma}` follows from the variational equation {cite:ps}`greiner_nuclear_1996`. 

A challenge with the direct application of the HF method is the infinite matrix elements {math}`\overline{V}_{\alpha\gamma\beta\gamma}` that follow from the hard-core nature of the bare nucleon-nucleon potential. Extensions to Hartree-Fock, like Brückner-Hartree-Fock (BHF), replace this bare potential with an effective potential e.g. the Brückner {math}`G`-Matrix {cite:ps}`ring_nuclear_2004`.

% TODO - G matrix vs effective forces in other textbooks like Wong?
:::
It can ultimately be shown that the HF Hamiltonian is
:::{math}
\hat{H} = 
\sum_{\alpha\beta}\pqty{T_{\alpha \beta} + \sum_{\gamma}\overline{V}_{\alpha\gamma\beta\gamma}}\hat{a}^\dagger_\alpha\hat{a}_\beta\,,
:::
where {math}`\hat{\overline{V}}` is the anti-symmetrised interaction potential. This implies that the mean field {math}`\hat{U}` from {eq}`hamiltonian-2q-mean-field` is
:::{math}
\hat{U} = \sum_{\alpha\gamma\beta}\overline{V}_{\alpha\gamma\beta\gamma}\hat{a}^\dagger_\alpha\hat{a}_\beta\,,
:::
i.e. the averaged two-body contributions from the {math}`N-1` remaining nucleons {cite:ps}`rowe_fundamentals_2010` {cite:ps}`greiner_nuclear_1996`.
Primitive excited states can then be constructed from one-particle/one-hole (1p1h) and two-particle/two-hole (2p2h) excitations of this ground state {cite:ps}`rowe_nuclear_2010`.

% NB for those computing the HF ground state - the expectation value of the GS energy <φ|H|φ> is not the sum of the SP energies - this follows from the fact that the mean-field potential between two nucleons in a two-particle nucleus is the same, so including it for each nucleon leads to double counting. {cite:ps}`suhonen_nucleons_2007`

+++

Whether the minimum found by the HF procedure is a true global minimum depends upon the initial configuration. If the initial configuration determined by the trial wave-functions lie close to a shape-isomeric state, it is quite possible for the numerical procedure to settle upon a configuration that is deformed from the ground state {cite:ps}`greiner_nuclear_1996`. The variational principle outlined in {eq}`variational-principle` can be extended to include a deformation constraint that restricts e.g. the quadrupole moment {math}`Q` of the nucleus (see {numref}`energy-vs-deformation`).
:::{figure} image/placeholder/energy-vs-deformation.png
:name: energy-vs-deformation
:width: 300px
:align: center

Schematic diagram of the convergence of different HF trial wave-functions to local minima with distinct quadrupole moments {math}`Q` corresponding to a deformed isomer and subsequent fissioning of the nucleus. Figure taken from Ref. {cite:ps}`greiner_nuclear_1996`. 
:::

%TODO: mention core polarization (greiner_nuclear_1996)

+++

#### Residual Interaction

+++

Whilst the HF approximation generates a set of self-consistent single-particle states, it does so by explicitly ignoring the residual interaction. The variational principle requires that the single-particle Hamiltonian matrix element satisfies {math}`\mel{\delta \psi}{\hat{H}}{\psi} = 0`, where {math}`\ket{\delta \psi} = \sum_{mi}\epsilon_{mi} \hat{a}^\dagger_m\hat{a}_i\ket{\psi}`. This is equivalent to requiring that the Hamiltonian does not couple one-particle-hole excitations to the ground state (i.e., no residual interaction). A significant component of this interaction is the short-range pairing correlation, discussed in {numref}`liquid-drop-model`, that couples like-pairs of nucleons to states of zero angular momentum {cite:ps}`rowe_fundamentals_2010`. This is most evident in nuclei with pairs of protons or neutrons outside of doubly-closed shells {cite:ps}`rowe_fundamentals_2010`.[^ignore-pairing] 
% NOTE: why isn't pairing taken into account for HF mean field? Can it be seen in the second quantisation form of the HFB /BCS operator vs the mean-field term?
% NOTE: Even for deformed nuclei, where there is no longer degeneracy of different j projections, Kramer's theorem holds that there exists a time-reversed analogue state {cite:ps}`Wigner1932`. {cite:ps}`rowe_fundamentals_2010` %p530

Extensions to the Hartree-Fock method have been developed to consider the pairing interaction: 
- the Bardeen-Cooper-Schrieffer (BCS) model introduces a generalised pair creation operator for even-even nuclei of the form {math}`A^{+}=\sum_{k>0} \frac{v_k}{u_k} a_k^{+} a_k^{+}` to build the BCS ansatz: {math}`\mathrm{BCS}\rangle \propto \exp \left(A^{+}\right)|-\rangle=\sum_{r=0}^{\infty} \frac{1}{n !}\left(A^{+}\right)^r|-\rangle`. The resulting Hamiltonian is constrained to conserve particle number {math}`N`. Unlike the base HF method, the BCS model is not self-consistent; the pairing field does not change the single-particle wavefunctions {cite:ps}`zelevinsky_physics_2017`, which are generated using traditional Hartree-Fock {cite:ps}`anguiano_study_2014`.
- the Hartree-Fock-Bogoliubov (HFB) model generalises HF theory to incorporate the quasi-particle concepts of the BCS model. Importantly, it replaces the single particle-pair operators with generalised Bogoliubov quasi-particle operators of the form {math}`\sum_\mu \hat{a}_\mu^\dagger u_{\mu\nu} + \hat{a}_\mu v_{\mu\nu}` {cite:ps}`rowe_fundamentals_2010`.

+++

#### Excited States
Meanwhile, _excited_ states are primarily modelled in the HF approximation as 1p1h excitations. Experimentally, however, it is clear that for many nuclei these single 1p1h excitations are themselves insufficient to describe low-lying excited states. An example is {math}`{}^{16}\text{O}`, for which the lowest energy excitations predicted by the harmonic oscillator approximation should be seen at around 11.5 MeV (the difference between the 1p and 2s-1d shells). The spectrum of {math}`{}^{16}\text{O}`, however, has a {math}`J^\pi = 3^-` state at 6.13 MeV, indicating additional _coherent_ excitation mechanisms {cite:ps}`ring_nuclear_2004`. The observation of these excitation modes directly underpins the use of collective models to describe the nucleus. These collective models usually ignore the single-particle degrees of freedom in favour of collective vibrational or rotational modes.

[^ignore-pairing]: Experimentally, it is found that the ground state of spherical nuclei is not degenerate with respect to angular momentum as would be expected for a purely single-particle model. It follows that the residual interaction lowers the zero angular momentum state with respect to the other configurations {cite:ps}`greiner_nuclear_1996`.

+++

In addition to collective models, there are microscopic treatments of collective excitations. The most fundamental of these is the Tamm-Dancoff Approximation (TDA), which treats excited states of the nucleus as a superposition of 1p1h excitations of the ground state. These excitations are introduced by a creation operator {cite:ps}`greiner_nuclear_1996`:
:::{math}
\hat{Q}^\dagger_\nu = 
\sum_{mi}
    c_{mi}^\nu\hat{a}_m^\dagger\hat{a}_i
\,,
:::
and a correlational potential that acts in the excited particle-hole space. It can be shown that such an ansatz admits collective behaviour through a _coherent_ excitation of single particles {cite:ps}`greiner_nuclear_1996`. Typically these solutions are  obtained in a restricted model space comprising of several levels above and below the Fermi level {cite:ps}`ring_nuclear_2004`. 
% NOTE - the TDA introduces the residual interaction into the 1p1h excited space- NOT the GS, so there won't be any 1p1h admixtures in the GS. 
A limitation of the TDA, besides treating only 1p1h excitations, is the use of the unmodified HF ground state; the TDA assumption is that only excited states may have particle-hole excitations above the ground state {cite:ps}`fetter_quantum_1972`. The Random-Phase Approximation (RPA) extends the particle-hole creation operator to 
:::{math}
\hat{Q}^\dagger_\nu = 
\sum_{mi}
    x_{mi}^\nu\hat{a}_m^\dagger\hat{a}_i +
    y_{mi}^\nu\hat{a}_i^\dagger\hat{a}_m
\,,
:::
where {math}`\left\{y_{mi}\right\}` account for the account for the correlations in the _ground_ state.

% Coherent means same energy here I believe.
% TODO: what are the subscripts on these operators - \overline{\nu} is the time reversed state of \nu, but where did we introduce this? FONM does in p.517?

+++

### Shell Model

Having established the fundamental principles of microscopic models with Hartree-Fock theory, the nature of the shell model becomes fairly trivial to describe. Yet Hartree-Fock theory, though formally solvable, is computationally expensive and requires that the mean field be computed for each nucleus of interest. A simplified approach, the Shell Model, is found by determining the self-consistent field _empirically_, rather than from the two-body nucleon-nucleon interaction. The shell model potential should reconstruct the well-established shell-structure (magic numbers) of nuclear structure. The simplest model of the nucleus, that of the harmonic oscillator, does not on its own reconstruct these magic numbers. Instead, a _central potential_ that lies between the HO potential and a square well, is combined with a spin-orbit interaction to reproduce the experimental values (see {numref}`shell-model-potential` and {eq}`shell-model-potential`). This {math}`l^2` term accounts for the screening effect of the "finite" range of the strong nuclear force, and flattens the radial shape of the potential. The Wood-Saxon potential produces a similar shape to this modified potential. The spin-orbit term, meanwhile, is primarily a surface term which equates to a dependence of the nuclear potential upon the total-spin of the nucleon {cite:ps}`casten_nuclear_1990`. 
The properties of the single-particle states upon which the shell model is based are determined experimentally through pick-up and stripping reactions, which determine the binding energy and angular momentum of particles near the Fermi surface {cite:ps}`greiner_nuclear_1996`.

:::{math}
:label: shell-model-potential
u(\vb(r)) = V(\vb{r}) + f(\vb{r})\vb{l}\cdot\vb{s}\,.
:::

+++

:::{figure} image/shell-model.png
:name: shell-model-potential
:width: 512px
:align: center

Single-particle energies for (a) a simple harmonic oscillator (SHO); (b) a SHO with an {math}`l^2` term; (c\) a shell-model potential with {math}`l^2` and {math}`\vb{l}\cdot{\vb{s}}` terms. 
Figure by Morten Hjorth-Jensen, distributed under a [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.
:::

+++

For closed-shell nuclei, the shell model is simply an approximation to Hartree-Fock theory. An IPM Hamiltonian is chosen such that the low-energy eigenstates have the observed properties of the associated physical states, such as the nuclear density distributions, or angular momenta. The zeroeth order approximation yields the IPM itself, which describes closed-shell nuclei {cite:ps}`rowe_nuclear_2010`. Thereafter, an improved approximation for open-shell nuclei is found by diagonalising a total Hamiltonian (such as {eq}`hamiltonian-2q-mean-field`) in the restricted space spanned by the lowest-energy solutions of the IPM. These solutions correspond to placing valence nucleons in the unoccupied levels of the closed-shell core {cite:ps}`rowe_fundamentals_2010`. Further *second approximation*s include the independent-pair approximation, which accounts for the pairing contributions to the residual interaction.

In general, the shell model simplifies the many-body problem into a few-body problem by eliminating the core; considering only the exclusion principle and the potential well that the nucleons within the core generate. This approach is limited by the size of the model space required to perform a shell model calculation. In general, successful shell model calculations must select an appropriate subspace that is tailored to modeling the dynamics of interest to the calculation {cite:ps}`rowe_fundamentals_2010`. {cite:ts}`rowe_fundamentals_2010` describe the most significant role of the shell model as providing the
> language and concepts for the interpretation of observed phenomena, to gain understanding of the circumstances in which particular phenomena arise, and to extrapolate into other mass regions to see if the interpretations are consistent.

+++

#### Deformed Shell Model

+++

As discussed in {numref}`nuclear-models:rotor-model`, nuclear states away from closed shells show evidence of strong quadrupole deformation through their electric quadrupole moments. Given the success of the shell model in describing (near) closed-shell nuclei, it is reasonable to ask whether it might be extended to this deformed regime. One such model is the Nilsson model, considered one of the most successful nuclear models ever developed {cite:ps}`rowe_fundamentals_2010`. As with the rotor model, the adiabatic approximation is used to decouple the (deformed) core from the motion of the core; this model diminishes in effectiveness at high angular momenta.

+++

:::{figure} image/nilsson-model.svg
:name: nilsson-model
:width: 256px
:align: center

Illustration of two nucleon orbits around a deformed core. {math}`K_1` depicts an orbit that lies closer to the bulk of the nucleus than {math}`K_2`, and therefore lies at lower energy.
Adapted from Ref. {cite:ps}`casten_nuclear_1990`.
:::

+++

The distinguishing feature of the Nilsson model with respect to the spherical shell model is an orientation of nucleon states with respect to the core. This is illustrated in {numref}`nilsson-model`, which depicts two nucleon orbits {math}`K_1` and {math}`K_2`. As illustrated for the rotor model in {numref}`rotor-frame`, the value {math}`K` corresponds to the projection of the the intrinsic angular momentum (in this case, the single-particle momentum) onto the symmetry axis of the core. 

Given the success of the SHO in the description of the single-particle basis of the spherical shell model, the spheroidal anisotropic (deformed) harmonic oscillator is well-motivated to establish these states in the deformed system. Unlike the _spherical_ oscillator, in which there is a singular frequency {math}`\omega` that determines the per-quanta energy in each axis, the anisotropic harmonic oscillator distinguishes the frequency by axis. In the event of an axially-symmetric rotor, there are two distinct frequencies. Given that solutions to deformed oscillator should map onto the spherical oscillator in the deformation-free limit, the anisotropic frequencies must preserve the nuclear volume: {math}`\omega_3\omega_perp^2 = \omega_0^3`, where {math}`\omega_0` is the spherical oscillator frequency. This yields the following relations
:::{math}
\omega_\perp &= \omega_0\exp(\frac{\epsilon}{3})

\omega_3 &= \omega_0\exp(\frac{-2\epsilon}{3})\,.
:::
where {math}`\hat{3}` is the symmetry axis, and {math}`\epsilon` is the deformation parameter, with {math}`\epsilon > 0` for prolate deformation {cite:ps}`rowe_fundamentals_2010`. Under this deformed potential, the total angular momentum {math}`j` is no longer a good quantum number; only the symmetry-axis projection remains invariant whilst the orthogonal components are partitioned between the nucleons and the core {cite:ps}`rowe_fundamentals_2010`. It follows that states of a given projection are two-fold degenerate as the Hamiltonian depends only upon the magnitude of the {math}`\hat{3}` projection.

The principle behind the shell model is that eigenstates of the single-particle Hamiltonian are well-separated into distinct bands. In the spherical harmonic oscillator, these are directly influenced by increments in the oscillator quanta as well as the spin-orbit interaction splitting. The deformed harmonic oscillator also produces shell-structure, with maximal degeneracy (corresponding to strongly-defined shell structure) appearing at integer ratios of the two oscillator frequencies {cite:ps}`bohr_nuclear_1977`. Through an application of group theory, it can be shown that the shell closures at integer deformation ratios correpond to the decomposition of the deformed oscillator into multiple spherical potentials {cite:ps}`nazarewicz_dynamical_1992`. These findings have implications for understanding alpha-conjugate nuclei, nuclei which may be decomposed into a set of alpha particles, and the phenomenon of alpha clustering.
% Link to cluster model?

+++

#### No-core Shell Model

The no-core shell model (NCSM) description of the nucleus is an _ab-initio_ approach to determine the behaviour of the nucleus from two-body and three-body realistic interaction potentials. No further detail beyond the high-level principles of the model will be described here, but an overview is given to contextualize the landscape of microscopic models. The term _realistic_ follows from the choice of nucleon-nucleon potential that fit experimental phase shifts up to a particular energy, and nucleon-nucleon-nucleon interactions that include terms corresponding to two-pion exchanges {cite:ps}`barrett_ab_2013`. 

In the domain of nuclear physics, "ab-initio" assumes a large number of distinct meanings. In the context of the NCSM, the term is a description of a system in which all {math}`A` nucleons are active members of the model space, and their collective behaviour is determined from the introduction of effective interactions. Clearly, a model that operates at the level of protons and neutrons is not concerned with the subnucleonic degrees of freedom that the term "ab-initio" might invoke.

The NCSM is somewhat paradoxically named; as aforementioned, the shell model is usually built upon a mean-field potential, which is notably absent in the NCSM. Rather, the harmonic-oscillator basis, truncated to a maximum total system energy, is used to define the single-particle states through _natural orbitals_ {cite:ps}`constantinou_natural_2017`. The resulting system, using second quantisation representation, is then amenable to treatment with techniques developed for shell model calculations, which justifies the _shell model_ description.

+++

### Anti-symmetrised Molecular Dynamics

Anti-symmetrised Molecular Dynamics (AMD) attempts to model the coexistence of cluster and mean-fields phenomena within the nucleus. Like the HF methods, AMD employs a basis of Slater determinants. Instead of single-particle eigenfunctions, however, AMD uses a basis of Gaussian wave packets:
:::{math}
\ket{\phi_\text{AMD}(Z)} = \hat{\mathcal{A}}\Bqty{\ket{\psi_1} \otimes \ket{\psi_1} \otimes \dots \otimes \ket{\psi_N}}\,,
:::
where {math}`\ket{\psi_i}` is the direct product state of the spatial ({math}`\phi`), intrinsic spin ({math}`\chi`), and isospin ({math}`\tau`) states of nucleus {math}`i`:
:::{math}
\ket{\psi_i} &= \ket{\phi_{\vb{Z}_i}}\otimes\ket{\chi_i}\ket{\tau_i}

\braket{\phi_{\vb{Z}_i}} &\propto \exp(-\nu\pqty{\vb{r}_j - \frac{\vb{Z}_i}{\sqrt{\nu}}}^2)

\ket{\chi_i} &= \left(\frac{1}{2}+\xi_i\right) \ket{\chi_{\uparrow}}+\left(\frac{1}{2}-\xi_i\right) \ket{\chi_{\downarrow}}\,.
:::

+++

It follows that an AMD many-body basis state can be represented by a set of variational parameters, {math}`\mathcal{Z} = \left\{\nu, \vb{Z}_1,\vb{Z}_2,\dots,\vb{Z}_N,\xi_1,\xi_2,\dots\xi_N\right\}`, where the width parameter {math}`\nu` is optimised for a given system, and {math}`\vb{z}_i = \pmqty{\vb{x} & \vb{y} & \vb{z} & \sigma}` describes the centre, momenta, and width of each localised Gaussian {cite:ps}`beck_clusters_2010`. In the limit that the Gaussian centres converge upon a particular location, then the AMD wave-function becomes equivalent to the harmonic oscillator shell-model wave-function  (see {numref}`amd-like-shell-model`) {cite:ps}`kanada-enyo_antisymmetrized_2012`. 

:::{figure} image/placeholder/amd-antisymmetrisation-shell-model.png
:name: amd-like-shell-model
:align: center

Schematic representation of the eigenstates resulting from anti-symmetrisation of Gaussian wave-packets in the limit of {math}`\frac{d}{\sqrt{a}} \rightarrow 0`, where {math}`d = 0.75 \sqrt { a }` is the displacement between each wave-packet, and {math}`a` the real width parameter. Figure taken from Ref. {cite:ps}`feldmeier_fermionic_1997`.
:::

#### Energy minimisation

:::{note}
:class: margin

At the surface level, the HF and AMD methods bare a striking resemblence. The fundamental difference between the two, besides the ansatz of a single-particle Gaussian representation (the basis of the AMD wavefunction), is the supposition of a mean-field. The HF equations are solved iteratively to determine the self-consistent solution. The single-particle eigenfunctions are typically expanded in a complete basis, e.g. harmonic oscillator eigenfunctions, or solved numerically. Meanwhile, the AMD method optimises _parameters_ for a fixed model (Gaussian wave-packets), following the gradient of the Hamiltonian. the "variation" in the time-independent HF method corresponds to single 1p1h excitation of the trial state, whereas for AMD, variation is introduced through the total derivative of the wavefunction.
:::

To determine the optimum values for {math}`\mathcal{Z}`, the time-dependent variational principle (using the principle of least action ) {cite:ps}`kramer_time-dependent_1981`
:::{math}
:label: time-dependent-variational-principle
\delta\matrixel{\psi}{\hat{H}-\mathrm{i} \hbar \frac{\partial}{\partial t}}{\psi}=0
:::
is used to derive the equations of motion of the system {cite:ps}`feldmeier_fermionic_1997`:
:::{math}
:label: amd-equation-of-motion
i \hbar \dv{t} u_k = (\lambda+i \mu) 
    \pdv{u_k^*}  
        \frac{
            \expval{\hat{H}}{
                \phi^{\pm}
            }
         }
         {
            \ip{\phi^{\pm}}
        }\,,
:::
where the term {math}`(\lambda+i \mu)` is an _artificial_ viscous component designed to dissipate the energy of the system towards a minimum {cite:ps}`wilets_classical_1977` {cite:ps}`horiuchi_neutron-rich_1995`.

+++

In the language of second quantisation, the AMD Hamiltonian
:::{math}
:label: amd-hamiltonian
\hat{H} = 
\sum_{\alpha\beta}T_{\alpha \beta}\hat{a}^\dagger_\alpha\hat{a}_\beta + 
\frac{1}{2}
\sum_{\alpha\beta\gamma\delta}
    \pqty{
        V^{\mathcal{N}}_{\alpha\beta\gamma\delta} +
        V^{\mathcal{C}}_{\alpha\beta\gamma\delta}
     }\hat{a}^\dagger_\alpha\hat{a}^\dagger_\beta\hat{a}_\delta\hat{a}_\gamma
- \hat{T}_\text{CoM}
:::
is identical to {eq}`hamiltonian-2q` except for an additional two-body Coulomb interaction (usually ignored in the HFB procedure) {cite:ps}`anguiano_coulomb_2001`, and the removal of the centre-of-mass energy via the operator {math}`\hat{T}_\text{CoM}`. A range of effective nuclear potentials have been used for {math}`\hat{V}_\text{nuc}` including the Volkov, Gogny, or Skyme forces; whilst the Coulomb force is often approximated by a sum of (seven) Gaussians {cite}`kanada-enyo_antisymmetrized_2012`. The expectation of this Hamiltonian is then minimised with respect to the wave-function parametrisation {math}`\mathcal{Z}`
:::{math}
 \min _ { \mathcal{Z} } 
 \frac { 
     \expval{ \widehat { H } - \widehat { T } _ { \mathrm { cm } }}{ \phi _ { \mathrm { AMD } } }
 } { \ip{ \phi _ { \mathrm { AMD } } } } 
:::
to determine the lowest energy state {math}`\ket{\phi_{\mathrm{AMD}}}`.

+++ {"jp-MarkdownHeadingCollapsed": true}

#### Variation after Projection, Projection after Variation
States obtained by the variation procedure generally no longer demonstrate the symmetries of the Hamiltonian {eq}`amd-hamiltonian` with respect to parity and rotational invariance {cite:ps}`neff_nuclear_2008`. These symmetries can be restored through projection onto angular momentum and parity eigenstates:
:::{math}
:label: parity-angular-projections
\ket{ \phi_{ \mathrm { AMD } } ^ { \pm } } &\equiv P ^ { \pm } \ket{ \phi _ { \mathrm { AMD } } ( \mathcal{Z} ) } = \frac { 1 \pm \hat { P } _ { r } } { 2 } \ket{ \phi _ { \mathrm { AMD } } ( \mathcal{Z} ) }

\ket{ \phi _ { M K } ^ { J } } &\equiv P _ { M K } ^ { J } \ket{ \phi _ { \mathrm { AMD } } ( \mathcal{Z} ) } = \int d \Omega D _ { M K } ^ { J * } ( \Omega ) \hat { R } ( \Omega ) \ket{ \phi _ { \mathrm { AMD } } ( \mathcal{Z} ) }
\,,
:::
where {math}`D _ { M K } ^ { J } ( \Omega )` is the Wigner's {math}`D` function, and {math}`\hat{R}(\Omega)` is a rotation operator for some Euler angle {math}`\Omega` {cite:ps}`kanada-enyo_antisymmetrized_2012` {cite:ps}`rampho_antisymmetrized_2012`. 
       
Early AMD calculations were performed first by a method known as variation _before_ projection (VBP, or properly {math}`\text{VaP}^\pi \text{bP}^J`) {cite:ps}`horiuchi_neutron-rich_1995`. By deferring angular momentum projection until after variation, VBP is numerically the least inexpensive means of obtaining states of good angular momentum. Nevertheless, it is possible to minimise the energy of the _projected state_, i.e.
:::{math}
\min_{\mathcal{Z}}
\frac{
    \expval
        {{P_{MK}^{J\pm}}^\dagger\pqty{\widehat{H}-\widehat{T}_{\mathrm{cm}}}P_{MK}^{J\pm}}
        {\phi_{\mathrm{AMD}}}
}{
    \expval
        {{P_{MK}^{J\pm}}^\dagger{P_{MK}^{J\pm}}}
        {\phi_{\mathrm{AMD}}}
}
:::
for some state {math}` \ket{ \phi _ { M K } ^ { J } }`, a method known as variation _after_ projection (VAP, or properly {math}`\text{VaP}^\pi \text{aP}^J`) {cite:ps}`kanada-enyo_variation_1998`. Fundamentally, VAP approach necessitates a minimisation procedure for each eigenstate onto which the AMD state is projected. Although much more costly than VBP, the VAP procedure is necessary to describe states with intrinsic structures that differ from the mean-field state (see {numref}`amd-variation-comparison`) {cite:ps}`feldmeier_nuclear_2017`.  
    
:::{note}
:class: margin

In simpler terms, a sum of two Slater determinants is not itself guaranteed to be a Slater determinant, though it is antisymmetric. Therefore the set of anti-symmetric states is larger than the set of Slater determinants. The inability to represent a state as a Slater is equivalent to the statement that the individual nucleons are not behaving as independent particles.
:::
    
The single Slater-determinant AMD basis representation ensures that the solution to the many-body problem is restricted to a subset of the anti-symmetric Hilbert space, i.e. that given by the mean-field approximation of independent nucleons in single-particle eigenstates moving in an external potential. Complex correlational phenomena, corresponding to configuration mixing, requires a linear superposition of Slater determinants.  The admixtures of eigenstates yielded by the projection operators leads to the consideration of beyond mean-field phenomena during the variational procedure.
    
:::{figure} image/placeholder/amd-variation-comparison.png
:name: amd-variation-comparison
:align: center
:width: 300px

Density distributions of the AMD wavefunctions for {math}`{}^{9}\text{Li}` obtained by (a) variation _before_ parity and angular momentum projection, (b) _after_ parity and _before_ angular momentum projection, and (c) _after_ parity and angular momentum projection. It can be seen that only (c) exhibits beyond mean-field structure. The proton ({math}`\rho_p`), neutron ({math}`\rho_n`), and total ({math}`\rho_m`) densities of the AMD wave-function are illustrated. Figure adapted from Ref. {cite:ps}`beck_clusters_2010`.
:::

+++

(expt:models-excited-states)=
#### Excited States

% NOTE: greiner 226 (1p1h deform men field)
In the HF approximation, a set of low-lying excited states can be constructed from superpositions of 1p1h excitations of the ground state {math}`\ket{HF}`. This approximation is built upon the assumption that these excited states do not significantly deform the mean field, and that their correlations can be ignored {cite:ps}`greiner_nuclear_1996`. In the extreme case of the structures that emerge in excited states near the cluster-decay threshold, these assumptions are unfounded and the single-particle states must be recalculated in a self-consistent manner. 

Unlike HF, the AMD method does not readily admit a set of basis states from which to compose excited states. There are two favoured methods for determining such a basis; orthogonal VAP, and constrained variation. In orthogonal VAP, a set of basis functions is established through orthogonalisation to already-obtained lower states {math}` \phi _ { k } ^ { J \pm } ( \{ \mathcal{Z}_k \} )` for {math}`k=1,\dots,n-1`, thus building a set of intrinsic AMD states:

:::{math}
 \phi _ { n } ^ { J \pm } (  \mathcal{Z}  ) = P _ { M K } ^ { J \pm } \phi _ { \mathrm { AMD } } (  \mathcal{Z}  ) - 
    \sum _ { k = 1 } ^ { n - 1 } \frac {
        \bra{ \phi _ { k } ^ { J \pm } \left(  \mathcal{Z}  _ { k } ^ { J \pm } \right) }\ket{ P _ { M K } ^ { J \pm } \phi _ { \mathrm { AMD } } (  \mathcal{Z}  ) } 
    } { 
        \ip{ \phi _ { k } ^ { J \pm } \left(  \mathcal{Z}  _ { k } ^ { J \pm } \right) }
    } \phi _ { k } ^ { J \pm } \left(  \mathcal{Z}  _ { k } ^ { J \pm } \right) 
\,.
:::

The eigenstates of the AMD Hamiltonian are constructed from these _intrinsic_ states {math}`\qty{\ket{{\phi _ { \mathrm { AMD } }}( \mathcal{Z}_i )}}` by simultaneously diagonalising the Hamiltonian {math}`\matrixel{P _ { M K ^ { \prime } } ^ { J \pm } \phi _ { \mathrm { AMD } } ^ { i }}{H}{P _ { M K ^ { \prime \prime } } ^ { J \pm } \phi _ { \mathrm { AMD } } ^ { j }}` and normal {math}`\braket{P _ { M K ^ { \prime } } ^ { J \pm  } \phi _ { \mathrm { AMD } } ^ i  }{P _ { M K ^ { \prime \prime } } ^ { J \pm } \phi _ { \mathrm { AMD } } ^ { j }}` matrices formed from these states {cite:ps}`kanada-enyo_variation_1998`. It follows that these eigenstates are _superpositions_ of intrinsic states.


Meanwhile, constrained variation closely resembles the Generator Coordinate Method (GCM) used to include collective phenomena in many-body wave-functions {cite:ps}`wa_wong_generator-coordinate_1975`. First, a set of basis functions is established through the imposition of a deformation constraint on the VBP variation equation. This establishes a set of states with a given quadrupole deformation for which the energy is locally minimal. These states are then projected onto states of good angular momentum, and used as a basis for the many-body state. Like orthogonal VAP, the eigenstates of the AMD Hamiltonian are determined through simultaneous diagonalisation of the norm and Hamiltonian matrices {cite:ps}`beck_clusters_2010`.

:::{figure} image/placeholder/amd-variation-comparison-2.png
:name: amd-variation-comparison-2
:align: center
:width: 300px

Density distributions of a singular AMD wave-function for {math}`{}^{9}\text{Li}` obtained by variation _after_ parity and _before_ angular momentum projection for a deformation constraint of {math}`\beta=0.35`. The proton ({math}`\rho_p`), neutron ({math}`\rho_n`), and total ({math}`\rho_m`) densities of the AMD wave-function are illustrated. See {numref}`amd-variation-comparison` for comparison to other variational solutions. Figure adapted from Ref. {cite:ps}`beck_clusters_2010`.
:::

% HOW does this differ to HF? HF w.f. are intrinsically not localised to particles like AMD

Constrained solutions are particularly useful in obtaining basis states for loosely bound systems, e.g. those of cluster or halo nature; the solution given by VAP usually corresponds to a compact configuration {cite:ps}`feldmeier_nuclear_2017`.

+++

(expt:nuclear-molecules)=
### Nuclear Molecules

The pairing force, which anti-aligns the angular momenta of like-nucleons within the same orbital, is responsible for some of the most exciting phenomena in nuclear physics, e.g. the even-even energy gap between the ground state and lowest single-particle excitation, or the zero angular momentum of even-even ground state nuclei. It is most strikingly seen within the {math}`\alpha`-particle system, which is comprised to two correlated pairs of protons and neutrons. In combination with the small symmetry energy of the system, the pairing interaction is responsible for the significant binding energy (28 MeV), and first excited state (20 MeV). These two properties suggest that where an {math}`\alpha`-particle forms in the nucleus, it may remain stable for a considerable period of time {cite:ps}`freer_clustered_2007-2`. Meanwhile, the emission of {math}`\alpha`-particles from the nucleus implies that such particles might be preformed and exist prior to the decay. Although it is known that such an assumption is overly reductive, the existence of many alpha-clustered structures is postulated by the Ikeda threshold rule, which predicts the emergence of such structures near the alpha breakup threshold {cite:ps}`catford_clustering_2013-1`.

:::{figure} image/placeholder/types-of-nuclear-clustering.png
:name: types-of-nuclear-clustering
:align: center
:width: 400px

A myriad of clustering phenomena are seen in light nuclei, varying from small clusters outside of a closed shell to alpha condensates. Figure taken from Ref. {cite:ps}`catford_clustering_2013-1`.
:::

+++

A number of examples of "clustering" phenomena, including alpha condensates (e.g. {math}`{}^8\text{Be}`), can be seen in {numref}`types-of-nuclear-clustering`. In recent times, a focus has been placed on neutron-rich nuclei, where the existence of valence neutrons has been shown to stabilise the cluster structure and give rise to a class of nuclear molecular states {cite:ps}`von_oertzen_nuclear_2006`. In the case of {math}`{}^8\text{Be}`; the alpha condensate has a half-life of {math}`\sim 10^{-16}`s, whereas its sibling {math}`{}^9\text{Be}` is considered stable. This "Borromean"-like behaviour follows from the behaviour of the valence neutron, which may be thought of as occupying a delocalised orbit shared between separate alpha-particle clusters {cite:ps}`mcewan_characterization_2004`. The term "nuclear molecule" is well-chosen; in the case of the beryllium isotopes, the effective {math}`\alpha`-{math}`\alpha` potential has three modes: weakly attractive at intermediate distances; strongly repulsive at smaller distances, due to the exchange interaction; and moderately repulsive at larger distances, due to Coulomb repulsion {cite:ps}`von_oertzen_nuclear_2006`.  The nature of this interaction closely resembles the Van Der Waals molecular potential, giving rise to the term "nuclear molecule". In general, molecular structures are strongly predisposed to form chain-like states in order to minimise the Coulomb repuulsion between the constituents
% This hard-core, which naturally follows from Pauli blocking, requires one of the clusters to move into the next major shell.

+++

#### {math}`\pi` bonds & {math}`\sigma` bonds
The Hückel method, taken from molecular orbital (MO) theory, can be used to describe the molecular orbit occupied by a valence neutron as a superposition of the single-centre shell model states:
:::{math}
\ket{\psi_\pm} = \frac{1}{\sqrt{2}} \pqty{\ket{\psi_1} \pm \ket{\psi_2}}\,.
:::

% :::{figure} image/placeholder/huckel-diagram.png
% :align: center
% :name: huckel-diagram
% :width: 150px
% 
% Schematic diagram of the two-centre wave functions of molecular orbitals which form the basis states of {math}`{}^9Be`. Figure adapted % from {cite:ps}`beck_clusters_2014`.
% :::

:::{note}
:class: margin

It helps to consider the spatial distributions of the spherical harmonics, which form the basis of angular momentum wavefunctions. It is clear, for example, that the projection of {math}`L=1` onto the symmetry axis yields the solutions seen in {numref}`pi-sigma-bonds-9be`. The visualisation of the spherical harmonics is useful in connecting the molecular orbital picture with the familiar quantum representation.

:::

This yields two molecular orbitals, conventionally labelled _g_ ({math}`\ket{\psi_+}`) and _u_ ({math}`\ket{\psi_-}`). Each has both an total spin {math}`J` and an orbital angular momentum {math}`l`. The projection {math}`m_l` of {math}`l` admits two further families of orbitals; {math}`\sigma` orbits with {math}`m_l = 0`, and {math}`\pi` orbits with {math}`m_l = 1`. This labelling of the {math}`m_l` projections follows from Molecular Orbital theory. Of course, in a non-spherical system the total angular momentum {math}`J` is no longer a good quantum number, so the symmetry-axis projection {math}`K` is taken instead. The parity of these states is given by {math}`\pi=\pqty{-1}^lp` where {math}`p=1` for _g_ orbits, and {math}`p=-1` for _u_ orbits {cite:ps}`beck_clusters_2014`.

+++

The Hückel wave-function amplitudes for the various orbital configurations are shown in {numref}`pi-sigma-bonds-9be`.

:::{figure} image/placeholder/pi-sigma-bonds-9be.png
:align: center
:name: pi-sigma-bonds-9be
:width: 400px

One-dimensional molecular orbits for cluster states in {math}`{}^9\text{Be}`; showing (a) {math}`\sigma` bonding, (b) {math}`\sigma` anti-bonding, (c\) {math}`\pi` bonding, (d) {math}`\pi` anti-bonding. In this 2D projection, the deformation axis lies in parallel to the plane normal. Figure adapted from Ref. {cite:ps}`mcewan_characterization_2004`.
:::
It can be seen that the {math}`\pi` and {math}`\sigma` bonds in {numref}`pi-sigma-bonds-9be` bare close resemblence to their namesakes in atomic molecular orbitals, shown in {numref}`pi-sigma-bonds-atomic`.

:::{figure} image/placeholder/pi-sigma-bonds-atomic.png
:align: center
:name: pi-sigma-bonds-atomic
:width: 400px

One-dimensional molecular orbits from atomic physics; showing (a) {math}`\pi` bonding, (b) {math}`\pi` anti-bonding, (c\) {math}`\sigma` bonding, (d) {math}`\sigma` anti-bonding. Figure adapted from Ref. {cite:ps}`noauthor_35_2020`.
:::

The {math}`\pi` orbit is also known as the _ring orbit_, because it spreads perpendicular to the {math}`\alpha`-{math}`\alpha` axis, whilst the {math}`\sigma` orbit is called the _chain orbit_ it spreads parallel to the {math}`\alpha`-{math}`\alpha` axis (see {numref}`pi-sigma-bonds-schematic`) {cite:ps}`itagaki_molecular_2000`.

+++

:::{figure} image/placeholder/pi-sigma-bonds-schematic.png
:align: center
:name: pi-sigma-bonds-schematic
:width: 400px

Illustration of the spatial overlap of two {math}`p`-shell orbits, corresponding to (a) {math}`\pi` and (b) {math}`\sigma` molecular orbitals. Figure adapted from Ref. {cite:ps}`von_oertzen_nuclear_2006`. 
:::

+++

In {math}`{}^9\text{Be}`, molecular states comprise two clusters {math}`\alpha+\alpha+n\rightarrow {}^5\mathrm{He}+\alpha`, whereby molecular orbitals are constructed from the {math}`p_{3/2}` shell-model orbit of the valence neutron in {math}`{}^5\text{He}`. A two-centre model of the nucleus has been explored in {cite:ps}`scharnweber_asymptotically_1970`, and a neutron level scheme computed as a function of the centre separation (see {numref}`two-centre-correlations`). Though a formal model can be used to build this scheme {cite:ps}`seya_nuclear_1981`, significant insight can be derived from mapping the separate-centre shell-model states onto states in the Nilsson deformed harmonic oscillator. With known spin and parity, the Nilsson orbits can be used to label the two-centre solutions and define a set of molecular orbitals {cite:ps}`von_oertzen_nuclear_2002`. By correlating the states in {numref}`two-centre-correlations` with those in {numref}`nilsson-orbits`, one can identify the four molecular orbitals available to the {math}`1p3/2` neutron in {math}`{}^5\mathrm{He}`: the {math}`3 / 2^{-}`, {math}`1 / 2^{+}`, and {math}`1 / 2^{-}` states in {math}`{ }^9 \mathrm{Be}` correspond to the {math}`\left(\pi_{3 / 2^{-}}, \mathrm{g}\right)`, {math}`\left(\sigma_{1 / 2^{+}}, u\right)`, and {math}`\left(\pi_{1 / 2^{-}}, g\right)` orbitals {cite:ps}`von_oertzen_dimers_1997`. The complete set of low-lying states in {math}`{}^{9}\mathrm{Be}` are consistent with rotational bands built upon these basis {cite:ps}`von_oertzen_dimers_1997`.

:::{figure} image/two-center-correlations.png
:align: center
:name: two-centre-correlations
:width: 300px

Neutron level scheme of the two-centre shell-model as a function of the deformation eccentricity {math}`z_0`. The y-axis intercepts correspond to spherical shell-model states, whilst at large separations the spherical shell-model states of the fragments are indicated {cite:ps}`scharnweber_asymptotically_1970`. 
:::

:::{figure} image/nilsson-orbits.png
:align: center
:name: nilsson-orbits
:width: 300px

Single-particle level scheme of the Nilsson deformed harmonic oscillator potential, for {math}`N<50`. Solid lines indicate positive parity solutions, whilst dashed lines represent negative parity states. Each state is labelled by {math}`[N n_z \Lambda \Omega]`, where {math}`N` is the major oscillator number, {math}`n_z` is the oscillator quanta along the 3-axis, {math}`\Lambda` the z projection of the orbital angular momentum, and {math}`\Omega` the z projection of the total angular momentum {math}`J`. Figure taken from Ref. {cite:ps}`heyde_basic_2004`.
:::

+++

:::{note}
:class: margin

In simple terms, the requirement that physical states have good parity means that one must take a superposition of the asymmetric states. This leads to symmetric and antisymmetric solutions.
:::
The set of basis states established from this two-centre approach can be extended in the case of a three-center molecule, such as the carbon isotopes. This additional center primarily splits the basis states, and lowers the lowest state with respect to the three-body particle threshold {cite:ps}`milin_search_2002`. In addition, the formation of asymmetric structures may lead to the phenomenon of parity doublets (see {numref}`expt:parity-doublets`).

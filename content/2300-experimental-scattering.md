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

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}

import numpy as np
from matplotlib import pyplot as plt
from mplhep.styles import ROOT

plt.style.use(ROOT)
plt.rc("figure", figsize=(10, 5), dpi=120)
```

(content:thick-target-experiments)=
# Thick Target Experiments

+++

## Resonant Scattering

+++

Nuclear reactions may be classified with respect to two extremes modes; _compound_ reactions in which the reactants fuse into a highly excited compound nucleus, and _direct_ interactions that involve typically only the surface nucleons of the target (see {numref}`nuclear-reaction-extremes`). As these latter reactions transition directly between initial and final states, the entrance and exit channels are strongly correlated. Meanwhile, the decay channel of the liquid-drop formed by coalescence of the target and projectile is considered to be reasonably independent of the entrance channel {cite:ps}`bohr_neutron_1936`. Consequently, the reaction cross-section is typically modelled as two separable terms {cite:ps}`satchler_introduction_1990`. 

:::{figure} image/placeholder/nuclear-reaction-extremes.png
:align: center
:name: nuclear-reaction-extremes
:width: 350px

Semi-classical illustration of the limiting extremes to nuclear reactions: formation of a transitory compound nucleus, and direct reactions. Figure taken from {cite:ps}`satchler_introduction_1990`.
:::

+++

At low incident energies, the compound nucleus may exhibit discrete states, despite being unstable against particle emission. Although there is sufficient energy for ejection of one or more particles, this energy is typically partitioned among several nucleons. Decay of this compound state occurs only once the excitation energy localises itself sufficiently for particles to escape. It follows that the compound nucleus may demonstrate a lifetime much greater than the orbital period of a single nucleon ({math}`\sim 10^{-22}\,\mathrm{s}`) i.e. the duration of a direct interaction {cite:ps}`satchler_introduction_1990`. In the low-energy region at which resonances are found, there are usually only two decay modes available to the liquid drop; rejection of the incident particle (scattering), or {math}`\gamma`-emission {cite:ps}`krane_introductory_1987`. Given that a quasi-bound state is unstable, it possesses an imprecise energy; from the Mandelstam-Tamm uncertainty principle {cite:ps}`mandelstam_uncertainty_1991`
:::{math}
:label: energy-uncertainty
\Delta{H} \Delta{T} \geq \frac{\hbar}{2}\,,
:::
one might assume that the long lifetime {math}`\tau=\Delta{T}` of the quasi-bound compound state implies that the width of this distribution {math}`\Gamma=\Delta{H}` is smaller than 1 MeV. 
Where the energy of the entrance channel is sufficiently matched with that of the quasi-bound state, there will be a marked enhancement in the cross section of the reaction, a phenomenon known as a _resonance_. Typically this has the form of the Breit-Wigner distribution
:::{math}
:label: breit-wigner

\sigma_\text{res}(E) =\sigma_0 \frac{\frac{1}{4} \Gamma^2}{\left(E-E_{\mathrm{r}}\right)^2+\frac{1}{4} \Gamma^2}\,,
:::
where {math}`\Gamma` is the full-width at half-maximum (FWHM) of the resonance (see {numref}`resonance-shape`), {math}`E_r` the centroid of the distribution, and {math}`\sigma_0` the amplitude of the resonance {cite:ps}`satchler_introduction_1990`. These resonant states are only visible at sufficiently low energies; as the excitation energy increases, the separation between levels decreases until the density is such that individual states can no-longer be resolved and form a continuum of unbound states. It transpires that in practical terms the energy relation in {eq}`energy-uncertainty` is inapplicable to the Breit-Wigner curve, yet it can be shown that the lifetime of the state {math}`\tau` is related to its width by {eq}`breit-wigner-width` {cite:ps}`bransden_quantum_2000` {cite:ps}`uffink_rate_1993`.
:::{math}
:label: breit-wigner-width

\Gamma = \frac{\hbar}{\tau}\,.
:::

+++

Among the exit channels of the compound nucleus is an elastic channel, i.e. that which corresponds to the {math}`A(a,a)A` reaction. When the elastic scattering cross section is measured, however, it typically does not exhibit the predicted Breit-Wigner shape. In addition to forming a resonant quasi-bound state in the compound nucleus, the incident particle may simply scatter directly off the target. This leads to an additional shape-elastic potential contribution to the elastic scattering cross-section (see {numref}`resonance-shape`).

% Should this be a subfig?

:::{figure} image/placeholder/resonance-shape.png
:align: center
:name: resonance-shape
:width: 512px

Comparison between the (left) Breit-Wigner distribution and the (right) elastic scattering cross section. (b) includes interference between the shape-elastic and resonance-elastic interactions. Subfigures taken from {cite:ps}`satchler_introduction_1990`.
:::

+++

(content:conservation-rules)=
## Conservation Rules

As a closed physical system, the normal conservation rules still apply to a scattering reaction between two nuclei. The total energy of the system must therefore be conserved during the interaction. Assuming a resonance reaction of the form {math}`A(a,b)B`,
:::{math}
:label: reaction-energy-balance
T_A + m_Ac^2 + T_a + m_ac^2 = T_B + m_Bc^2 + T_b + m_bc^2\,\,
:::
where {math}`m_X` is the _rest mass_ of {math}`X`, which may be excited, and {math}`T_X` is the kinetic energy of {math}`X` in the current frame. With the following definition of the reaction Q-value with respect to the ground-state masses (e.g. {math}`m_X^\mathrm{gs}`) 
:::{math}
Q = \pqty{m_A^\mathrm{gs}+m_a^\mathrm{gs}-m_B^\mathrm{gs}-m_b^\mathrm{gs}}\,,
:::
{eq}`reaction-energy-balance` simplifies to
:::{math}
T_A + T_a + Q = T_B + T_b + E_\mathrm{ex} \,,
:::
where {math}`E_\mathrm{ex}` is the total excitation energy shared between {math}`B` and {math}`b`. For resonant reactions involving a compound nucleus {math}`X`, one must consider the intermediate state. If both the reactants and the products of the total reaction remain in their ground states, then 
:::{math}
T_A + T_a + Q = T_X + E_\mathrm{ex} = T_B + T_b\,,
:::
i.e. measurement of the reactant and product kinetic energies is sufficient to determine the excitation energy for a known {math}`Q`-value.

+++

% Is this frame dependent? (L) No - is a property of the frame, and most simply defined in the body-fixed frame of heavy nucleus
In addition to conservation of energy, the conservation of angular momentum must also be considered. For {math}`J=0` reactants, the angular momentum of the compound nucleus is entirely determined by the orbital angular momentum of the beam
:::{math}
\vb{\hat{J}_X} &= \vb{\hat{J}_A} + \vb{\hat{J}_a}

\vb{\hat{J}_X} &= \vb{\hat{L}_A} + \vb{\hat{I}_A} +  \vb{\hat{L}_a} + \vb{\hat{I}_a}

\vb{\hat{J}_X} &= \vb{\hat{L}_a}\,,
:::
where {math}`\vb{\hat{J}_X}` is the total angular momentum of {math}`X`, the compound nucleus; {math}`\vb{\hat{I}_X}` the intrinsic spin angular momentum of {math}`X`; {math}`A`, the target; and {math}`a`, the beam.
The vector {math}`\vb{\hat{J}_X}` is _by definition_ perpendicular to the momentum vector of the beam, in the event of a two-body scatter. In combination with conservation of parity, the conservation of angular momentum implies that one can only populate either natural-parity ({math}`\Pi=(-1)^l`) or unnatural parity ({math}`\Pi=(-1)^{l+1}`) states for spin-0 reactants. The same holds for the subsequent decay of the resonant states; if the products are both spin-0, then the orbital angular momentum of the products is defined entirely by the parity of the populated state.

+++

(content:time-projection-chambers)=
## Time-Projection Chambers

A time-projection chamber (TPC) is a particle detector which employs the use of a time-sensitive anode to perform three-dimensional reconstruction of particle trajectories. The original design for the TPC was developed at Lawrence Berkeley Laboratory {cite:ps}`marx_time_1978`, and has since seen multiple variations that improve the spatial resolution and gain. At the heart of the TPC is the time-sensitive anode, upon which a current is induced due to the drift of charges liberated by ionising radiation incident upon the active volume (see {numref}`gridded-ion-chamber`). Conventionally, time-projection chambers use gas mixtures such as P10 (90% Argon, 10% Methane) as the interaction medium; gas targets may easily be pressurised to tune the density according to the energies and families of particles that are likely to be observed.
In order to produce signals which can be discriminated against the electronic noise of the acquisition system, gas multiplication is typically employed.

+++

:::{figure} image/ion-chamber.svg
:align: center
:name: gridded-ion-chamber
:width: 300px

Operational principle of a gridded ion-chamber, in which charged particles ionise the gas to liberate electron-ion charge carriers that move under an applied field. The movement of charge carriers induces a charge upon the anode and cathode. The grid serves to remove the positional dependence of the signal amplitude when operated in electron-sensitive mode; only the electron component contributes to the measured voltage across the resistor {math}`R` once the electrons enter into the grid-anode region.
:::

+++

### Gas Ionisiation

+++

A charged particle moving through a gas medium loses energy by both excitation and ionisation of the target, to a similar extent. Each ionising collision is a stochastic process, obeying Poissonian statistics:
:::{math}
P(n) = \pqty{\frac{\pqty{{s}/{\lambda}}^n}{n!}}\exp({-s}/{\lambda})\,,
:::
where {math}`s` is the length of a given segment, {math}`\lambda=\frac{1}{N_e\sigma_i}` is the mean separation between clusters, {math}`N_e` is the electron number density of the gas, and {math}`\sigma_i` the ionisation cross-section of an electron {cite:ps}`hilke_time_2010`. The probability that zero clusters are formed in an interval is {math}`\exp\!\pqty{\frac{-s}{\lambda}}`, which tends to zero as {math}`\lambda \rightarrow 0`. Thus, clusters tend to form quite close together along a given track. Whilst most of these clusters consist of single ions liberated by the charged particle, a small proportion of collisions induce secondary ionisation whereby the liberated electron ionises additional molecules. In some cases, these electrons travel sufficient distance from the primary ionisation that they leave detectable ionisation trails, and are referred to as {math}`\delta`-electrons. 
It is observed that clusters with greater than a single electron tend to contain a significant number, contributing strongly to the mean number of electrons per unit path length. Between the Poisson counting statistics and distribution of the cluster size, the spatial resolution of a drift-chamber is limited by the properties of the gas.

+++

The mean energy-loss of an ion moving through a material is given by the Bethe-Bloch formula {cite:ps}`cockcroft_experimental_1955`, which relates several material properties
:::{math}
:label: bethe-bloch-formula

 -\expval{ \dv{E}{x} } = {
     \frac {4\pi }{m_{e}c^{2}}}
     \cdot {\frac {nz^{2}}{\beta ^{2}}}
     \cdot \pqty{{\frac {e^{2}}{4\pi \varepsilon _{0}}}}^{2}
     \cdot \bqty{ \ln \pqty{{\frac {2m_{e}c^{2}\beta ^{2}}{I\cdot (1-\beta ^{2})}}}-\beta ^{2}
 }\,,
:::
where {math}`c` is the speed of light, {math}`\varepsilon_0` the vacuum permittivity, {math}`I` the mean excitation potential of the material, {math}`z` the proton number of the ion, {math}`E` the energy of the ion, {math}`\beta=\frac{v}{c}, m_e` the electronic rest mass, {math}`e` the elementary charge, and {math}`n` the electron number density of the material. In the non-relativistic limit, this simplifies to 
:::{math}
:label: bethe-bloch-formula-non-rel

-\expval{ \dv{E}{x} } = {\frac {4\pi nz^{2}}{m_{e}v^{2}}} \cdot \pqty{{\frac {e^{2}}{4\pi \varepsilon _{0}}}}^{2}\cdot \bqty{\ln \pqty{{\frac {2m_{e}v^{2}}{I}}}}.
:::

+++

### Charge Multiplication

+++

The applied field between the anode and cathode serves to accelerate the liberated charge carriers within the detector. Due to collisions with gas atoms, the drift velocity of each charge carrier approaches a constant proportional to {math}`\frac{E}{P}`, where {math}`E` is the applied field; and {math}`P` the gas pressure {cite:ps}`recine_understanding_2014-1`. The utility of a gas chamber for energy measurement lies in a proportional response between the measured current/voltage and the energy deposited within the detector. Below a threshold field strength, recombination of the liberated ion pairs contributes to non-linearity and defines the _ion-saturation_ region of the pulse-amplitude applied-field curve. At higher field strengths, exceeding a threshold field value {math}`E_\mathrm{av}`, free electrons drifting under {math}`E` gain sufficient kinetic energy between collisions with the gas molecules to cause secondary ionisations. This demarcates the start of a proportional response mode. In typical gases at atmospheric pressure, the secondary ionisation potential tends to exceed the order of {math}`10^6` V/m. The first Townsend coefficient, {math}`\alpha`, of the gas determines the fractional increase in the number of electrons per unit path length
:::{math}
\dv{n}{x} = \alpha \dd{x}\,.
:::
It follows that for spatially invariant fields, the number density of electrons is given by {math}`n(x) = n(0)\exp\!\pqty{\alpha x}`. Thus, increasing the voltage above {math}`E_\mathrm{av}` leads to an increased gain that facilitates measurements of clusters that are seeded by only a few primary electrons.
Increasing the applied field further leads to the onset of non-proportionality, in which the build-up of slow-moving positive ions is sufficient to deform the electric field within the detector. Quickly thereafter begins the Geiger-Mueller region of operation, in which the space-charge effect is sufficiently strong that the multiplication process is self-limiting, and the pulse amplitude from the detector is independent of the properties of the incident radiation (see {numref}`gas-detector-region-operation`).

:::{figure} image/placeholder/gas-detector-region-operation.png
:align: center
:name: gas-detector-region-operation
:width: 400px

The different operation regions of gas-filled detectors, according to the applied electric field. Only a limited range of field strengths corresponds to a proportional regime in the detector response. Figure taken from {cite:ps}`knoll_radiation_1989`.
:::

Frequently, noble gases such as argon or helium are used as the primary gas, as they have small electronegativities that prevent ionised electrons being absorbed by the fill gas. However, alone these gases are susceptible to low breakdown-voltages in which the proportional region is lost, and typically have poor gain characteristics. Addition of a second component with a smaller ionisation energy than the fill gas leads to the Penning effect, in which the number of ion pairs produced per unit energy is enhanced {cite:ps}`sahin_penning_2010`. Furthermore, additive gasses can be used to suppress the breakdown phenomenon; primary gas atoms excited by secondary electrons may de-excite through the emission of UV photons. These photons can seed additional avalanches within the active volume, leading to saturation. By adding a _quench_ gas with additional degrees of freedom and a large UV photo-absorption cross section, e.g. diatomic hydrocarbons with rotational and vibrational modes, the UV photons emitted by secondary excitation can be absorbed without subsequent re-emission {cite:ps}`cortesi_recent_2018`. Finally, with a large enough field, the dielectric properties of a gas detector can break down. Admixtures that contain quench gases can also increase the value of the field required to induce this phenomenon {cite:ps}`suzuki_prototype_2012-1`.

+++

## Thick-Target Inverse Kinematics

Nuclear reactions are typically performed in one of two configurations. In thin-target experiments, a beam of known energy is trained upon a target whose geometry is sufficiently thin that the majority of interactions occur at a similar beam energy. Thick-target experiments dispense with this constraint; the thickness of the target is employed as a degree of freedom. Whilst thin-target experiments pose a much reduced analysis challenge, to perform a measurement that spans a range of energies requires varying the energy of the beam, a slow process that is both costly in time and limited in the number of "stops" (energies) that can be observed. Meanwhile, thick-target experiments circumvent this restriction by using the target itself as both the reaction domain and energy loss medium. 
In this configuration, the energy of each interaction is given as a function of the interaction location, i.e. the distance travelled within the target by the projectile.

+++

In a system consisting of two different-mass nuclei, thick-target resonant scattering can be performed either in forward kinematics, or in _inverse_ kinematics. In forward kinematics, the beam consists of the lighter nucleus, whilst the heavier nucleus serves as the target. In _inverse kinematics_, the reverse is true: the heavier ion serves as the beam, which is used to bombard a target consisting of the lighter isotope. This approach provides several advantages over forward kinematics: 
- From the conservation of momentum, two-body reactions are forward focussed (see {numref}`inverse-forward-kinematics`), which improves the geometrical efficiency of the forward-angle detector for a particular solid-angle coverage. 
- For short-lived isotopes, it is possible to use a particle accelerator to produce ions on-line to circumvent challenges of radioactive target production. This is particular feasible for alpha-scattering experiments; {math}`{}^4\mathrm{He}` is one of the lightest nuclei in existence, and therefore most nuclei of interest have larger masses.


::::{subfigure} AB
:layout-sm: A|B
:gap: 8px
:subcaptions: below
:name: inverse-forward-kinematics

:::{image} image/forward-kinematics.svg

:::

:::{image} image/inverse-kinematics.svg
:::

Schematic illustration of a non-relativistic elastic scattering reaction (lab frame) in (a) forward kinematics, in which the lighter nucleus _a_ is used as the projectile; and (b) inverse kinematics, whereby the heavy nucleus _A_ impinges upon the light target. 
In each panel, the upper region indicates a potential post-scattering configuration. In the inverse regime, due to conservation of momentum and energy, the reaction is _forward projected_; both nuclei continue travelling forward in the lab frame. Meanwhile, in forward kinematics it is possible for the beam to achieve a (smaller) negative velocity in the lab frame.
::::

+++

Given the clear {math}`z` dependence of {eq}`bethe-bloch-formula-non-rel` (see {numref}`stopping-power-10c-4he`), it is evident that thick-target inverse-kinematics configurations are particularly useful in isolating the heavy beam ions from the light target ions; the target dimensions can be configured such that the heavy ions are quickly arrested within the detector volume. From the {math}`\frac{\ln(\frac{E}{I})}{E}` terms, the stopping power acquires a maximum as a function of energy just prior to the particle coming to rest. When plotted as a function of the path length, the observed peak in the stopping power distribution is often called the Bragg-peak.
The thickness of the target additionally enhances the luminosity; unlike thin-target reactions in which a significant proportion of events will not interact with the target, thick-target reactions span a much wider portion of the reaction cross-section energy domain. In the event that the beam fully stops within the target, the efficiency of the experiment is limited only by secondary interactions, and the efficiency of the detectors.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Stopping power of {math}`{}^{10}\mathrm{C}` and {math}`{}^{4}\mathrm{He}`
      ions in a gas-mixture of 96% {math}`{}^4\mathrm{He}`, 4% {math}`\mathrm{CO}_2`
      at 405 atm, simulated using SRIM {cite:ps}`ziegler_srim_2010`.
    name: stopping-power-10c-4he
  image:
    align: center
    width: 512px
tags: [hide-input]
---
_, dE_dx1, E1 = np.loadtxt("data/10C-in-4He-CO2.csv", delimiter=",", unpack=True)
_, dE_dx2, E2 = np.loadtxt("data/4He-in-4He-CO2.csv", delimiter=",", unpack=True)

plt.figure()
plt.xlabel("Ion Energy /MeV")
plt.ylabel("dE/dx /MeV/cm")
plt.plot(E1, dE_dx1, label="${}^{10}\\mathrm{C}$")
plt.plot(E2, dE_dx2, label="${}^{4}\\mathrm{He}$")
plt.yscale("log")
plt.legend();
```

+++ {"tags": ["no-latex"]}

Unlike thin-target kinematics, reactions that take place within a gas chamber are not confined to a localised region.  Therefore, the experimental advantages of operating in a thick-target inverse-kinematic regime can only realised if there are suitable detectors (see {ref}`content:the-texat-detector`) and analysis techniques (see {ref}`content:track-finding-and-fitting`) available to recover the reaction kinematics. 
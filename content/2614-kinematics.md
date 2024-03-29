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
mystnb:
  execution_mode: inline
---

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}

import pickle

import numpy as np
import particle
from matplotlib import pyplot as plt
from mplhep.styles import ATLAS
from particle import Particle
from texat.detector.micromegas import PAD_HEIGHT
from texat.units import units as u

plt.style.use(ATLAS)
plt.rc("figure", figsize=(10, 5), dpi=120)

u.separate_format_defaults = True
```

(expt:kinematics)=
# Kinematics

+++

(expt:angular-scattering)=
## Angular Scattering

+++

Fundamentally, in the sub-relativistic regime, the following conservation laws typically form the basis of any kinematic reconstruction of an elastic interaction
:::{math}
:label: non-relativistic-kinematics

\sum_j \vb{p^{j}_i} &= \sum_j \vb{p^{j}_f}

\sum_j E^{j}_i &= \sum_j E^{j}_f\,.
:::

+++

In the context of a scattering reaction between an incident heavy (larger A, Z) ion and a stationary light (smaller A, Z) target (gas), the reaction will be forward projected and the range of the scattered light ion will be significantly greater than that of the recoiling heavy ion. As such, the tracks left by light ions moving through the TPC are much more easily identified, and may be fit with greater precision than fits performed using the heavy recoil.

+++

Given the energy and angular straggling of the beam following interactions with the window, it is also evident that indirect measurements of the beam energy will be less accurate than those of the light ion after it interacts with the silicon detector array. As such, the most accurate measurements of the reaction kinematics are given by the track scattering angles and known energy of the light product. In such a configuration, the beam and recoil momentum vectors are initially unknown. We can define a beam-centric coordinate system (see {numref}`scattering-coordinate-system`) with the {math}`\hat{1}` vector given by the beam direction, the {math}`\hat{3}` vector given by the normalised cross product of the beam and scatter tracks, and the {math}`\hat{2}` vector taken to be perpendicular to {math}`\hat{1}` and {math}`\hat{3}`.

+++

:::{figure} image/scattering-coordinate-system.svg
:name: scattering-coordinate-system

Schematic diagram of a static-target scattering reaction in a beam-centric coordinate system. The {math}`\hat{1}` vector is given by the beam direction, the {math}`\hat{3}` vector given by the reaction plane normal, and the {math}`\hat{2}` vector taken to be perpendicular to {math}`\hat{1}` and {math}`\hat{3}`. Each particle {math}`\vb{p}_{i}` can be resolved along these canonical axis vectors. Each vector {math}`\vb{p}_{i}` indicates the momentum of the reaction participant {math}`i`, whose components {math}`\vb{p}_{i}^{(j)}` have been resolved along the beam-centric coordinate system vectors {math}`\hat{j}`.
:::

+++

From {eq}`non-relativistic-kinematics`, conservation of momentum can be applied separately to each axis such that we have
:::{math}
p_1 &= p_2^\pqty{1} + p_3^\pqty{1}

0 &= p_2^\pqty{2} + p_3^\pqty{2}\,.
:::
An application of energy conservation yields
:::{math}
\frac{
    p_1
^2}{2m_1} =
\frac{
    p_2
^2}{2m_2} +
\frac{
    p_3
^2}{2m_3} + 
E_\mathrm{ex}\,,
:::
where {math}`E_\mathrm{ex}` is the total excitation energy of particles 2 and 3. For elastic scattering, {math}`E_\mathrm{ex} = 0`. It can be shown that if {math}`m_1 = m_3`, the recoil momentum is uniquely determined by
:::{math}
:label: angular-kinematics-recoil
p_3^\pqty{1} &= \frac{\pqty{\pqty{p_2^\pqty{2}}^2 + \pqty{p_2^\pqty{1}}^2}\frac{m_1}{m_2} + \pqty{p_2^\pqty{2}}^2 - \pqty{p_2^\pqty{1}}^2}{2 p_2^\pqty{1} }\\
&= \frac{\pqty{p_2^\pqty{2}}^2\pqty{m_1+m_2} + \pqty{p_2^\pqty{1}}^2\pqty{m_1-m_2}}{2 p_2^\pqty{1} m_2 }\,,
:::
ultimately yielding an expression for the beam energy in terms of the reaction products.

::::{admonition} Derivation of {eq}`angular-kinematics-recoil`
:class: dropdown no-latex

:::{math}
\frac{\pqty{p_1}^2}{2m_1} &= \frac{\pqty{p_2}^2}{2m_2} + \frac{\pqty{p_3}^2}{2m_1}\\
p_1^\pqty{1} &= p_2^\pqty{1} + p_3^\pqty{1} \\
0 &= p_2^\pqty{2} + p_3^\pqty{2} \\
\frac{\left(p_2^\pqty{1} + p_3^\pqty{1}\right)^2}{2m_1} &= \frac{\pqty{p_2^\pqty{2}}^2 + \pqty{p_2^\pqty{1}}^2}{2m_2} + \frac{\pqty{p_3^\pqty{2}}^2 + \pqty{p_3^\pqty{1}}^2}{2m_1}\\
\frac{\left(p_2^\pqty{1} + p_3^\pqty{1}\right)^2}{2m_1} &= \frac{\pqty{p_2^\pqty{2}}^2 + \pqty{p_2^\pqty{1}}^2}{2m_2} + \frac{\pqty{p_2^\pqty{2}}^2 + \pqty{p_3^\pqty{1}}^2}{2m_1}\\
\frac{\pqty{p_2^\pqty{1}}^2 + 2p_2^\pqty{1}p_3^\pqty{1}}{2m_1} &= \frac{\pqty{p_2^\pqty{2}}^2 + \pqty{p_2^\pqty{1}}^2}{2m_2} + \frac{\pqty{p_2^\pqty{2}}^2}{2m_1}\\
{\pqty{p_2^\pqty{1}}^2 + 2p_2^\pqty{1}p_3^\pqty{1}} &= \left(\pqty{p_2^\pqty{2}}^2 + \pqty{p_2^\pqty{1}}^2\right)\frac{m_1}{m_2} + \pqty{p_2^\pqty{2}}^2\\
p_3^\pqty{1}&= \frac{\pqty{p_2^\pqty{2}}^2\pqty{m_1+m_2} + \pqty{p_2^\pqty{1}}^2\pqty{m_1-m_2}}{2 p_2^\pqty{1} m_2 }\,.
:::

::::

+++

{numref}`angular-energy-curve` shows a histogram of the observed silicon energy as a function of the reconstructed event vertex position. The vertex is computed from the tracks fit in {numref}`expt:texat-track-fitting`, using the closest point of approach between the beam and the light recoil tracks. In the event that one does not observe the beam track directly, an idealised track can be assumed in which the beam is aligned along the forward ({math}`+\hat{y}`) vector. For these tracks, the vertex of the interaction is given by taking the closest point of approach between the ideal beam track and the track of the observed light-recoil.

Two clear loci are visible, corresponding to the elastic (upper) and inelastic (lower) scattering channels; with a portion of the available centre-of-mass energy partitioned into formation of an excited state in the (heavy) scattered beam nucleus, there is less kinetic energy available to the products of inelastic scattering reactions.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A plot of the vertex position in non zero-degree scattering reactions
      as a function of energy measured in the silicon detectors. A clear locus of
      bins corresponding to elastic reactions can be observed, with a maximum near
      (-100, 7500).
    name: angular-energy-curve
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/angular-energy-vertex.pickle", "rb") as f:
    hist = pickle.load(f)

hist.plot();
```

This approach necessarily requires the knowledge of the interaction vertex (to identify the light particle energy) and the relative angle of the beam to the scattered ion track. If both of these cannot be determined, then there is insufficient knowledge of the system to find a solution. In the central detectors, in which the light product track is close to zero degrees, it is possible to leverage the assumption of a linear reaction in order to once-again determine the beam energy (see {numref}`expt:zero-degree-scattering`).

+++

(expt:zero-degree-scattering)=
## Zero-degree Scattering

+++

Unlike the method described in {numref}`expt:angular-scattering`, reactions in the zero-degree regime are unsuitable for reconstruction using track fit information; the resolution of the TexAT MicroMeGaS in the drift plane is too poor to appropriately identify the reaction vertex in the majority of these interactions. Reactions confined to the drift axis are more amenable to the track-fit method; the temporal resolution of the MicroMeGaS is superior to the anode spatial resolution, but only a subset of events are suitable for this kind of reconstruction. 


An alternative reconstruction approach leverages the approximation that angular information can be neglected in the extreme zero-degree (lab frame) scattering regime. Under this assumption, {eq}`angular-kinematics-recoil` simplifies to
:::{math}
p_3 = \frac{p_2\pqty{m_1 - m_2}}{2 m_2}\,.
:::
This in turn admits a relationship between the beam and scatter energies
:::{math}
:label: beam-energy-zero-degree
\frac{E_2}{E_1} = \frac{4 m_1 m_2}{\pqty{m_1+m_2}^2}\,.
:::


::::{admonition} Derivation of {eq}`beam-energy-zero-degree`
:class: dropdown no-latex

:::{math}
E_1 &= \frac{\pqty{p_3}^2}{2m_1} + \frac{\pqty{p_2}^2}{2m_2}

&= \frac{\pqty{p_2}^2 \pqty{\frac{m_1}{m_2}-1}^2}{4\cdot 2m_1} + \frac{\pqty{p_2}^2}{2m_2}

&= \frac{\pqty{p_2}^2}{2}\bqty{\frac{\pqty{\frac{m_1}{m_2}-1}^2}{4\cdot m_1}+\frac{1}{m_2}}

&= \frac{\pqty{p_2}^2}{2}\frac{\bqty{m_2\pqty{\frac{m_1}{m_2}-1}^2+4m_1}}{4m_1 m_2}

&= \frac{\pqty{p_2}^2}{2}\frac{\bqty{\pqty{m_2-m_1}^2+4m_1m_2}}{4m_1 m_2^2}

&= \frac{\pqty{p_2}^2}{2m_2}\frac{\pqty{m_2+m_1}^2}{4m_1 m_2}

&= E_2\frac{\pqty{m_2+m_1}^2}{4m_1 m_2}
:::

::::

In this regime, the reaction vertex (and hence kinematics) is given by the point at which a separate model of the beam energy, such as that described in {numref}`expt:beam-energy-estimation`, agrees with that given by {eq}`beam-energy-zero-degree`. Yet, it was observed that the beam energy as predicted by direct and indirect methods did not show strong agreement and thus choice of a particular method introduces significant error in the reconstructed kinematics. 

The infeasibility of using a directly-reconstructed beam-energy model to identify the reaction vertex derives from from the sensitivity of energy loss calculations upon the path-length and stopping-power model of beam ion. For high-Z ions and large path lengths, this uncertainty dominates all other measures of uncertainty (such as the resolution of the silicon detectors and appropriateness of the zero-degree assumption). 

An alternative reconstruction approach is to identify the vertex of the reaction using the position of the Bragg peak of the scattering projectile. Knowledge of the Bragg peak location provides a measure of the heavy-product energy at that position. The interaction vertex is then defined by the position at which the heavy-product energy given by {eq}`beam-energy-zero-degree` agrees with that which yields the Bragg peak at the observed location. Such an approach requires precise tabulation of the low-energy stopping powers for the projectile, unlike the methodology outlined in {numref}`expt:angular-scattering` which requires only the stopping powers of the light-product. Furthermore, and prohibiting the use of such a method in this analysis, it must be possible to identify the Bragg peak within the active volume. For these data, the kinematics given by simulated stopping powers (using both SRIM and MSTAR) do not admit the possibility of observing the Bragg peak of the scattered beam; for an elastic scattering reaction to have sufficient energy to be measurable by the silicon detectors, it is found that the heavy-product must stop before the start of the MicroMeGaS.

With {eq}`beam-energy-zero-degree`, the beam energy is uniquely determined for elastic scattering by the energy of the light ion at the reaction vertex. If the beam energy is approximately known, it is possible to identify the vertex at the intersection between the curves that describe the beam energy as reconstructed from the initial beam energy and the energy deposited in the silicon detectors. See {numref}`zero-degree-energy-curve` for a plot of the vertex position as a function of silicon energy as reconstructed by this method.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 'A plot of the expected vertex position in zero-degree scattering as
      a function of energy measured in the central silicon detectors. The two curves
      show the interaction vertex for (solid line) elastic and (dashed line) inelastic
      scatters that produces the corresponding silicon hit for a known beam energy
      given by {numref}`expt:beam-energy-estimation`. '
    name: zero-degree-energy-curve
  image:
    align: center
    width: 512px
tags: [hide-input]
---
energy_hit, y_sample = np.loadtxt(
    "data/zero-degree-energy-vertex-map.csv", delimiter=",", unpack=True
)
energy_hit_ex, y_sample_ex = np.loadtxt(
    "data/zero-degree-energy-vertex-map-inelastic.csv", delimiter=",", unpack=True
)


plt.plot(y_sample, energy_hit, color="white", label="0° curve")
plt.plot(
    y_sample_ex,
    energy_hit_ex,
    color="white",
    label="0° curve (first excitation)",
    linestyle="--",
)
plt.xlabel("Vertex Position /mm")
plt.ylabel("Silicon Energy /keV")
plt.axvline(-64 * PAD_HEIGHT, label="Start of MicroMeGaS", color="C2")
hist.plot()
plt.legend(labelcolor="white");
```

For _inelastic_ scatters, it is anticipated that the measured silicon energy be reduced with respect to the elastic curve for a given vertex position. This describes the loci below the elastic curve shown in {numref}`zero-degree-energy-curve`. By treating the excitation of the heavy product, it can be shown that {eq}`beam-energy-zero-degree` is the ground-state simplification of the following relation:
:::{math}
:label: beam-energy-zero-degree-excited
\frac{E_2}{E_1} = \frac{4 m_1 m_2}{\pqty{m_1\pqty{1+\frac{E^*}{E_2}}+m_2}^2}\,,
:::
where {math}`E^*` is the excitation energy of the scattered heavy-ion.

Without additional information such as the Bragg peak to disambiguate between elastic and inelastic loci, it is not possible with these data to identify the subset which corresponds to elastic interactions; for any event with an observed energy deposit in the central silicon detector, either an elastic scattering reaction at vertex {math}`v_1` took place, or an inelastic reaction at vertex {math}`v_2`, where {math}`v_1` lies closer in the beam axis towards the silicon detector than {math}`v_2`.

+++

(content:excitation-functions)=
## Excitation Functions

```{code-cell} ipython3
:tags: [hide-cell]

carbon_10 = Particle.from_nucleus_info(a=10, z=6)
helium_4 = Particle.from_nucleus_info(a=4, z=2)
hydrogen_1 = Particle.from_nucleus_info(a=1, z=1)
oxygen_14 = Particle.from_nucleus_info(a=14, z=8)

Q = ((carbon_10.mass + helium_4.mass - oxygen_14.mass) * u.MeV / u.c**2) * u.c**2
```

The calculation of a reaction Q-value is described in {numref}`expt:conservation-rules`. For elastic scattering of {math}`{}^{10}\mathrm{C}` ions upon a {math}`{}^4\mathrm{He}` target, the Q-value is {eval}`Q.to("keV")`. This value is used to build the elastic non-zero-degree excitation function shown in {numref}`excitation-curve`, which is given by {math}`E_\mathrm{ex} = E_1 - E_\mathrm{CoM} + Q = E_1\frac{m_2}{m_1+m_2} + Q`. Without the ability to isolate the elastic and inelastic contributions to the excitation function, it is not possible to combine the data in {numref}`excitation-curve` with those in {numref}`zero-degree-excitation-curve` which plots the zero-degree counterpart. As such, {numref}`zero-degree-excitation-curve` plots the excitation function derived under the assumption that these data were obtained via the elastic, and inelastic channels.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A histogram of the excitation energy of the {math}`{}^{14}\mathrm{O}`
      nucleus integrated over all non-zero-degree scattering angles. States published
      in the ENSDF database are plotted in dashed lines, whilst the various AMD predictions
      discussed in this work for {math}`{}^{14}\mathrm{O}` are, where plausible, indicated
      by solid lines. Clear peak-like structures are visible, against a wider background
      distribution. Despite this, further enhancement of these data through secondary
      fitting is required to provide more conclusive agreement with predicted states.
    name: excitation-curve
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/excitation-function.pickle", "rb") as f:
    excitation_hist = pickle.load(f)

excitation_hist["Angular", ...].plot(label="Elastic")
ax = plt.gca()
ax.xaxis.labelpad = 20
plt.vlines(
    [11970, 12840, 13010, 14640, 17400],
    0,
    500,
    linestyle="--",
    label="ENSDF",
    color="black",
)
plt.vlines([13.32e3, 15.7e3, 17.36e3], 0, 500, label="AMD", color="black")
plt.legend();
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A histogram of the excitation energy of the {math}`{}^{14}\mathrm{O}`
      nucleus computed from the near-zero-degree scattering channel. States published
      in the ENSDF database are plotted in dashed lines, whilst the various AMD predictions
      discussed in this work for {math}`{}^{14}\mathrm{O}` are, where plausible, indicated
      by solid lines.
    name: zero-degree-excitation-curve
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/excitation-function.pickle", "rb") as f:
    excitation_hist = pickle.load(f)

excitation_hist[["Elastic", "Inelastic"], ...].stack(0).plot()
ax = plt.gca()
ax.xaxis.labelpad = 20
ax.xaxis.label_position = "bottom"
plt.vlines(
    [11970, 12840, 13010, 14640, 17400],
    0,
    500,
    linestyle="--",
    label="ENSDF",
    color="black",
)
plt.vlines([13.32e3, 15.7e3, 17.36e3], 0, 500, label="AMD", color="black")
plt.legend();
```

Although the analysis work described in this chapter does not yield sufficient results to elucidate the structure of the {math}`{}^{14}\mathrm{O}` nucleus, it can be seen that a number of peaks in the excitation function coincide with known or predicted energies. Yet, further analysis is still required, including kinematic fitting of the angular measurements, and elastic-inelastic subtraction, to make any deeper observations. The completion of this work is planned by the nuclear physics group at the University of Birmingham, which will identify the cross sections associated with the elastic scattering channel, and use them to infer the states present in {math}`{}^{14}\mathrm{O}`.

+++

(expt:beam-energy-estimation)=
## Beam Energy Estimation

```{code-cell} ipython3
:tags: [hide-cell]

# Energy in keV
m_10c = particle.Particle.from_nucleus_info(6, 10).mass * 1e3
m_4he = particle.Particle.from_nucleus_info(2, 4).mass * 1e3
alpha_to_beam = (m_10c + m_4he) ** 2 / (4 * m_10c * m_4he)

range_4he, de_dx_4he, ion_energy_4he = np.loadtxt(
    "data/4He-in-4He-CO2.csv", delimiter=",", unpack=True
)
range_4he = u.Quantity(range_4he, "cm")
de_dx_4he = u.Quantity(de_dx_4he, "MeV/cm")
ion_energy_4he = u.Quantity(ion_energy_4he, "MeV")

max_si_energy = 23 * u.MeV
range_at_max = np.interp(max_si_energy, ion_energy_4he, range_4he)
energy_at_window = np.interp(range_at_max + 577 * u.mm, range_4he, ion_energy_4he)
```

The beam energy after the Havar window is predicted by SRIM calculations to be ~25 MeV. A preliminary evaluation of this estimate can be performed using the maximum energy deposited in the central silicon detectors. This should correspond to a near zero-degree scatter from the farthest point in the active volume, i.e. the window (see {numref}`max-silicon-hist`). Given a maximum energy of {eval}`max_si_energy`, the after-window beam energy computed by the alpha stopping power is {eval}`energy_at_window * alpha_to_beam`. This value is much larger than the initial prediction, but lies in close agreement with the fit parameter used to produce the theoretical stopping power curve in {numref}`stopping-power-beam-hist`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A histogram of the silicon energy distribution, with inset axes indicating
      a candidate for the maximum value.
    name: max-silicon-hist
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/silicon-maximum-hist.pickle", "rb") as f:
    energy_hist = pickle.load(f)

energy_hist.plot()

# Create an inset axis in the bottom right corner
ax = plt.gca()
x_0 = 23000
real_width = 15000
width = 5000

ax_inset = ax.inset_axes(
    [x_0 - real_width / 2, 300, real_width, 400], transform=ax.transData
)  # Plot the data on the inset axis and zoom in on the important part
energy_hist.plot(ax=ax_inset)
ax_inset.set_xlim(x_0 - width / 2, x_0 + width / 2)
ax_inset.set_ylim(
    -5, 70
)  # Add the lines to indicate where the inset axis is coming from
ax_inset.axvline(23000, linestyle="--")
ax.indicate_inset_zoom(ax_inset)

ax_inset.set_xlabel(None)
ax.xaxis.labelpad = 20
ax.xaxis.label_position = "bottom"

plt.ylim(0, 1000)
plt.axvline(23000, linestyle="--");
```

A more robust approach is to reconstruct the reaction kinematics in the non zero-degree regime, and plot the difference of the projectile energies computed by this reconstruction and directly by energy loss through the gas. {numref}`beam-energy-diff-hist` clearly shows a non-central distribution, indicating that the direct prediction lies below the reconstructed value by ~1 MeV, i.e. the true beam energy after the window is {eval}`energy_at_window * alpha_to_beam + 1*u.MeV`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A histogram of the difference in projectile energy computed directly
      (through SRIM calculations of energy loss in the gas), and via indirect kinematic
      reconstruction (using the known track angles and measured energy deposit in
      the silicon detectors).
    name: beam-energy-diff-hist
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/beam-energy-delta.pickle", "rb") as f:
    beam_energy_delta_hist = pickle.load(f)
beam_energy_delta_hist.plot(label=r"$E_B(\mathrm{si}) - E_B$")
plt.axvline(1e3, linestyle="--", label="Centroid")
plt.legend();
```

It is evident that these calculations are highly sensitive to the stopping power tabulation; the disagreement in {numref}`beam-energy-diff-hist` implies that the stopping powers used in this analysis over-predict the energy loss of the beam in the energy region of interest. There is preliminary experimental evidence to suggest that this is the case for both MSTAR and SRIM {cite:ps}`d_torresi_measurement_2017`. Future work should measure these stopping powers, both of {math}`{}^{10}\mathrm{C}` in {math}`{}^{4}\mathrm{He}` and {math}`{}^{4}\mathrm{He}` in {math}`{}^{4}\mathrm{He}` in order to reduce the discrepancy in the agreement of these two beam-energy estimates.

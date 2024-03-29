---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(expt:silicon-calibration)=
# Silicon Calibration

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}

import pickle
from pathlib import Path

import awkward as ak
import numpy as np
import vector
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from texat.utils.awkward.convert import from_hdf5
from mplhep.styles import ATLAS

plt.style.use(ATLAS)
plt.rc("figure", figsize=(10, 5), dpi=120)
data_path = Path("data")
```

## Semiconductor Detectors
The silicon detectors that surround the TexAT TPC are used to measure the energy of light products that escape the active volume. Within each detector, the periodic structure of the semiconductor's crystalline lattice establishes a set of electron energy bands separated by ranges of forbidden energies. At the Fermi level, the lower energy (_valence_) band comprises a continuum of fully occupied states that are bound to particular lattice sites, whilst the higher energy (_conduction_) band contains entirely unfilled states in which the electrons are free to move throughout the lattice (see {numref}`conduction-valence-band`). 

:::{figure} image/semiconductor-band-structure.svg
---
name: conduction-valence-band
alt: An illustration of the valence and conduction bands in a semiconductor. A dashed line at the Fermi energy indicates the boundary between the lower energy (filled) valence band and the higher energy (unfilled) conduction band.
width: 300px
align: center
---
An illustration of the band structure in a semiconductor. The dashed line indicates the Fermi level that separates the valence and conduction bands.
Figure by Tim Starling & Mliu92, distributed under a [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) license.
:::

The excitation of an electron across the gap between the valence and conduction bands establishes an electron-hole pair, which is free to migrate throughout the lattice. It is the motion of these charge-pairs under an electric field that gives rise to a current. Above 0 K there will exist some steady-state concentration (given by the Boltzmann distribution) of thermal electrons in the conduction band such that the material will be conductive.  

In order to observe the charge-pairs produced by ionisation, there must exist an electric field such that the charge-carriers do not recombine, but rather induce a current through their motion. As any externally developed potential will induce an opposing potential in the material, it follows that this field must be established through intrinsic diffusion of the charge carriers. To this end, one can _dope_ the semiconductor lattice with substitutional impurities that introduce a surplus of a particular charge carrier. These dopant atoms do not conserve the electron-hole equilibrium, i.e. they introduce a majority of the singular charge carrier that exclusively determines the material's electric conductivity. Semiconductors doped with donor (electron) impurities are denoted N-type semiconductors whilst those with acceptor impurities are termed P-type materials (see {numref}`np-doping`). 


::::{subfigure} AB
:layout-sm: A|B
:gap: 8px
:subcaptions: below
:name: np-doping

:::{image} image/p-type-doping.svg
:alt: (a)

:::

:::{image} image/n-type-doping.svg
:alt: (b)

:::

An illustrative diagram of the minority-majority charge carriers in an (a) p-type semiconductor and (b) n-type semiconductor. A surplus of mobile charge carriers can be seen in the conduction band. The charge carriers in p-type semiconductors (a) are termed holes, whilst those in n-type materials (b) are electrons.
::::

+++

Upon interfacing two alternately doped semiconductors, a P-N junction is formed. An initial gradient in the concentration of charge carriers leads to the establishment of a "depletion zone" in which electrons and holes combine, filling the valence band. This displacement of the majority charge carriers in turn establishes an electric field that inhibits further diffusion (see {numref}`p-n-junction`). These two phenomena render the depletion zone an ideal region for radiation detection; the electron-hole pairs formed by ionisation will quickly move under the electric field to establish a measurable current. 

The _contact potential_ established by the space charge at either end of the junction is of the order $\sim 1\,V$, which yields a poor electron-hole mobility. An electric potential can be applied to either side of the junction, widening the depletion region and reducing the likelihood of charge-pair recombination. Known as reverse biasing, this significantly improves the detector performance.

:::{figure} image/pn-junction-equilibrium-graphs.png
---
name: p-n-junction
alt: An illustrative diagram of the charge-carrier distribution across a P-N junction. The holes in the P-type region and electrons in the N-type region are shown to reduce in concentration towards their counterparts. The space charge potential due to net charge carrier diffusion is shown to be maximal at the junction interface, and tending to zero outside of a given thickness.
width: 800px
align: center
---
An illustrative diagram of the charge-carrier distribution across a P-N junction. Additional graphs show the charge, field, and electric potential, across the junction. Figure by TheNoise, distributed under a [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en) license.
:::


%s the number of charge pairs produced by ionisation is proportional to the deposited energy, it is the time integral of the measured current that 
%In each region, a surplus of mobile charge carries is introduced through substitutional impurities, which serve to modify the 
% - [x] The periodic lattice of crystalline materials establishes allowed energy bands for electrons that exist within that solid.
% - [x] valence band, corresponds to those outer-shell electrons that are bound to specific lattice sites within the crystal
% ~~unlike metals, The number of electrons within the crystal is just adequate to fill completely all available sites within the valence band.~~
% ~~conduction in metals doesn't generate holes in valence band, just moves around (unlike semiconductor)~~
% donor impurities introduce loosely bound charge. Doesn't create hole, as only loosely bound? Maybe hole doesn't migrate because so sparsely distributed within material - long range interaction instead of short-range neighbours?
% mostly liberated by thermal conduction excitation
% in intrinsic semiconductor, holes & pairs only from thermal ex, so ni=pi
% p type have holes (vacancies) close to valence band - thermal ex from valence band fills vacancies, leaving holes in valence band
% Deposition of energy within these detectors leads to the formation of electron-hole charge-carriers that are excited to the conduction band of the material. The motion of these charge-carriers in an applied electric field gives rise to a current, whose time integral is approximately proportional to the deposited energy. 
% natural "contact" potential arises even though doped materials have net 0 charge . Need rev biasing to fully collect charges
% depletion region introduces net charge imbalance & removes charge carriers
% contact potential ~< band gap, arises due to space charge effects
% rev bias widens depletion region

+++

It is the time-integral of the current induced within the semiconductor that is proportional to the energy deposited within the material. In order to determine the constant of proportionality between the measured signal and the deposited energy, the detector must first be calibrated with a known source. 

For this experiment, a four-peak alpha source was suspended within the TexAT TPC chamber, which was held under vacuum. A list of constituent isotopes and their decay radiation is given in {numref}`calibration-sources`.

:::{list-table} Isotopes present in the four-α calibration source, and their α decay radiation. From ENSDF database as of March 24th, 2023. Version available at <http://www.nndc.bnl.gov/ensarchivals/>.
:name: calibration-sources
:header-rows: 1

* - Isotope
  - Energy /keV
  - Intensity (%)
* - <sup>241</sup>Am
  - 5442.8
  - 13.1
* - 
  - 5485.6
  - 84.8
* - <sup>244</sup>Cm
  - 5762.6
  - 23.1
* - 
  - 5804.8
  - 76.9
* - <sup>239</sup>Pu
  - 5105.5
  - 11.9
* - 
  - 5144.3
  - 17.1
* - 
  - 5156.6
  - 70.8
* - <sup>148</sup>Gd
  - 3182.7
  - 100
:::

+++ {"tags": ["remove-input", "remove-output"]}

The waveforms recorded by the GET acquisition system were fit using the methods described in {numref}`expt:signal-fitting`, and the corresponding charge accumulated in a histogram. It can be seen in {numref}`calibration-spectra` that the majority of the silicon quadrants measured similar signal amplitudes for the given sources. A total of 11 quadrants were found to have an insufficient number of hits to be able to build a calibration, primarily those in the forward silicon detector array. See {numref}`calibration-quadrant-map` for a visual representation of these missing quadrants.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A schematic diagram of the (a) forward and (b) side silicon detector
      arrays indicating quadrants with incomplete calibrations in pink.
    name: calibration-quadrant-map
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open(data_path / "calibration-heatmap.pickle", "rb") as f:
    calibration_heatmap = pickle.load(f)[:, ::2j]
quadrant_table = from_hdf5(data_path / "calibration.h5")
count = np.sum(calibration_heatmap.values(), axis=-1)
quadrant = ak.zip({"position": quadrant_table.position, "count": count}, depth_limit=1)
is_forward = quadrant.position.y > 190

vertices = (
    ak.where(
        is_forward,
        vector.zip({"x": quadrant.position.x, "y": quadrant.position.z}),
        vector.zip({"x": quadrant.position.y, "y": quadrant.position.z}),
    )[:, np.newaxis]
    + vector.zip(dict(x=[-1, -1, 1, 1], y=[-1, 1, 1, -1]))[np.newaxis, :] * 12.5
)
vert = ak.concatenate(
    (vertices.x[..., np.newaxis], vertices.y[..., np.newaxis]), axis=-1
)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, width_ratios=(200, 250))

ax1.add_collection(
    PolyCollection(
        vert[(quadrant.count > 100) & is_forward],
        edgecolors="black",
        facecolors="green",
        linestyle="--",
        alpha=0.2,
    )
)

ax1.add_collection(
    PolyCollection(
        vert[(quadrant.count <= 100) & is_forward],
        edgecolors="black",
        facecolors="red",
        linestyle="--",
        alpha=0.2,
    )
)
ax2.add_collection(
    PolyCollection(
        vert[(quadrant.count > 100) & (~is_forward)],
        edgecolors="black",
        facecolors="green",
        linestyle="--",
        alpha=0.2,
    )
)

ax2.add_collection(
    PolyCollection(
        vert[(quadrant.count <= 100) & (~is_forward)],
        edgecolors="black",
        facecolors="red",
        linestyle="--",
        alpha=0.2,
    )
)
ax1.set_xlabel("x /mm")
ax1.set_ylabel("y /mm");
ax1.set_title("(a)")
ax1.set_xlim(-100, 100)
ax1.set_ylim(-100, 100)
ax1.set_aspect(1)
ax2.set_title("(b)")
ax2.set_xlim(-125, 125)
ax2.set_ylim(-100, 100)
ax2.set_aspect(1)
ax2.set_xlabel("x /mm");
```

```{code-cell} ipython3
---
jupyter:
  source_hidden: true
mystnb:
  figure:
    caption: A 2D histogram of the charge distribution measured by each silicon detector
      for a fixed calibration source containing <sup>241</sup>Am, <sup>148</sup>Gd,
      <sup>239</sup>Pu, and <sup>244</sup>Cm.
    name: calibration-spectra
  image:
    align: center
    width: 1280px
tags: [hide-input]
---
fig_heatmap = plt.figure(figsize=(24, 10))
ax = fig_heatmap.gca()
calibration_heatmap.plot2d(ax=ax)
ticks = ax.get_xticks()
ax.set_xticks(ticks[::2]);
```

Where charge-pair formation is not the primary mode of energy loss within the semiconductor, the number of created pairs is governed by Poisson counting statistics {math}`\operatorname{Var}(N)=N`. Meanwhile, in the limit that charge-pair formation is the singular energy-loss mechanism, the number of charge pairs is exactly determined by the deposited energy (ignoring the distribution on the ionisation energy), i.e. {math}`\operatorname{Var}(N)=0`. The ratio between the observed variance and its Poissonian expectation value is the Fano factor: {cite:ps}`subashiev_correlation_2010`
:::{math}
:label: fano-factor
F=\frac{\langle\delta N^2\rangle}{\langle N\rangle}\,,
:::
where {math}`\langle\delta N^2\rangle` is the observed variance and {math}`\langle N\rangle` the observed mean. In silicon detectors, which exhibit a high charge-pair formation efficiency, $F$ is experimentally found to be of the order $10^{-1}$ {cite:ps}`kotov_pair_2018`{cite:ps}`alig_scattering_1980`.

+++ {"tags": ["no-latex"]}

:::{note}
Simplified "final-state" models can predict the experimental values for {math}`F` with a microscopic assuming a single-particle-distribution function. One such model, the "bathtub model", assumes no inter-charge-pair correlations and draws from this single-particle-distribution to partition the deposited energy. It has been shown that correlational effects are required to fully reproduce experimental measurements of $F$, through models such as the random parking problem (RPP) {cite:ps}`subashiev_correlation_2010`.
:::

% See also http://www.ee.sunysb.edu/~serge/235.pdf and https://arxiv.org/pdf/0911.1532.pdf
% each shot is random uncorrelated -> central limit theorem -> gaussian energy distribution
% correlation effects lead to increasing F close to true value (mainly NN effects)
% resolution vs efficiency - bigger detectors collect compton scattering, worse res

+++

For each detector, the charge distribution was fit as a sum of four Gaussian distributed random variables.

+++ {"tags": ["no-latex"]}

:::{note}
The motivation for a Gaussian fit function follows from the application of the central-limit-theorem to the final-state model of charge-pair formation {cite:ps}`subashiev_correlation_2010`, yielding
```{math}
P(E_{N})=C_{N}\exp\left[-\frac{(E_{N}-N\epsilon)^{2}}{2N\langle\delta\epsilon^%
{2}\rangle}\right]~{}.
```
:::

+++

In order to determine the set of initial fit parameters, a cumulative mass lookup was used to estimate the peak loci (see {numref}`calibration-charge-cmf`), and sensible values chosen for the peak width and scaling factor.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: The charge distribution for a random silicon detector, superimposed with
      a plot of the cumulative distribution. The dashed lines indicate particular
      fractions of the cumulative distribution at which the peaks are localised.
    name: calibration-charge-cmf
  image:
    align: center
    width: 512px
tags: [hide-input]
---
y = calibration_heatmap[5j, :].values()
charge = calibration_heatmap.axes[1].centers
charge_edge = calibration_heatmap.axes[1].edges

# CMF loci of peaks
cmf = np.cumsum(y) / np.sum(y)
peak_cmf = np.r_[0.14, 0.44, 0.67, 0.9]
i_peak = np.searchsorted(cmf, peak_cmf)

fig_cmf, ax = plt.subplots()
ax.scatter(charge[i_peak], y[i_peak], label="Peak", color="C0")
ax2 = ax.twinx()
lines = ax.plot(charge, y, label="Charge", color="C0") + ax2.plot(
    charge, cmf, label="CMF", color="C1"
)
ax2.scatter(charge[i_peak], peak_cmf, marker="x", color="C1")
ax2.hlines(
    peak_cmf,
    charge[i_peak],
    charge_edge[-1],
    linestyle=(0, (3, 2)),
    color="C1",
    alpha=0.3,
)
plt.legend(handles=lines)
ax.set_xlabel("Charge /arb")
ax.set_ylabel("Counts");
ax2.set_ylabel("CMF");
plt.tight_layout()
```

This method of localising the decay peaks from the calibration source is robust in the face of varying detector noise.

+++

## Calibration
Following the peak fitting process, a linear regression was then performed against the known energies given in {numref}`calibration-sources` to obtain a set of calibration coefficients for each detector. A superposition of the calibrated charge distributions can be seen in {numref}`calibrated-distributions`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A combined plot of the calibrated charge distribution histograms. The
      characteristic decay peak energies are shown in the staggered X axis.
    name: calibrated-distributions
  image:
    align: center
    width: 512px
tags: [hide-input]
---
calibration = ak.Array(
    [
        [[5442.80, 13.1], [5485.56, 84.8]],  # Am
        [[5762.64, 23.10], [5804.77, 76.90]],  # Cm
        [[5105.5, 11.94], [5144.3, 17.11], [5156.59, 70.77]],  # Pu
        [[3182.690, 100]],  # Gd
    ]
)

source_energy = ak.to_numpy(
    np.sort(
        np.sum(calibration[..., 1] * calibration[..., 0], axis=1)
        / np.sum(calibration[..., 1], axis=1)
    )
)

fig_combined, ax = plt.subplots(figsize=(14, 4))
ax.plot(
    quadrant_table.coefficient[:, 1] * charge[:, np.newaxis] + quadrant_table.coefficient[:, 0],
    np.transpose(calibration_heatmap.values()),
)
ax.set_xlabel("Energy /keV")
ax.set_ylabel("Counts")
ax.set_xlim(2500, 6500)

ticks = np.c_[
    np.r_[xticks := np.linspace(2500, 6500, 9), source_energy],
    np.r_[np.zeros_like(xticks), np.full_like(source_energy, 15)],
]
ticks = ticks[np.lexsort(ticks[:, [1, 0]].T)]

for tick, pad in zip(ax.set_xticks(ticks[:, 0]), ticks[:, 1]):
    tick.set_pad(pad)
```

## Resolution

+++

The energy resolution of a detector is a measure of its performance with respect to the resolution of fine detail in the deposited energy.

It is conventionally given as the dimensionless quantity
:::{math}
:label: resolution
R = \frac{\text{FWHM}}{E}\,,
:::
where $E$ is the mean, and $\text{FWHM}$ the full-width at half-maximum (FWHM) of the energy distribution. Given {eq}`fano-factor`, this expands to
:::{math}
:label: silicon-resolution-fano
R = 2\sqrt{\frac{2\ln{2}Fk}{E}}\,,
:::
where $F$ the Fano factor, and $k$ is the mean number of charge carriers liberated per unit energy deposited in the detector. Experimental measurements have found $k$ to be approximately 3.6 eV for alpha particles in silicon {cite:ps}`kotov_pair_2018`{cite:ps}`scholze_mean_1998`{cite:ps}`alig_scattering_1980`.

+++

Whilst the majority of the calibrated detectors were found to have a resolution of 70-120 keV at 3182.7 keV, it can be seen that some detectors exhibited clear signs of degraded resolution. The waveforms measured by these detectors were subsequently discarded.

<!-- :::{warning}
Is this resolution too poor given [^1]?
> (...) only one of 12 has lost the resolution below an acceptable level (75 keV).
[^1]: https://www.sciencedirect.com/science/article/pii/S0168900220300073
::: -->

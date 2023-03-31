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

(expt:the-texat-detector)=
# The TexAT Detector for Rare Isotope Beam Experiments

```{code-cell}
:tags: [hide-cell]

import awkward as ak
import k3d
import numpy as np
from IPython.display import Image
from matplotlib.cm import viridis
from utils import displayed_as_mimebundle
```

TexAT (Texas Active Target) is a general-purpose detector developed by the Cyclotron Institute at Texas A&M University for low-energy nuclear physics experiments {cite:ps}`koshchiy_texas_2020`. As an active-target detector, the fill gas serves as both the detection medium and the target, such that TexAT is well suited to conducting scattering and implantation experiments with rare isotope beams.

TexAT has been upgraded over several experiments. In this section, the initial design of the detector will be outlined, followed by an exploration of the modifications relevant to the experiment discussed later in the chapter.

+++

## Experiment Design

+++

A primary {math}`{}^{10}\mathrm{B}^{3+}` beam with 7 MeV/u was produced by the K500 cyclotron at the Cyclotron Institute, Texas A & M University {cite:ps}`youngblood_texas_1991`. These ions were directed towards a liquid-nitrogen (LN) cooled 9.2 cm gas cell, with 4 μm thick and 19 mm diameter Havar entrance and exit windows {cite:ps}`hooker_structure_2019`. At a pressure of  870 torr, the {math}`\mathrm{H}_2` gas within the cell was used to facilitate an {math}`{}^{10}\mathrm{B}(p,n){}^{10}\mathrm{C}` exchange reaction. The resulting {math}`{}^{10}\mathrm{C}` beam had an energy of 32.9 MeV, and an intensity of 7500–16500 particles per second (pps).

+++

## Detector Overview

+++

TexAT is comprised of a gas-filled TPC and MicroMeGaS (Micro-Mesh Gaseous Structure) particle detector, surrounded by an array of telescopes for particle identification and total energy measurement of ions that escape the active volume. A 3D model of these detectors is shown in {numref}`texat-detector-3d`.

```{code-cell}
---
mystnb:
  figure:
    caption: A 3D model of the "final" innermost TexAT detector components, comprised of silicon (purple), thallium doped cesium iodide (turquoise), and MicroMeGaS (yellow) detectors. The ion counter is not pictured here.
    name: texat-detector-3d
  image:
    align: center
    alt: A time-projection-chamber detector with a MicroMeGaS anode and array of silicon
      detectors surrounding the exterior of the active volume.
    width: 512px
tags: [hide-input]
---
with open("../content/model/silicon.json", "r") as f:
    silicon = ak.from_json(f.read())
with open("../content/model/cesium.json", "r") as f:
    cesium = ak.from_json(f.read())
with open("../content/model/micromegas.json", "r") as f:
    micromegas = ak.from_json(f.read())


def rgb_to_packed(rgb):
    col = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return int(col[0] << 16 | col[1] << 8 | col[2])


col = viridis(np.linspace(0, 1, 3))

plot = k3d.plot(camera_auto_fit=False)

plot += k3d.mesh(silicon.vertex, silicon.index, color=rgb_to_packed(col[0]), name="Si")
plot += k3d.mesh(
    cesium.vertex, cesium.index, color=rgb_to_packed(col[1]), name="CsI(Tl)"
)
plot += k3d.mesh(
    micromegas.vertex * [[1, 1, -1]],
    micromegas.index,
    color=rgb_to_packed(col[2]),
    name="MicroMeGaS",
)
plot.camera = [
    475.765746444383,
    -236.658468205975,
    303.60900138312763,
    60.14126510733682,
    173.88348471035994,
    -143.0433116963373,
    -0.41591720629770645,
    0.37906690479277294,
    0.8266324208475794,
]
# Provide image fallback
with displayed_as_mimebundle() as c:
    display(plot, Image("image/texat-tpc-volume.png"))
```

To establish a uniform electric field within the ionisation region, a wire field-cage surrounds the active volume. 
An isographic 3D rendering of the combined detector with the field-cage and MicroMeGaS visible is shown in {numref}`texat-detector-2d`.

+++

:::{figure} image/placeholder/texat-detector.png
:name: texat-detector-2d
:align: center
:alt: A time-projection-chamber detector with a MicroMeGaS anode and array of silicon detectors surrounding the exterior of the active volume.
:width: 400px

The TexAT detector configuration. A black arrow indicates the direction of the beam, which first enters the detector through the ion-counter (IC, indicated). The segmented anode is visible in blue and purple at the top of the detector, whilst the field-cage (FC) and the array of CsI(Tl) + Si detectors are visible around the outside of the TPC volume. Figure taken from Ref. {cite:ps}`barbui_ensuremathalpha-cluster_2022`.
:::

+++

(expt:micromegas)=
### MicroMeGaS

The MicroMeGaS is a parallel-plate gas particle detector. It comprises of a micro-pattern anode, with a thin metallic mesh suspended at a height of 128 μm above the surface (see {numref}`micromegas-schematic`). This _micro_-mesh partitions the gas into two juxtaposed volumes of differing potentials, forming a large drift region above the mesh, and a small amplification region between the mesh and the anode

+++

:::{figure} image/placeholder/drift-micromegas.png
:name: micromegas-schematic
:alt: A charged particle ionises the detector gas along its path, producing charge clusters which drift towards the anode. These clusters pass through a micromegas into the high-field amplification region, whose avalanches are detected on the anode.
:width: 400px
:align: center

Charge signal formation from charged particle ionisation. The small amplification region can be seen between the mesh and the anode strips, with a much higher electric field than that of the drift region, of the order ~kV/cm. Figure taken from Ref. {cite:ps}`manjarres_performances_2012-1`.
:::

+++

In this manner, the detector behaves like an ideal parallel plate detector; the signals formed on the anode readout are predominantly determined by the electron mobility of the gas rather than that of the ions. The irregular pixellation of the anode facilitates high position resolution measurement of these signals. The bias for the mesh is constant across the detector geometry; individual region biasing is performed by applying different potentials to the corresponding elements of the anode.

+++

The MicroMeGaS anode has an active area of $245\times224\,\text{mm}^2$, which is composed of three distinct conductive elements:
- single electrode rows ($112\times1.67\,\text{mm}^2$)
- chained electrode columns ($1.67\times224\,\text{mm}^2$) 
- single electrode pads ($3.42\times1.67\,\text{mm}^2$)

These elements are arranged into a three-region configuration: the two side regions are formed by interleaving strips and chains, and the central columnar region is composed from a regular grid of pads (see {numref}`micromegas-anode`). To ensure that adjacent elements remain electrically isolated from one another, the separation between disjoint strips and chains is 1.75 mm, whilst separate pads are separated by chains is 1.75 mm and 3.5 mm in the vertical and horizontal axes respectively.

+++

:::{figure} image/placeholder/micromegas-anode.png
:name: micromegas-anode
:alt: A schematic diagram showing the different regions within the MicroMeGaS anode. A central pixellated column is visible, between two side regions formed from stagged strips and contiguous chains.
:width: 400px
:align: center

The segmentation plan of the MicroMeGaS anode. There are three distinct regions: a central column of $6\times 128$ pads, and two side regions with 64 interleaved rows (strips) and columns (chains). The strips are formed from single electrodes, whilst the chains are formed from staggered readout pads that are electrically connected together. Note that the measurements in this figure were subsequently revised for fabrication. Figure adapted from Ref. {cite:ps}`koshchiy_texas_2020`.
:::

+++

The multiplexing scheme present in the side regions is used to reduce the number of channels from $64\times128$ to $64+64$, at a cost of lower resolution, sensitivity, and reconstruction ambiguity. The readout is mapped such that individual zones within the MicroMeGaS can be biased in order to create areas with different gas gains.

+++

### Silicon

In the TexAT configuration used in the experiment described in this chapter, only the silicon quadrant detectors were present. Without the thallium-doped caesium iodide detectors, only partial energy can be measured for escaping ions that punch through the silicon detectors. In these cases, particle identification must be performed by alternate means.

Two families of silicon detector are used in the TexAT detector:
- MSQ25-1000 (Micron Semiconductor)
- KDP-1K (JSC, “Institute in Physical-Technical Problems”, Dubna, Russia)

Both of these detectors are configured with four ($25\times25\,\text{mm}^2$) quadrants, as shown in {numref}`silicon-schematic`. Although the MSQ25-1000 includes an additional rear quadrant ($50\times50\,\text{mm}^2$), it was not read-out for this experiment.

+++

:::{figure} image/placeholder/silicon-schematic.png
:name: silicon-schematic
:alt: Schematic views of the four different telescope configurations within the TexAT detector. All show a semi-regular grid of quadrant detectors, with one configuration showing a cutout for the beam.
:width: 400px
:align: center

A 3D rendering of the solid-state detector telescopes that surround the TPC: downstream array (top left); upstream array (bottom left); side array (top right); bottom array (bottom right). Figure taken from Ref. {cite:ps}`koshchiy_texas_2020`.
:::

+++

### Ion Counter
For this experiment, a planar windowless ionisation chamber (IC) was placed immediately after the entrance window to the gas volume to detect the beam current (see {numref}`texat-detector-2d`). Through charge-time discrimination, the signals of this detector can be used to identify the beam ion, help to eliminate pile-up within the TPC, and trigger the acquisition system in coincidence with the other detectors.

+++

## Readout Electronics

(expt:get-architecture)=
### GET Architecture
TexAT uses the General Electronics for TPCs (GET) system for readout of the detectors {cite:ps}`pollacco_get_2018`. GET comprises of a heirarchy of electronic components, starting at the lowest level with the AGET (ASIC, Application-Specific Integrated Circuit, for GET) chip to amplify, shape, and store the signals from each detector (see {numref}`get-schematic`).

+++

:::{figure} image/placeholder/get-schematic.png
:name: get-schematic
:alt: Schematic diagram of the GET electronics system. A series of channels is read by each AGET chip. There are four AGET chips for each AsAd board, and there are four AsAd boards for each CoBo.
:width: 400px
:align: center

An illustration of the relationship between the experimental detector, readout electronics, and data acquisition and storage equipment in an experiment that uses the GET system {cite:ps}`pollacco_get_2018`.
:::

+++

Each channel possesses an independent trigger and continuously samples the filtered analogue signal from the shaper, with a sampling frequency between 1 and 100 MHz, using a 512-cell switch-capacitor circular buffer {cite:ps}`pollacco_get_2018`. A single AGET chip has 64 independent channels in addition to 4 floating channels that provide a measure of the electronic noise, known as fixed-pattern noise (FPN) channels. These FPN channels are distributed across the AGET chip in order to place one FPN channel at the edge of each chip {cite:ps}`pollacco_get_2018`. 

To read out all of the channels in a TexAT detector requires 24 AGET chips. There are 4 AGET chips on each AsAd (ASIC and Analog to Digital converter) board, which digitises the signals from the SCA memory of the AGET chips using a 12-bit ADC {cite:ps}`pollacco_get_2018`. The data from these AsAd boards are collected by a series of CoBo's (Concentration Boards), which timestamp the information and transmit it to the storage infrastructure. 

In order to synchronize the CoBos and generate a global trigger, an additional board called the MuTAnT (MUltiplicity Trigger ANd Time) is used.

+++

### Signal Shaping

+++

The internal pre-amplification stage (CSA) in each AGET chip can be bypassed in cases where exernal pre-amplifiers need to be read-out by the GET electronics {cite:ps}`pollacco_get_2018`. For this experiment, instead of using the internal GET pre-amplifier, the IC is connected via a bypass circuit (see {numref}`external-shaper`) to an external MESYTEC shaper (MSCF-16), whose signals are fed back into the Gain-2 stage of AGET chip, as discussed in {cite:ps}`koshchiy_texas_2020`.

+++

:::{figure} image/placeholder/external-shaper.png
:name: external-shaper
:alt: Schematic diagram of the bypass mechanism for the AGET chip.
:width: 300px
:align: center

A schematic diagram of the shaper bypass facility of AGET chips. External shapers are used for the ion counter signals (see above). Figure adapted from Ref. {cite:ps}`koshchiy_texas_2020`.
:::

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

# Signal Ringing

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}

import pathlib
import pickle

import awkward as ak
import hist
import numpy as np
from matplotlib import pyplot as plt
from mplhep.styles import ATLAS
from texat.signal.convolution import gold_deconvolve_fft
from texat.signal.statistics import rolling_statistics
from texat.utils.awkward.convert import from_hdf5
from texat.utils.awkward.structure import groupby

plt.style.use(ATLAS)
plt.rc("figure", figsize=(10, 5), dpi=120)

data_path = pathlib.Path("data")
```

In the presence of shaped signals whose amplitudes exceed the dynamic range of the ADC, spurious waveforms are observed in the other channels of the acquisition system. This phenomenon, known as "ringing", presents a challenge to the reconstruction of particle trajectories within the TPC. An example waveform is shown in {numref}`ringing-waveform`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A waveform with the ringing phenomenon visible at {math}`t\sim 345`.
      A distinct non-ringing component is also visible at {math}`t\sim 254`. The shaded
      region indicates the span covering ringing in this channel.
    name: ringing-waveform
  image:
    align: center
    width: 512px
tags: [hide-input]
---
y_ringing = np.load(data_path / "sample-ringing.npy")

plt.figure(figsize=(12, 6))
plt.stairs(y_ringing)
plt.ylabel("Amplitude")
plt.xlabel("Time /cells")
plt.axvline(345, linestyle="--", color="C1", label="Ringing Locus")
plt.axvspan(320, 420, alpha=0.1, color="C1", label="Ringing Span")
plt.legend();
```

(texat:pulse-width-identification)=
## Pulse Width Identification

+++

In order to identify and eliminate these spurious signals, one approach might be to consider the narrow width of the primary peaks. On average, it can be seen that ringing waveforms posses sharper peaks than true waveforms (see {numref}`ringing-width-distribution`)

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: The distribution of peak widths for ringing and non-ringing events.
    name: ringing-width-distribution
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open(data_path / "correlations-hist.pickle", "rb") as f:
    hist_correlations = pickle.load(f)

plt.figure(figsize=(12, 6))
hist_correlations[0:len:sum, 0, 0.8j:, :500j:sum].plot(
    density=False,
    label="No Ringing",
)
hist_correlations[0:len:sum, 1, 0.8j:, :500j:sum].plot(
    density=False,
    label="Ringing",
)
plt.legend();
```

However, given that the shape of these ringing waveforms is not that of a typical GET waveform (see {numref}`ringing-waveform`), it follows that we cannot rely on the fit (which assumes a regular response function) as a robust description of the ringing peak. In order to identify and remove these waveforms, a different approach must be taken.

+++

## Pulse Height Identification

+++

As outlined above, the appearance of ringing waveforms in the sampled GET waveforms follows from the presence of saturated channels. Predictably, these ringing waveforms also occur at a similar time to that of the saturated signals (see {numref}`ringing-width-distribution`)

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A waveform from the same event as {numref}`ringing-waveform` in which
      the signal is saturated at {math}`t\sim 345`. The shaded region indicates the
      span covering ringing signals in other channels.
    name: saturated-waveform
  image:
    align: center
    width: 512px
tags: [hide-input]
---
y_saturated = np.load(data_path / "sample-saturated.npy")

plt.figure()
plt.stairs(y_saturated)
plt.ylabel("Amplitude")
plt.xlabel("Time /cells")
plt.axvline(345, linestyle="--", color="C1", label="Ringing Locus")
plt.axvspan(320, 420, alpha=0.1, color="C1", label="Ringing Span")
plt.legend();
```

Consequently, the loci of peaks fit to saturated waveforms can be used to define a set of time intervals in which ringing signals may be anticipated. Given that one cannot use the GET fit to perform a robust classification between a measurement and a ringing signal, the amplitude of the signal may be used instead. It is observed that the majority of ringing signals have amplitudes well below that of the saturated signal, on the order of {math}`y < 750` units. By taking the logical AND of these two conditions, a better classification of ringing signals can be performed.

+++

:::{figure} image/placeholder/ringing-event-cleanup.png
---
name: ringing-event-hit
alt: A 2D hitmap of the MicroMeGaS anode for a random event. A large number of strips and chains in the left region have been activated, but do not appear to agree with the precursor track in the pads region.
width: 1024px
align: center
---
A 2D hitmap of the MicroMeGaS anode for a random event. (a) A raw event heatmap with ringing signals. Note that the majority of the elements in the left side region have been activated. The linear track formed in the central pads region does not suggest such a pattern will be observed in the side region. (b) A modified hitmap with ringing signals and invalid fits removed. The resulting hitmap more closely agrees with the predicted track yielded by the central pads region.
:::

+++

## Periodicity

+++

The presence of saturated signals in the MicroMeGaS detector gives a locus (in time) for ringing signals to occur. It is not sufficient to discriminate those elements which are trigged by legitimate signals at this locus from those which are experiencing the ringing phenomenon. The damped periodicity of the ringing signals can be used to further discriminate one from the other. {numref}`ringing-waveform-deconvolved` shows the result of computing a deconvolution of the baseline-adjusted waveform. It can clearly be seen that the peaks in the shaded region are of a similar amplitude, and narrow widths, whilst the those associated with the locus at {math}`t=250` are dominated by a single, broad peak.

The baseline is adjusted such that the waveform is positive definite. The GOLD algorithm {cite:ps}`morhac_multidimensional_2005` used to deconvolve ringing waveforms requires such a condition. Furthermore, the baseline estimation procedure outlined in {numref}`texat:micromegas-baseline-estimation` does not produce reasonable solutions in the event that the baseline is dominated by a strong noise component. This is a significant problem for signals with ringing artefacts, which therefore require baseline adjustment in order to properly recover the peaks.

It follows that a veto window that start immediately before the saturated waveform locus, and extends several peak-widths beyond it, can be defined. Waveform peaks that are identified within this veto window are only retained iff. they demonstrate a reasonable width (see {numref}`texat:pulse-width-identification`), and they have no secondary ringing peaks (identified as above) with a primary-amplitude ratio that exceeds a threshold value.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A waveform with the ringing phenomenon visible at {math}`t\sim 345`,
      and the deconvolution of the baseline adjusted signal overlaid. A distinct
      non-ringing component is also visible at {math}`t\sim 254`. The shaded region
      indicates the span covering ringing in this channel. It can be seen that the
      green peaks in the shaded region have much higher relative amplitudes, and much
      narrower widths.
    name: ringing-waveform-deconvolved
  image:
    align: center
    width: 512px
tags: [hide-input]
---
response_si = np.load(data_path / "response-si.npy")
sample_mm = np.load(data_path / "sample-double-mm.npy")

y_ringing_zero = y_ringing - np.min(y_saturated)
y_ringing_source = gold_deconvolve_fft(y_ringing_zero, response_si, 15, 20, 1.4)

fig, ax = plt.subplots()
handles = [ax.axvspan(320, 420, alpha=0.1, color="C1", label="Ringing Span")]
handles.append(ax.stairs(y_ringing, label=r"$y$"))
ax.set_ylabel("Amplitude")
ax.set_xlabel("Time /cells")
ax2 = ax.twinx()
handles.append(
    ax2.stairs(
        y_ringing_source,
        color="C2",
        label=r"$\operatorname{Deconv}(y - \operatorname{min}(y))$",
    )
)
plt.legend(handles=handles);
```

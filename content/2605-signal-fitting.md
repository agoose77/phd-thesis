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

(expt:signal-fitting)=
# Signal Fitting

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from mplhep.styles import ROOT
from scipy.fft import irfft, rfft
from scipy.optimize import minimize, minimize_scalar
from texat.signal.convolution import gold_deconvolve_fft
from texat.signal.waveforms import GET_response, gaussian

plt.style.use(ROOT)
plt.rc("figure", figsize=(10, 5), dpi=120)

data_path = Path("data")
```

In the above sections, it was established that the sampled GET waveforms are effectively convolutions of an original source signal and the intrinsic GET shaper response function. Having determined an approximation for this response function, the source signals can then be recovered by deconvolutional methods. 

## MicroMeGaS Signals
For each preprocessed MicroMeGaS waveform, a convolutional Gaussian fit is performed using a nonlinear least squares optimiser that solves $y = F * \mathcal{N}(\boldsymbol{\phi})$ for the set of model parameters $\boldsymbol{\phi}$. This is preferred over computing the Gaussian fit of the deconvolved signal; although repeated convolution is much more computationally expensive, it is less vulnerable to artefacts produced by the deconvolution technique. For samples which do not exceed the dynamic range of the acquisition system, the peak multiplicity is estimated using the GOLD deconvolution algorithm with boosting {cite:ps}`morhac_multidimensional_2005`, which collapses broad peaks into smooth, sharp peaks. These peaks are then identified using a simple turning-point localiser, which is used to seed the initial fit parameters (see {numref}`boosted-peak-search`).

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A plot of the peaks identified within a MicroMeGaS waveform sample using
      boosted GOLD deconvolution.
    name: boosted-peak-search
  image:
    align: center
    width: '512'
tags: [hide-input]
---
sample_mm = np.load(data_path / "sample-double-mm.npy")
response_si = np.load(data_path / "response-si.npy")

fig, ax = plt.subplots(sharex=True)
ax2 = ax.twinx()
ax.set_ylim(0, 1250)
ax2.set_ylim(0, 10250)
ax.stairs(sample_mm[1], color="C0", label="Signal")
ax2.stairs(
    gold_deconvolve_fft(np.clip(sample_mm[1], 0, np.inf), response_si, 20, 10, 1.4),
    color="C1",
    linestyle="--",
    label="GOLD Deconvolution",
)
ax.set_xlabel("Time /cells")
ax.set_ylabel("Amplitude")
ax2.set_ylabel("Amplitude")
plt.legend();
```

In some cases, the measured sample exceeds the dynamic range of waveform amplitudes that can be measured. This saturation introduces a discontinuity in the derivative of the sample, which renders it un-amenable to deconvolution (see {numref}`signal-saturation-discontinuity`).

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A plot of the saturated MicroMeGaS waveform sample, and its GOLD deconvolution.
    name: signal-saturation-discontinuity
  image:
    align: center
    width: '512'
tags: [hide-input]
---
with open("data/sample-saturated-mm.npy", "rb") as f:
    y_demo = np.load(f)

fig, ax = plt.subplots(sharex=True)
ax2 = ax.twinx()
ax.set_ylim(0, 4096)
ax2.set_ylim(0, 4096 * 20)
handles = [
    ax.stairs(y_demo[9], color="C0", label="Signal"),
    ax2.stairs(
        gold_deconvolve_fft(np.clip(y_demo[9], 0, np.inf), response_si, 20, 10, 1.4),
        color="C1",
        linestyle="--",
        label="GOLD Deconvolution",
    ),
]
ax.set_xlabel("Time /cells")
ax.set_ylabel("Amplitude")
ax2.set_ylabel("Amplitude")
plt.legend(handles=handles);
```

In such instances, one cannot easily determine the peak multiplicity of the sample. It is therefore assumed that the measured sample contains only one peak, which is fit as described above using an additional mask that forces the fit algorithm to ignore the saturated regions. Consequently, these fits are more prone to poor estimation of the signal amplitude where a significant portion of the signal is lost to saturation effects.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A plot of the saturated MicroMeGaS waveform sample, and the mask used for fitting.
    name: signal-saturation-mask
  image:
    align: center
    width: '512'
tags: [hide-input]
---
fig, ax = plt.subplots(sharex=True)
ax2 = ax.twinx()

mask = y_demo[9] <= 3290
handles = [
    ax.stairs(y_demo[9], color="C0", label="Signal"),
    ax2.stairs(mask, color="C1", linestyle="--", label="Saturation Mask"),
]
ax.set_xlabel("Time /cells")
ax.set_ylabel("Amplitude")
ax2.set_yticks([0, 1])
ax2.set_ylabel("Mask")
plt.legend(handles=handles);
```

## Silicon Signals

In the silicon detector, the preliminary calibration run that is analysed in {numref}`expt:silicon-calibration` was used to ensure that the dynamic range of the silicon detectors was sufficiently large during the acquisition phase of the experiment. As such, signals measured by the silicon detectors do not suffer from the saturation phenomenon described above.

Meanwhile, the response function derived in {numref}`expt:response-estimation` is, by virtue of its construction, a poor choice for (de)convolution fits of the silicon signals as the necessary source waveforms approach widths of ~1 time cell. Therefore, a simple linear transformation of the response function was used to fit silicon waveforms, which correctly recovers the peak locus and amplitude (see {numref}`signal-silicon-linear-fit`).

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A plot of silicon waveform sample, and its linear response fit.
    name: signal-silicon-linear-fit
  image:
    align: center
    width: '512'
tags: [hide-input]
---
sample_si = np.load(data_path / "sample-si.npy")
response_si = np.load(data_path / "response-si.npy")


sample = sample_si[1]

response = np.roll(response_si, 380)


def model(p):
    dt, q = p
    x = np.arange(512)
    return np.interp((x + dt), x, response, period=512) * q


def objective(p):
    dy = model(p) - sample_si
    return np.sum(dy**2)


res = minimize(objective, (300, 1000), bounds=[(0, 360), (100, np.inf)])
fig, ax = plt.subplots(sharex=True)
ax.set_ylim(0, 1250)
ax.stairs(sample_si[1], color="C0", label="Signal")
ax.stairs(model(res.x), color="C1", label="Fit", linestyle="--")
ax.set_xlabel("Time /cells")
ax.set_ylabel("Amplitude")
plt.legend();
```

+++ {"tags": ["remove-cell"]}

:::{warning}
TODO: 
- [ ] discuss current vs voltage here of preamplifier
- [ ] check whether drift of charges is significant to signal formation in presence of micromesh?
- [x] consider meaning of non linear least squares
- [x] Mention GOLD deconvolution
:::

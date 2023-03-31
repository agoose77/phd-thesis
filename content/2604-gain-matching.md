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
mystnb:
  execution_mode: "inline"
---

# Gain Matching

```{code-cell}
:tags: [remove-input, remove-output]

# Fix RC overwriting
%config InlineBackend.rc = {}

import json
import pickle
from pathlib import Path

import awkward as ak
import iminuit
import iminuit.cost
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from mplhep.styles import ATLAS

plt.style.use(ATLAS)
plt.rc("figure", figsize=(10, 5), dpi=120)

data_path = Path("data")
```

In {numref}`expt:micromegas`, it was noted that the MicroMeGaS anode is subdivided into a set of distinct zones that can be held at different potentials in order to spatially vary the gain. In this experiment, both the strip-chain (side) regions and final block of pads in the central region were held at a high gain in order to better resolve light particle tracks with low stopping powers (see {numref}`micromegas-anode-gain-region`).

+++

:::{figure} image/placeholder/micromegas-anode-zones.svg
:name: micromegas-anode-gain-region
:width: 400px
:align: center

Illustration of the significant zones within the MicroMeGaS anode segmentation. The strip-chain region (a), held at the same potential as the high-gain pads (c), is shaded in dark grey. The high-gain pads region (c) is shaded in yellow, whilst the low-gain pads (b) are coloured in light grey.
:::

+++

Following position reconstruction, these gains must be accounted for if the collected charge is to be used for particle identification. Given that the strips, chains, and final central pads were held at the same potential, the relative gain of these regions can be determined solely by looking at the relative gain of the final central pad region. This was experimentally measured by observing the change in charge collected by the rows of pads either side of the high-low gain boundary (see regions (b) and (c) of {numref}`micromegas-anode-gain-region`).

```{code-cell}
---
mystnb:
  figure:
    caption: Ratio of the mean collected charge between the low gain and high gain
      region boundary in the Micromegas pads.
    name: micromegas-anode-relative-gain
  image:
    align: center
    width: '512'
tags: [hide-input]
---
with open(data_path / "gain-hists.pickle", "rb") as f:
    gain_hists = pickle.load(f)


def pdf(x, q, mu, sigma):
    return q * stats.norm(mu, sigma).pdf(x)


def cdf(x, q, mu, sigma):
    return q * stats.norm(mu, sigma).cdf(x)


xe_last = gain_hists["last-rel"].axes[0].edges
y_last = gain_hists["last-rel"].values()

nll_last = iminuit.cost.ExtendedBinnedNLL(y_last, xe_last, cdf)

m_last = iminuit.Minuit(nll_last, q=1, sigma=0.02, mu=0.1)
m_last.limits["mu"] = (0, 1)
m_last.limits["sigma"] = (0, 1)
m_last.limits["q"] = (0, 1e6)
m_last.migrad()

P_last = cdf(xe_last, *m_last.values)

gain_hists["last-rel"].plot1d(label="Measured")
plt.plot(xe_last, np.append(np.diff(P_last), np.nan), drawstyle="steps-post", label="Fit")
plt.axvline(m_last.values["mu"], linestyle="dashed", label="$\mu$")
plt.xlabel("Relative Gain")
plt.ylabel("Counts")
plt.legend();
pass  # Required for next cell's eval
```

After fitting this distribution with a binned likelihood estimator, the relative gain between the low and high gain regions was found to be {eval}`f"{m_last.values['mu']:.3f}"` with a standard deviation of {eval}`f"{m_last.values['sigma']:.3f}"`.

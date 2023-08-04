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

(expt:texat-track-fitting)=
# Track Fitting

```{code-cell} ipython3
:tags: [hide-cell]

import pickle
from pathlib import Path

import awkward as ak
import k3d
import k3d.platonic
import mplhep as hep
import numpy as np
import vector
from IPython.display import Image
from matplotlib import pyplot as plt
from matplotlib.cm import viridis
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon
from texat.utils.awkward.convert import from_hdf5
from texat.utils.awkward.structure import ordered_map
from utils import displayed_as_mimebundle

hep.style.use(hep.style.ATLAS)
```

Tracks within the TPC volume were fit with line-interval models (see {numref}`texat:line-segment`) using the methods described in {numref}`texat:pearl-fit`. From these fits, a set of labels was generated, which permits ascribing each cluster to a given track model. {numref}`track-example-fit` shows an event that was fit according to these techniques.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: A 3D plot of the track reconstruction for a single event using the PEARL
      method described in {numref}`texat:pearl-fit`. Each distinct track is labelled
      with a distinct colour, and the line of best fit superimposed. Due to the uncertainty
      of the cluster positions in the pads region, the beam track is found to be longer
      than it is physically expected to be. This can be corrected in a subsequent
      constrained fit. The upper track corresponds to a beam-like pile-up track, whilst the 
      lower track triplet belong to a single scattering reaction.
    name: track-example-fit
  image:
    align: center
    width: 512px
tags: [hide-input]
---
cluster = from_hdf5("data/cluster-fit.h5")
track = from_hdf5("data/track-fit.h5")


def vec_to_array(vec):
    fields = ak.unzip(vec[["x", "y", "z"]])
    return ak.to_numpy(ak.concatenate([f[..., np.newaxis] for f in fields], axis=-1))


points = vec_to_array(cluster.position).astype(np.float32)
label = ak.to_numpy(cluster.label).astype(np.float32)

starts = vec_to_array(track.start)
stops = vec_to_array(track.stop)
line_points = np.concatenate((starts, stops), axis=-1).reshape(-1, 3).astype(np.float32)
line_indices = (np.arange(line_points.shape[0])).reshape(-1, 2)

color_map = np.concatenate(
    ((f := np.linspace(0, 1, 32))[:, np.newaxis], viridis(f)[:, :3]), axis=1
)

plot = k3d.plot(camera_auto_fit=False, grid_visible=False, colorbar_object_id=0)

plot += k3d.points(
    points,
    attribute=label,
    color_map=color_map,
    name="Cluster",
    point_size=2.0,
    render="3d",
)
plot += k3d.lines(
    line_points,
    attribute=(line_indices // 2).ravel(),
    color_map=color_map,
    indices=line_indices,
    indices_type="segment",
)

plot.camera = np.array(
    [
        -32.21654280817863,
        -71.44774694349248,
        101.78294988049275,
        8.25564617466183,
        -34.66977691828356,
        22.24595725375475,
        0.6849613598383177,
        0.40730740534726717,
        0.6040932071769807,
    ]
)


# Provide image fallback
with displayed_as_mimebundle() as c:
    display(
        plot,
        Image("image/sample-track-reconstruction.png"),
    )
```

## Track Multiplicity

+++

In {numref}`expt:facility-location-problem`, the PeARL method for multi-model discovery and fitting was discussed. For this experiment, a random sample of 1024 models was drawn from pairwise combinations of the clusters computed in {numref}`expt:cluster-reconstruction`. Each model comprised of a pair of clusters, with corresponding positions and charges, and assigned a characteristic width drawn from a Gaussian distribution whose width was determined by inspection. {numref}`track-multiplicity-fit` shows the track multiplicity of these fits, i.e. the number of tracks per event. Perfect scattering reactions correspond to three-track events, in which the beam, light product recoil, and heavy reactant scatter are observed. However, these events are in the minority; interactions which occur near (or before) the start of the MicroMeGaS are only partially captured by the detector; the beam track falls outside of the active region of the TPC. Similarly, the heavy product track is often too short to be identified from the resolution of the detector. As such, the majority of events are fewer-than-three-track events. Beyond-three-track events typically correspond to coherent noise, which is reconstructed as ghost tracks, or pileup, in which there are demonstrably greater than three tracks present in the event.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Histogram of the track multiplicity found during fitting of the usable
      experimental runs. A majority of events have a single track; these correspond
      to events in which the light product is not observed.
    name: track-multiplicity-fit
  image:
    align: center
    width: 512px
tags: [hide-input]
---
with open("data/track-multiplicity.pickle", "rb") as f:
    hist_mul = pickle.load(f)


hist_mul.plot();
```

These track fits are unconstrained; in the preliminary fitting procedure there is no imposition of reaction kinematics upon the result. Though it might seem prudent to pursue only those solutions which satisfy kinematic constraints, at this early juncture in the analysis there is insufficient information to introduce these constraints; in order to apply the rules of energy and momentum conservation, each track must be identified in terms of the particle kind, and the reaction to which it belongs. This requires that the fitting process be diphasic; a primary track finding routine, followed by a kinematic fitting procedure (see {numref}`expt:theory:kinematic-fitting`).

+++

## Silicon Projection

For each event, with the trigger placed upon the silicon detector channels, it follows that there should be a track associated with a low-z ion incident upon the detector. Therefore, one can establish a 2D histogram corresponding to the projection of these tracks upon the triggered silicon detector. Without any gating logic, it should follow that the these intersections agree closely to the known geometrical dimensions of each quadrant. {numref}`silicon-hitmap-forward` shows a pair of hitmaps for the forward silicon detector array. Due to the high incidence of proton tracks in the central region, it is necessary to ignore the central detectors in order to best visualise the quality of the hitmap in other regions. 

A plot of the _relative_ hitmap formed by taking the difference of the reconstructed hit position with the known silicon centroid is shown in {numref}`silicon-hitmap-forward-relative` to have good agreement with the quadrant dimensions. It is expected that the agreement will not be exact; small tracks incur a larger angular error, which manifests as significant displacements in the reconstructed hit position. In both figures, the hitmap is formed by the union of all track intersections in order to remove bias from gating the track hit position. A position gate was applied to the track endpoint; tracks whose endpoints lie within the final sector of the MicroMeGaS are likely to be the light particles that reach the silicon; the beam and scattered beam tracks are typically found earlier in the detector.


```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 2D hitmaps for the forward silicon detector array, formed by the intersection
      of reconstructed tracks, whose endpoints lie in the final sector of the MicroMeGaS,
      with the silicon plane. The hitmap for all events is shown in (a). The subset
      of hits outside the central region is plotted in (b).
    name: silicon-hitmap-forward
  image:
    align: center
    width: 512px
tags: [hide-input]
---
calibration_map_path_local = Path("data", "calibration.h5")

quadrant_table = from_hdf5(calibration_map_path_local)
quadrant_map = ordered_map(
    quadrant_table.addr.index.chan, quadrant_table[["position", "coefficient"]]
)
forward_quadrant_position = quadrant_map.value.position[
    quadrant_map.value.position.x < 160
]

vertices = (
    forward_quadrant_position[:, np.newaxis]
    + vector.zip(dict(x=[-1, -1, 1, 1], y=0, z=[-1, 1, 1, -1]))[np.newaxis, :] * 12.5
)
vert = ak.concatenate(
    (vertices.x[..., np.newaxis], vertices.z[..., np.newaxis]), axis=-1
)

with open("data/forward-hit-map.pickle", "rb") as f:
    forward_hit_map_hist = pickle.load(f)
with open("data/forward-hit-map-non-central.pickle", "rb") as f:
    forward_hit_map_non_central_hist = pickle.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
forward_hit_map_hist.plot(ax=ax1)
forward_hit_map_non_central_hist.plot(ax=ax2)

ax1.add_collection(
    PolyCollection(
        vert, edgecolors="white", facecolors="none", linestyle="--", alpha=0.2
    )
)
ax2.add_collection(
    PolyCollection(
        vert, edgecolors="white", facecolors="none", linestyle="--", alpha=0.2
    )
)
ax1.set_aspect(1)
ax1.set_title("(a)")
ax2.set_aspect(1)
ax2.set_title("(b)")
plt.axhline(0)
plt.axvline(0);
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 2D relative hitmaps for the forward silicon detector array, formed by
      the intersection of reconstructed tracks, whose endpoints lie in the final sector
      of the MicroMeGaS, with the silicon plane. The position of each reconstructed
      hit is plotted relative to the detector centroid.
    name: silicon-hitmap-forward-relative
  image:
    align: center
    width: 256px
tags: [hide-input]
---
with open("data/forward-relative-hit-map.pickle", "rb") as f:
    forward_relative_hit_map_hist = pickle.load(f)

fig, ax = plt.subplots(figsize=(7, 3))
forward_relative_hit_map_hist.plot(ax=ax)
ax.set_aspect(1)
ax.add_patch(
    Polygon(
        np.asarray([[-12.5, -12.5], [12.5, -12.5], [12.5, 12.5], [-12.5, 12.5]]),
        edgecolor="white",
        facecolor="none",
        linestyle="--",
    )
)
plt.xlim(-35, 35)
plt.ylim(-35, 35)
ax.set_aspect(1);
```

```{code-cell} ipython3

```

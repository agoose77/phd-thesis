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
---

```{code-cell} ipython3
:tags: [hide-cell]

# Fix RC overwriting
%config InlineBackend.rc = {}
import awkward as ak
import jax; jax.config.update('jax_platform_name', 'cpu')
import k3d
import k3d.platonic
import numpy as np
from IPython.display import Image
from IPython.utils.capture import capture_output
from matplotlib import pyplot as plt
from scipy.spatial import KDTree
from texat.tracking.model.interval import probability_point_line
from mplhep.styles import ATLAS
from utils import DOT

plt.style.use(ATLAS)
plt.rc("figure", figsize=(10, 5), dpi=120)

import vector
vector.register_awkward()
```

(expt:track-finding-and-fitting)=
# Track Finding and Fitting

Fundamental to the design of many particle physics experiments is the ability to detect reaction ejectiles and measure their physical properties. The considerable challenge that this poses, in even the most conventional forward-kinematics fixed-target experiments, is exacerbated in the thick-target regime described in {numref}`expt:thick-target-experiments`. In the absence of a single interaction locus, it becomes of vital importance to be able to observe the _trajectories_ of reaction products such that the underlying kinematic variables can be reconstructed. As discussed in {numref}`expt:time-projection-chambers`, the TPC detectors in which these experiments are often conducted typically incorporate a segmented readout, whereby particle trajectories are described as a set of discretised samples. The resolution of these data is usually governed by a combination of the ejectile, gas, and readout properties. 

The problems of identifying and fitting the particle trajectories recorded in such data are nominally distinct concepts, although many approaches necessarily combine the two. Track _finding_ describes the task of identifying the existence of a particle track, whilst track _fitting_ refers to the process of ascribing model variables to identified tracks subject to the parametrisation. Central to both subproblems is the importance of outlier rejection, which is often used as a metric by which to evaluate algorithm performance.

+++

## Conventional Techniques

+++

### Hough Transform

The _classical_ Hough transform is a technique for estimating the parameters and multiplicity of a model family within a dataset. In this context, a _model_ is a description of a set of data, such as a line or a plane. The Hough transform employs a scheme whereby _features_ in the dataset, i.e. points along a line, vote for models with which they are compatible (see {numref}`hough-transform-flow`). For any continuous parametrisation, a single observation is a member of an infinite set of models. In order to make this tractable, the Hough transform is conventionally performed by discretising the {math}`n`-dimensional parameter space of the model. Thereafter, for each observation, the set of compatible models can be determined from the permutations of the discrete {math}`n-1`-dimensional free parameter space.

:::{mermaid}
:caption: Flowchart detailing the classic discrete Hough transform. Once the algorithm has terminated, maxima in the voting space correspond to models (parameterisations) with high support (large numbers of votes). These maxima can be treated as candidates that well describe the data.
:name: hough-transform-flow
:align: center

graph LR;
    start[Start]
    observation[Select observation]
    parameter_2_n[Select parameters 2..n]
    compute_dependent[Compute parameter 1]
    accumulate_vote[Store vote]
    has_more_parameter_2_n{Phase-space exhausted?}
    has_more_observation{Next observation?}
    stop[Stop]
    
    start-->observation
    observation --> parameter_2_n
    parameter_2_n --> compute_dependent
    compute_dependent --> accumulate_vote
    accumulate_vote --> has_more_parameter_2_n
    has_more_parameter_2_n --> |Yes| parameter_2_n
    has_more_parameter_2_n --> |No| has_more_observation
    has_more_observation --> |Yes| stop
    has_more_observation --> |No| observation

:::

This technique introduces an explicit relationship between the precision of the identified model parameters and the robustness to noise; fine discretisations are able to accurately determine the underlying model parameters, but the introduction of noise quickly leads to the identification of multiple models. Meanwhile, coarse discretisations are far less vulnerable to over-fitting, but at a cost of poor parameter resolution. This trade-off requires the user to balance the anticipated level of noise (signal-to-noise ratio) and the similarity of observations (how close any-two separate models are in parameter space. Furthermore, the search complexity increases exponentially with the number of model parameters.

Certain procedures can be used to mitigate this compromise:
- Bin smoothing: convolving the parameter space with a smoothing kernel to reduce the significance of spurious peaks
- Secondary optimisation: by asserting that identified models are close to their "true" representations, a secondary optimiser (e.g. least squares) can be used to improve the model parameters.

+++

### RANSAC 

Random Sample Consensus (RANSAC) is a paradigm for fitting a singular model to experimental data. It recognises the model finding/fitting problem as a connected one; the challenge of identifying a unique set of models within a dataset is highly dependent upon estimating their free parameters given the observed data {cite:ps}`fischler_random_1981`.

RANSAC draws a distinction between two kinds of error: 
- _measurement_ error: deviations from the "true" values observed in measurements
- _classification_ error: gross errors that arise from misclassification of the dataset

The RANSAC procedure accounts for these two kinds of error by starting with a small, feasible, initial dataset, before enlarging this set with _consistent_ data (see {numref}`ransac-flow`). Concretely, when fitting e.g a line within a set of {math}`N` points, the RANSAC approach would be to select two points, compute origin and direction vectors, and then determine the points which lie within an acceptance window (orthogonal distance) to the model. These new _inliers_ can then be used to re-estimate the model; smoothing the measurement errors. 


:::{mermaid}
:caption: Flowchart outlining the RANSAC algorithm.
:name: ransac-flow

graph LR;
start[Start]
finish[Finish]
sample[Draw random sample]
fit[Fit model to subset]
test[Expand inliers]
refit[Fit consensus set]

loop{Drawn k trials?}
start --> sample
sample --> fit
fit --> test
test --> refit
refit --> loop
loop --> |No| sample
loop --> |yes| finish
:::

A number of parameters determine the termination of the algorithm, namely:
- the acceptance window that separates inliers from outliers
- the minimum support required to instantiate a model (the number of inliers required to consider the model _valid_)
- the number of (random) subsets to draw in the search for model candidates.

+++

The upper bound on the number of trials required to select a "good" subset from the dataset can be determined mathematically. If {math}`w` is the probability that a selected data point is within the error tolerance of a given model, then the expectation value {math}`E(K)` of the number of trials {math}`k` required to select a subset of {math}`n` points is given by
:::{math}
E(k) &= b + 2(1-b)b + 3(1-b)^2b + \dots + i(1-b)^{i-1}b\dots\,,

     &= b\bqty{1 + 2a + 3a^2 + \dots + i a^{i-1} + \dots}\,,
:::
where {math}`b=w^n` and {math}`a=(1-b)`.

It can be shown that the above simplifies to
:::{math}
E(k) = \frac{1}{b} = w^{-n}
:::
(see {cite:ps}`fischler_random_1981`).

Although there is no analytic method for determining the minimum support required to instantiate a model, there exist methods by which to determine sensible values of this parameter for a given problem.

+++

(content:sequential-ransac)=
#### Sequential RANSAC

The RANSAC algorithm is designed to find the best-fit model given a dataset. In scenarios where there may be multiple models, RANSAC must be generalised to identify a family of consensus sets. A common approach is to use _Sequential_ RANSAC, which iteratively applies the RANSAC algorithm to the dataset until no further models can be identified with sufficient support. 

The RANSAC algorithm establishes a hard distinction between inliers and outliers. An important consequence of this behaviour is that the method is hierarchical: the first "winning" model has the greatest number of data points to choose from, whilst the final model has the least. As such, for models with overlapping observations, RANSAC can perform poorly. Two instances of ideal simulated track scattering reactions are shown in {numref}`ransac-greedy-1-labels` and {numref}`ransac-greedy-2-labels`, whilst a reaction for which sequential RANSAC is ill-suited is shown in {numref}`ransac-greedy-3-labels`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of a simulated elastic scattering reaction between a
      {math}`{}^{10}\mathrm{C}` beam and a {math}`{}^{4}\mathrm{He}` gas target. The
      simulation parameters match the experimental parameters described in {numref}`experiment`.
      The simulation was performed using a heavily modified variant of TexATSim, the software
      developed by the group at Texaa A&M for TexAT reaction studies.
      The beam direction is given by the {math}`\hat{y}` axis. Three track labels
      given by sequential RANSAC are indicated by the colour map, with a fourth outlier
      label corresponding to -1. It can clearly be seen that the scattered beam (blue) labelling
      is over-supported, as it extends into the incident beam (yellow) track clusters.
    name: ransac-greedy-1-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
cm = 1
mm = 0.1 * cm


def vector_to_ndarray(vec):
    layout = ak.to_layout(vec[["x", "y", "z"]])
    if isinstance(layout, ak.record.Record):
        layout = layout.array[layout.at : layout.at + 1]
    as_numpy = ak.to_numpy(layout)
    return as_numpy.view(as_numpy.dtype[1]).reshape(-1, 3)


def show_event(
    event,
    color,
    label,
    plot=None,
    length=15,
    show_simulation=True,
    labelling=None,
    cluster_kwargs=None,
):
    if plot is None:
        plot = k3d.plot(camera_auto_fit=False)

    heavy_end = event.simulation.vertex + event.simulation.heavy * length
    light_end = event.simulation.vertex + event.simulation.light * length

    heavy_line = k3d.line(
        np.stack(
            [
                vector_to_ndarray(event.simulation.vertex),
                vector_to_ndarray(heavy_end),
            ]
        ),
        color=color,
        point_size=2,
        name=f"Heavy (sim) {label}",
    )
    heavy_line.visible = show_simulation
    plot += heavy_line

    light_line = k3d.line(
        np.stack(
            [
                vector_to_ndarray(event.simulation.vertex),
                vector_to_ndarray(light_end),
            ]
        ),
        color=color,
        point_size=2,
        name=f"Light (sim) {label}",
    )
    light_line.visible = show_simulation
    plot += light_line

    plot += k3d.points(
        vector_to_ndarray(event.reconstruction.position),
        point_size=0.25,
        name=f"Cluster {label}",
        color_map=k3d.matplotlib_color_maps.Viridis,
        render="3d",
        **(cluster_kwargs or {}),
    )

    return plot


ransac_greedy_1 = ak.from_parquet("data/1-ransac-greedy.parquet")

plot_greedy_1 = show_event(
    ransac_greedy_1,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(ransac_greedy_1["ransac"].label)},
)


plot_greedy_1.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_1, Image("image/1-ransac-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`ransac-greedy-1-labels` using sequential RANSAC. 
      Only the track direction should be considered; these fits correspond to unbounded lines. 
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. It can be seen that whilst
      the scattered beam track lies close to the simulated track, a common-vertex
      fit will pull the vertex away from its true value.
    name: ransac-greedy-1-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_1_tracks = show_event(
    ransac_greedy_1,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(ransac_greedy_1["ransac"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(ransac_greedy_1["ransac"].track):
    plot_greedy_1_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.start + track.direction * 10),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_1_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_1_tracks, Image("image/1-ransac-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of a second simulated elastic scattering reaction between a
      {math}`{}^{10}\mathrm{C}` beam and a {math}`{}^{4}\mathrm{He}` gas target. The
      simulation parameters match the experimental parameters described in {numref}`experiment`.
      The beam direction is given by the {math}`\hat{y}` axis. Three track labels
      are indicated by the colour map, with a fourth outlier label corresponding to -1. Like
      {numref}`ransac-greedy-1-labels`, the RANSAC fit is greedy, but in this figure
      it can be seen that the indicent beam (purple) is over-supported and extends
      into the scattered beam (yellow) track clusters.
    name: ransac-greedy-2-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
ransac_greedy_2 = ak.from_parquet("data/2-ransac-greedy.parquet")

plot_greedy_2 = show_event(
    ransac_greedy_2,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(ransac_greedy_2["ransac"].label)},
)


plot_greedy_2.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_2, Image("image/2-ransac-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`ransac-greedy-2-labels` using sequential RANSAC. 
      Only the track direction should be considered; these fits correspond to unbounded lines. 
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. Like {numref}`ransac-greedy-1-tracks`,
      it can be seen that whilst the scattered beam track lies close to the simulated
      track, a common-vertex fit will pull the vertex away from its true value.
    name: ransac-greedy-2-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_2_tracks = show_event(
    ransac_greedy_2,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(ransac_greedy_2["ransac"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(ransac_greedy_2["ransac"].track):
    plot_greedy_2_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.start + track.direction * 10),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_2_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_2_tracks, Image("image/2-ransac-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of a third simulated elastic scattering reaction between a
      {math}`{}^{10}\mathrm{C}` beam and a {math}`{}^{4}\mathrm{He}` gas target. The
      simulation parameters match the experimental parameters described in {numref}`experiment`.
      The beam direction is given by the {math}`\hat{y}` axis. Three track labels
      are indicated by the colour map, with a fourth outlier label corresponding to -1. Whilst
      the correct number of active tracks (3) have been identified, it can be seen
      that the light-product track (blue) extends far into the incident beam clusters
      (green), and the incident beam clusters extend into the scattered beam region
      (yellow). The beam track is thus discontinuous.
    name: ransac-greedy-3-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
ransac_greedy_3 = ak.from_parquet("data/3-ransac-greedy.parquet")

plot_greedy_3 = show_event(
    ransac_greedy_3,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(ransac_greedy_3["ransac"].label)},
)


plot_greedy_3.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_3, Image("image/3-ransac-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`ransac-greedy-3-labels` using sequential RANSAC. 
      Only the track direction should be considered; these fits correspond to unbounded lines. 
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. It can be seen that the poor labelling
      shown in {numref}`ransac-greedy-3-labels` produces a poor fit, with the reconstructed
      vertex (given by the intersection of the blue scattered and heavy beam tracks)
      displaced outside the measured clusters.
    name: ransac-greedy-3-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_3_tracks = show_event(
    ransac_greedy_3,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(ransac_greedy_3["ransac"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(ransac_greedy_3["ransac"].track):
    plot_greedy_3_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.start + track.direction * 10),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_3_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_3_tracks, Image("image/3-ransac-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

(expt:facility-location-problem)=
## Facility Location Problem
The previously explored methods of the Hough transform and RANSAC are both _greedy_ methods; the order in which solutions are generated favours those models which are found first. The consequence of greedy optimisation is that the global solution across several models may not be optimal.

In order to obtain a _global_ solution to track labelling, the task must be reframed as a global optimisation problem. 
The facility location problem (FLP) is an optimisation problem whose solution determines the optimal location for a set of facilities such that the transportation costs for each facility are minimised. There are several formulations of the problem with auxillary constraints, such as the _capacity_ of the facilities, or the addition of an _opening cost_ for each facility. 

The significance of "facility" and "transportation cost" depends upon the framing of the problem. Here, the _uncapacitated facility location problem_ (UFLP) will be explored in the context of particle track labelling.

### Uncapacitated Facility Location Problem
The uncapacitated facility location problem is a variant of the FLP in which each facility has an unlimited capacity and an associated opening cost. In prose, the problem may be defined by three requirements:
- A manufacturing company wants to minimise costs.
- Delivery is expensive, so facilities need to be close to consumers.
- Facilities are also expensive, so as few as possible should be opened.

The solution to this problem is given by the minimisation of the following cost function: 
:::{math}
:label: uflp-cost-function
E(F) = \sum_{f \in F} \left( O_f + \sum_{c \in C} T_{fc} D_{fc} \right)\,,
:::
where 
- {math}`F` is the set of open facilities.
- {math}`O_f` is the cost of opening facility {math}`f`.
- {math}`T_{fc}` is the cost of transporting goods between facility {math}`f` and consumer {math}`c`.
- {math}`D_{fc}` is the demand of consumer {math}`c` satisfied by facility {math}`f`.


In the domain of track labelling, the terms "facility", "distance", and "consumer", acquire new meaning:
```{list-table} Terms corresponding to the FLP interpretation of track labelling.
:name: flp-labelling-terms
:header-rows: 1

* - Term
  - Interpretation
* - Facility
  - A hypothetical track model
* - Consumer
  - An observation that belongs to an unknown track model
* - Transport cost
  - The goodness-of-fit for an observation given a particular track model
```

Meanwhile, the consumer demand {math}`D_{fc}` is simply the delta function of the labelling {math}`\delta_{ff(c)}`, i.e. a single observation {math}`c` is served by exactly one facility {math}`f(c)`. See {numref}`track-model-illustration` for an illustration of these components.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: An illustration of a 2D track described by a proposed track model.
    name: track-model-illustration
  image:
    align: center
    width: 512px
tags: [hide-input]
---
plt.figure()

n = 100

t = np.random.uniform(high=10.0, size=n)
w = np.random.normal(scale=0.15, size=n)
R = np.stack((w, t), axis=1)

x = np.radians(60)
M = np.sin([[np.pi / 2 - x, -x], [x, np.pi / 2 - x]])
S = R @ M

# Draw scatter
plt.scatter(S[:, 0], S[:, 1], s=3, label="Observation (consumer)")

# Draw model
Q = np.r_[5, 5]
plt.plot([0, Q[0]], [0, Q[1]], color="C1", label="Track Model (facility)")

# Random midpoint
i_midpoint = np.argmin(np.abs(S[:, 0] - 4.5))
P = S[i_midpoint]
plt.scatter(P[0], P[1], marker="+", color="C3")

# Intersection
tau = ((P - [0, 0]) @ Q) / (Q @ Q)
H = tau * Q

# Draw tangent
plt.plot(
    [P[0], H[0]],
    [P[1], H[1]],
    color="C3",
    linestyle="--",
    label="Residual (transport cost)",
)

plt.gca().set_aspect(1)
width = 13.5
plt.xlim(-5 + 4, -5 + 4 + width)
plt.ylim(-0.5, -0.5 + width / 2)
plt.tick_params(
    axis="both",
    which="both",
    left=False,
    bottom=False,
    top=False,
    right=False,
    labelbottom=False,
    labelleft=False,
)
plt.legend();
```

The probability of observing set {math}`C` of observations for facility $f$ is the product of the probabilities of observing each $c$, i.e. 
:::{math}
P(f \mid C) = \prod_c{P(f \mid c)}\,.
:::
If the per-consumer transport cost is given as a log-likelihood, then it follows that the sum over the transport costs for each facility is equivalent to the log-likelihood of the facility given {math}`C`:
:::{math}
:label: log-likelihood-sum

\sum_c{\ln\left({P(f \mid c)}\right)} 
&= \ln\left({\prod_c{P(f \mid c)}}\right)

&= \ln\left(P(f \mid C)\right)\,.
:::

+++

### Metric Labelling Problem

The trivial form of {eq}`uflp-cost-function`, in which the facility cost {math}`O_f` is zero
:::{math}
:label: cost-function-trivial
E(F) = \sum_{f \in F,\,c \in C} T_{fc} D_{fc}\,,
:::
is ill-posed. A _well-posed_ problem is guaranteed to have a _unique_ solution that depends continuously on the input data {cite:ps}`hadamard`.

In order to solve {eq}`cost-function-trivial`, the set of admissible solutions must be restricted by the introduction of _a priori_ knowledge, i.e. the problem must be _regularised_. The label cost term given in {eq}`uflp-cost-function` is one such regulariser which imposes a preference for solutions with fewer labels.

A common feature of the labelling problem (of which the track labelling problem is a derivative) is that coherent groups of observations are typically known _a priori_ to be positively correlated. 

This behaviour can be accounted for by an additional regulariser in the energy function
:::{math}
:label: cost-smoothness
\sum_{cc'\in C}V_{f(c),f(c')}(c, c')\,,
:::
where {math}`V_{f(c),f(c')}(c, c')` is the pairwise prior that penalises {math}`f(c) \neq f(c')`, such that
:::{math}
:label: cost-function-pearl
E(F) = 
\underbrace{\sum_{f \in F} O_f}_{\text{label cost}} + 
\underbrace{\sum_{f \in F,\,c \in C} T_{fc} D_{fc}}_{\text{data cost}} + 
\underbrace{\sum_{cc'\in C}V_{f(c),f(c')}(c, c')}_{\text{smooth cost}}\,.
:::

A two dimensional model potential is shown in {numref}`smoothness-labelling-illustration`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Illustration of a 2D smoothness prior between two labellings. The highest
      costs are observed between unalike labels at small distances.
    name: smoothness-labelling-illustration
  image:
    align: center
    width: 512px
tags: [hide-input]
---
plt.figure()
tree = KDTree(S)

model = np.random.choice([1, 2], size=len(S))

pairs = tree.query_pairs(0.3, output_type="ndarray")
pair_costs = np.where(
    model[pairs[:, 0]] != model[pairs[:, 1]],
    np.sum((pairs[:, 0] - pairs[:, 1]) ** 2),
    0.0,
)

cost = np.zeros(len(S))
np.add.at(cost, pairs[:, 0], pair_costs)
np.add.at(cost, pairs[:, 1], pair_costs)


colors = np.array(plt.rcParams["axes.prop_cycle"].by_key()["color"])

# Draw scatter
plt.scatter(
    S[model == 1, 0],
    S[model == 1, 1],
    c=cost[model == 1],
    s=20,
    label="Model 1",
    marker="o",
)
plt.scatter(
    S[model == 2, 0],
    S[model == 2, 1],
    c=cost[model == 2],
    s=20,
    label="Model 2",
    marker="^",
)

plt.gca().set_aspect(1)
colorbar = plt.colorbar(orientation="horizontal", fraction=0.08)
colorbar.ax.set_title("Potential")
colorbar.ax.tick_params(
    axis="both",
    which="both",
    left=False,
    bottom=False,
    top=False,
    right=False,
    labelbottom=False,
    labelleft=False,
    labelright=False,
    labeltop=False,
)
plt.xlim(0, 8)
plt.ylim(0, 4)
plt.tick_params(
    axis="both",
    which="both",
    left=False,
    bottom=False,
    top=False,
    right=False,
    labelbottom=False,
    labelleft=False,
)
plt.legend(loc="lower right");
```

Clearly, the _label cost_ leads to minimisation of the model count, whilst the _smooth cost_ leads to the preference of spatially coherent labellings. As before, the _data cost_ prefers models which are well-described by their inliers.

<!-- 
:::{admonition} To Do
:class: margin

Mention constraints on potential (see [https://profs.etsmtl.ca/hlombaert/energy/#SECTION00010000000000000000](https://profs.etsmtl.ca/hlombaert/energy/#SECTION00010000000000000000))
:::
 -->

+++

### Graph Cut Optimisation

In the absence of smooth costs, the UFLP can be solved by integer programming techniques, but remains NP-hard {cite:ps}`Cheriyan98approximationalgorithms`. There exists an heuristic method which solves {eq}`uflp-cost-function` in {math}`O(\lvert F\rvert^2 \lvert C \rvert)` time {cite:ps}`kuehn_heuristic_1963`, where {math}`O(n)` represents an asymptotic time complexity that is linear in {math}`n`. Meanwhile, the task of minimising {eq}`cost-function-pearl` is also NP-hard for {math}`\lvert F \rvert \geq 3` {cite:ps}`boykov_fast_2001-1`, but there exist approximate solutions using _graph cuts_ that are guaranteed to find the local minima within a fixed bound of the global optimum {cite:ps}`delong_fast_2010`.

::::{admonition} NP-hardness
:class: dropdown

In computational complexity theory, _P_ problems are those problems of size {math}`n` for which the time {math}`T(n)` to determine their solutions is upper bounded by a polynomial in {math}`n`, i.e. {math}`T(n)=\mathcal{O}(n^k)`

_NP_ problems are those which cannot be _solved_ but can be _verified_ in polynomial time.

_NP-complete_ problems are NP problems to which all other NP problems can be reduced in polynomial time.

_NP-hard_ problems are _at least_ as complex as NP-complete problems, i.e. there must exist an NP-complete problem that can be transformed in polynomial time to an NP-hard problem.

:::{figure} https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/P_np_np-complete_np-hard.svg/640px-P_np_np-complete_np-hard.svg.png
:name: p-np-complete
:width: 512px
:align: center

Diagram illustrating the relationship between P, NP, NP-complete, and NP-hard problems under the assumptions of {math}`P=NP` and {math}`P\neq NP`. Figure by Behnam Esfahbod, distributed under a [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/deed.en) license.
:::

::::

+++

#### Graph Cuts

+++

One family of approximations to the solution of {eq}`cost-function-pearl` are based upon the method of _graph cuts_. Here, the fundamentals of the {math}`\alpha`-expansion method will be discussed, with the treatment of label costs and {math}`\alpha\beta`-swap moves omitted for brevity.

Without label costs, {eq}`cost-function-pearl` becomes
:::{math}
:label: cost-function-graph
E(F) = 
\underbrace{\sum_{f \in F,\,c \in C} T_{fc} D_{fc}}_{\text{data cost}} + 
\underbrace{\sum_{cc'\in C}V_{f(c),f(c')}(c, c')}_{\text{smooth cost}}\,.
:::

A _graph_ {math}`\mathcal{G}(\mathcal{V}, \mathcal{E})` is fundamentally a set of vertices {math}`\mathcal{V}` and a set of pairwise edges {math}`\mathcal{E}` between them. Each edge may have an associated weight, and may further be directed such that {math}`A\rightarrow B` is distinct from {math}`A \leftarrow B`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Simple two-vertex graph.
    name: simple-graph
  image:
    align: center
    width: 128px
tags: [hide-input]
---
DOT(
    """
    digraph my_graph {
        {rank = same; "u"; "v"}
        "u" [shape=circle];
        "v" [shape=circle];
        u -> v [label=10]
    }
    """
)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Simple two-vertex graph with terminals {math}`s`, {math}`t`. The maximum
      flow between the terminals is 10.
    name: simple-graph-terminals
  image:
    align: center
    width: 256px
tags: [hide-input]
---
DOT(
    """
digraph my_graph {
    rankdir=LR;
    {rank = same; "u"; "v"}
    "s" [shape=square color=orange fontcolor=orange];
    "t" [shape=square color=blue fontcolor=blue];
    "u" [shape=circle];
    "v" [shape=circle];
    s -> u [label=7];
    s -> v [label=3];
    u -> t [label=2];
    v -> t [label=8];
    u -> v [label=5]
}
"""
)
```

A _cut_ {math}`\mathcal{C} \subset \mathcal{E}` is a set of edges which partitions the graph into two disjoint subsets, separating the terminals. Importantly, the _cost_ {math}`\lvert \mathcal{C} \rvert` equals the sum of the edge weights. Furthermore, no proper subset of {math}`\mathcal{C}` may also be a cut.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Simple two-vertex graph with terminals {math}`s`, {math}`t`. A valid
      cut is indicated by dotted lines.
    name: simple-graph-cut
  image:
    align: center
    width: 256px
tags: [hide-input]
---
DOT(
    """
digraph my_graph {
    rankdir=LR;
    {rank = same; "u"; "v"}
    "s" [shape=square color=orange fontcolor=orange];
    "t" [shape=square color=blue fontcolor=blue];
    "u" [shape=circle];
    "v" [shape=circle];
    s -> u [label=7];
    s -> v [label=3 style=dotted];
    u -> t [label=2 style=dotted];
    v -> t [label=8];
    u -> v [label=5 style=dotted]
}
"""
)
```

Under the _min-cut max-flow_ theorem , the _minimum_-cut {math}`\mathcal{C}^\star` (cut for which {math}`\lvert \mathcal{C} \rvert` is minimal) is equivalent to the maximum-_flow_, which can be computed in an efficient manner {cite:ps}`ford_maximal_1956` {cite:ps}`kolmogorov_what_2004`.

+++

(expt:alpha-expansion)=
#### Alpha Expansion
The {math}`\alpha`-expansion algorithm is a method of finding the labelling {math}`F` such that the potential {eq}`cost-function-graph` is minimised. It has been extended to solve {eq}`cost-function-pearl` through the treatment of label costs. The method is based upon the observation that, if {eq}`cost-function-graph` is encoded in terms of a particular graph construction {math}`G_{\alpha}`, the minimum cut corresponds to the optimal (local) labelling. The choice of this graph, and the mechanism by which the optimal labelling is determined by the minimum cut, will be outlined briefly below.

+++

Consider an example comprised of two nodes (observations) {math}`\Omega` and {math}`A`. One can introduce two labels: {math}`\alpha` and {math}`\omega`. The true labelling is given in {numref}`expansion-example-true-labelling`: the {math}`\Omega` is labelled by {math}`\omega`, and {math}`A` is labelled by {math}`\alpha`.

:::{list-table} Lowest cost (correct) labelling for a two-node system
:name: expansion-example-true-labelling
:header-rows: 1

* - Node
  - Label
* - {math}`A`
  - {math}`\alpha`
* - {math}`\Omega`
  - {math}`\omega`
:::

+++

The optimal labelling given in ({numref}`expansion-example-true-labelling`) should have a cost that evaluates to

+++

:::{math}
:label: expansion-minimum-cut-cost
E(F) = D(A\cdot \alpha) + D(\Omega \cdot \omega) + V(\Omega \cdot \omega,A\cdot \alpha)\,,
:::
i.e. the sum of 
- the data cost for {math}`A` under the {math}`\alpha` model
- the data cost for {math}`\Omega` under the {math}`\omega` model
- the smoothness cost between {math}`\Omega` under the {math}`\omega` model, and {math}`A` under the {math}`\alpha` model.

The graph for this two-node system whose minimum cut yields {eq}`expansion-minimum-cut-cost` is shown in {numref}`graph-expansion-ocean-cut`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Graph representing a two-node system whose optimal labelling is given
      in {numref}`expansion-example-true-labelling`. By choosing appropriate edge
      weights, the cost of the minimum cut is equal to the optimal labelling cost
      given in {eq}`expansion-minimum-cut-cost`. Cut links are indicated with dotted
      lines. Smoothness costs that penalise localised discontinuities in the labelling
      are introduced through the addition _auxillary nodes_ at label boundaries, i.e.
      the {math}`\star` node between {math}`\Omega` and {math}`A`. The edges between
      these auxiliary nodes and their neighbours encode the smoothness penalty.
    name: graph-expansion-ocean-cut
  image:
    align: center
    width: 512px
tags: [hide-input]
---
DOT(
    """
graph min_cut_example {
    rankdir=LR;
    {rank = same; "A"; "★"; "Ω"}
    "α" [shape=square color=orange];
    "ω" [shape=square color=grey];
    "Ω" [shape=circle];
    "A" [shape=circle];
    "★" [shape=doublecircle];
    "α" -- "Ω";
    "Ω" -- "ω" [label="D(Ω·ω)" style=dotted];
    "α" -- "A" [label="D(A·α)" style=dotted];
    "A" -- "ω";
    "★" -- "A";
    "Ω" -- "★" [label="V(Ω·ω,A·α)" style=dotted];
    "★" -- "ω";
}
"""
)
```

Clearly, the cut illustrated in {numref}`graph-expansion-ocean-cut` yields the optimal cost. However, how does this cut invoke a (new) labelling? One implication of the property 
> no proper subset of {math}`\mathcal{C}` may also be a cut

is that exactly _one_ edge between the terminals ({math}`\{\,\omega, \alpha\,\}`) and any node can be cut {cite:ps}`boykov_fast_2001-1`. This naturally defines a correspondence between a cut and a labelling: the cutting of a terminal edge assigns the corresponding label to the node. In this case, there is a cut through {math}`\alpha-A` and {math}`\omega-\Omega`, which assigns label {math}`\alpha` to {math}`A` and {math}`\Omega` to {math}`\omega` respectively.

+++

Although it is already known that this labelling is the correct (optimal) one, in general one might not have this prior information. The _expansion-move_ algorithm can be used to find an improved labelling {math}`F^\prime_\alpha` through the expansion of a particular label {math}`\alpha`. If the expansion does not modify the labelling, then it is optimal i.e. the current labelling {math}`F` is a (local) minimum. The _expansion_ of a label {math}`\alpha` refers to an equivalence class of cuts that preserve the edges between the alternate label and each node. For the two-node system shown in {numref}`graph-expansion-ocean-cut`, the _expansion_ property of the expansion-move algorithm is introduced by setting the cost of the edges between the terminal {math}`\omega` and the nodes {math}`A`, {math}`\Omega` to infinity. Edges with infinite costs will belong to any minimum cut, ensuring that the {math}`\omega` label does not grow (see {numref}`graph-expansion-optimal-cut`).

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: Variation of {numref}`graph-expansion-ocean-cut` depicting a two-node
      system whose labelling is already optimal. As such, the weight between {math}`A`
      and the terminal {math}`\omega` is set to infinity, so that the {math}`\omega`
      label does not grow i.e. the {math}`\alpha` label does not shrink.
    name: graph-expansion-optimal-cut
  image:
    align: center
    width: 512px
tags: [hide-input]
---
DOT(
    """
graph min_cut_expansion {
    rankdir=LR;
    {rank = same; "A"; "★"; "Ω"}
    "α" [shape=square color=orange];
    "ω" [shape=square color=grey];
    "Ω" [shape=circle];
    "A" [shape=circle];
    "★" [shape=doublecircle];
    "α" -- "Ω";
    "Ω" -- "ω" [label="D(Ω·ω)" style=dotted];
    "α" -- "A" [label="D(A·α)" style=dotted];
    "A" -- "ω" [xlabel="∞" color=red fontcolor=red];
    "★" -- "A";
    "Ω" -- "★" [label="V(Ω·ω,A·α)" style=dotted];
    "★" -- "ω";
}
"""
)
```

This simple model only considers two labels ({math}`\lvert F \rvert = 2`), whilst in practice {math}`\lvert F \rvert \gg 2`. To generalise the expansion of label {math}`\alpha` to {math}`\lvert F \rvert > 2`, {math}`\omega` can be replaced with a _meta_ label {math}`\overline{\alpha}` that represents not-{math}`\alpha`. Thereafter, the procedure remains identical. In order to determine the optimum expansion-move, this procedure must be repeated for each label.

+++

The {math}`\alpha`-expansion algorithm is therefore

1. Build a graph {math}`\mathcal{G}_\alpha(\mathcal{V}_\alpha, \mathcal{E}_\alpha)` composed of a set of vertices {math}`\mathcal{V}_\alpha` and a set of pairwise edges {math}`\mathcal{E}_\alpha`. 
2. Add a pair of additional _terminal_ vertices {math}`\alpha` and {math}`\overline{\alpha}` that represent the {math}`\alpha` label and the set of complement labels {math}`\overline{\alpha}=F - \{\,\alpha\,\}`.
3. Establish a _weight_ for each edge in {math}`\mathcal{E}_\alpha`.
4. Determine the minimum cut of {math}`\mathcal{G}(\mathcal{V}, \mathcal{E})` to propose a new labelling.
5. Accept the new labelling if the cost of the cut, which is equivalent to {eq}`cost-function-graph`, is lower than the existing solution.
6. Go to 1. for the next label.

+++

The choice of weights is the fundamental mechanism by which the expansion-move algorithm operates. The rules for finding these values are given in {cite:ps}`delong_fast_2010`. In addition, it can be shown that this algorithm can be generalised to account for label costs in order to solve {eq}`cost-function-pearl` {cite:ps}`delong_fast_2010`.

+++

A condition of the {math}`\alpha`-expansion method is that the interaction potential between labels be _metric_, i.e. it must satisfy {cite:ps}`boykov_fast_2001-1`

:::{math}
V_{\alpha, \beta} &\leq V_{\alpha, \gamma} + V_{\gamma, \beta}

V_{\alpha, \beta} &= V_{\beta, \alpha} \geq 0\,.
:::

The choice of a {math}`V_{\alpha, \gamma}=\delta_{\alpha\gamma}` interaction potential (the Potts model) combined with a geometric distance meets this requirement {cite:ps}`isack_energy-based_2012`.

+++

(texat:pearl-fit)=
### PeARL

So far, the application of graph-cuts to solving the metric labelling problem has been explored. It is not immediately obvious how this approach maps onto the problem of track fitting. At first glance, the model {math}`f` seen in {eq}`cost-function-pearl` resembles the label described in {numref}`expt:alpha-expansion`. However, our track models are members of {math}`\mathcal{L}=\mathbb{R}^n`, and therefore a one-to-one mapping between {math}`F` and {math}`\mathcal{L}` would be infinitely large. In order to explore the continuum of model parameters whilst working within a feasible subset of the parameter space, the PeARL algorithm may be used {cite:ps}`boykov_fast_2001-1`.

+++

:::{mermaid}
:caption: Process diagram of the PeARL algorithm
:name: pearl-algorithm

graph LR
    propose["(1) Propose labelling F"]
    expand["(2) Expand labelling F to F'"]
    reestimate["(3) Re-estimate models"]
    propose --> expand
    expand --> reestimate
    reestimate --> expand
:::

+++

A process diagram for the PeARL algorithm is shown in {numref}`pearl-algorithm`, and is comprised of the following steps:

1. *Propose* an initial set of models {math}`\mathcal{L}_0` by random sampling from a set of observations
2. Compute the optimal labelling {math}`F_t` from {math}`\mathcal{L}_t` by *expanding* each label {math}`f \in F`
3. *Re-estimate* the model parameters of {math}`\mathcal{L}_t` using {math}`F_t` to find {math}`\mathcal{L}_{t+1}`; go to (2.)

+++

The proposal step (1) of the PeARL algorithm closely resembles that of RANSAC. Unlike RANSAC, however, PeARL evaluates these proposals against a single optimisation objective, rather than hierarchically.

+++

### Track Fitting

#### Unbounded Line
Conventional track fitting approaches often model a track as an unbounded line in three dimensional space. Such a model has an non-normalisable probability density; naturally over an infinite interval, the probability of observing any particular value approaches 0. As such, it is not appropriate (or indeed possible) to use the log-likelihood in {eq}`log-likelihood-sum` to describe the data cost required by {eq}`cost-function-pearl`. Instead, a simple orthogonal displacement cost function, analogous to the total least-squares cost function, can be used
:::{math}
T_{fc} = k\frac{\norm{\left(\vec{r}(c) - \vec{o}(f)\right)\wedge \hat{\vec{n}}(f)}^2}{\sigma(f)^2}\,,
:::
where {math}`\vec{r}(c)` is the position of observation {math}`c`, {math}`\vec{o}(f)` a point belonging to model {math}`f`, {math}`\hat{\vec{n}}(f)` the direction of model {math}`f`, {math}`\sigma(f)` the width of the transverse distribution, and {math}`k` a scaling factor. This corresponds to the residual shown in {numref}`track-model-illustration`. 

The unbounded line may not be the most suitable model to describe linear data. Crucially, it has no concept of regularity; there is no parameterisation by which to describe the distribution along the linear axis.

+++

(texat:line-segment)=
#### Line Segment
Another model applicable to track fitting is to treat a set of observations as a line _interval_. 
With a finite length, the model has a normalisable probability density, and as such the log likelihood can be used to determine the data cost.

A curve can be defined as an infinite sum of point distributions, where the probability {math}`p(\va{r})` of observing {math}`\va{r}` is
:::{math}
:label: p-point-curve

p(\va{r}) = \int_L f(\va{r};\va*{\mu}(t) ,\va*{\Sigma})\dd{t}\,.
:::
The PDF for a non-degenerate multivariate normal distribution is
:::{math}
:label: pdf-multivariate-point

{ f(\va{r})={\frac {\exp \left(-{\frac {1}{2}}({\va {r} }-{\va*{\mu }})^{\mathrm {T} }{\va*{\Sigma }}^{-1}({\va {r} }-{\va*{\mu }})\right)}{\sqrt {(2\pi )^{k} \abs{{\va*{\Sigma }}} }}}}\,,
:::

for $\va{r}\in\mathbb{R}^k$, where ${\va*{\Sigma }}$ is a symmetric matrix. For a line interval of normally distributed points, bounded between {math}`t\in [0, 1]`, {eq}`p-point-curve` expands to 

:::{math}
:label: p-point-multivariate-line

p(\va{r}) = \int_0^1{{\frac {\exp \left(-{\frac {1}{2}}({\va {r} }-\va*{\mu}(t))^{\mathrm {T} }{\va*{\Sigma }}^{-1}({\va {r} }-\va*{\mu}(t))\right)}{\sqrt {(2\pi )^{k} \abs{{\va *{\Sigma }}}}}}\dd{t}}\,.
:::

+++

With considerations for symmetry, it can be shown that the log of the integral in {eq}`p-point-multivariate-line` reduces to
:::{math}
:label: p-point-line-solution

p(\va{r}) = \underbrace{\log\pqty{\frac{1}{4\pi L\sigma^2}}}_{\text{length penalty}} +
            \underbrace{\log\left(\operatorname{erfc} \bqty{\frac{1}{\sqrt{2}\sigma}\pqty{\abs{\Delta\va{r}\cdot \vu{n} - \frac{L}{2}} - \frac{L}{2}}}\right)}_{\text{end-point penalty}} +
            \underbrace{\frac{1}{2\sigma^2}\bqty{\pqty{\Delta\va{r}\cdot \vu{n}}^2 - \Delta\va{r}\cdot\Delta\va{r}}}_{\text{orthogonal distance penalty}}\,,
:::
where {math}`L` is the length of the line, {math}`\vu{n}` is the unit direction of the line, and {math}`\Delta\va{r}` the relative position of {math}`\va{r}` with respect to the line origin.

+++ {"tags": ["appendix"]}

::::{admonition} Derivation of {eq}`p-point-line-solution`
:class: dropdown

Consider the expanded integral:
:::{math}
\begin{aligned}
p(\mathbf{r}) 
    &= \left(\frac{1}{\sigma\sqrt{2\pi}}\right)^3 
        \int_0^1 {
        \exp\!\left[{-\frac{\left(x - \left(a_x + (b_x-a_x)t\right)\right)^2}{2\sigma^2}}\right]
        \exp\!\left[{-\frac{\left(y - \left(a_y + (b_y-a_y)t\right)\right)^2}{2\sigma^2}}\right]
        \exp\!\left[{-\frac{\left(z - \left(a_z + (b_z-a_z)t\right)\right)^2}{2\sigma^2}}\right]
        }\,dt\\
    &= \left(\frac{1}{\sigma\sqrt{2\pi}}\right)^3 
        \int_0^1 {
        \exp\!\left[{-\frac{\left(d_x - n_xLt\right)^2}{2\sigma^2}}\right]
        \exp\!\left[{-\frac{\left(d_y - n_yLt\right)^2}{2\sigma^2}}\right]
        \exp\!\left[{-\frac{\left(d_z - n_zLt\right)^2}{2\sigma^2}}\right]
        }\,dt\,.\\
\end{aligned}
:::

First, let's define our integrand, and simplify the arguments according to

:::{math}
\begin{matrix}
a = \frac{d_x}{\sqrt{2}\sigma} &
A = \frac{n_xL}{\sqrt{2}\sigma} \\
b = \frac{d_y}{\sqrt{2}\sigma} &
B = \frac{n_yL}{\sqrt{2}\sigma} \\
c = \frac{d_z}{\sqrt{2}\sigma} &
C = \frac{n_zL}{\sqrt{2}\sigma} \\
\end{matrix}
:::

Wolfram gives the solution as 
:::{math}
\frac{\sqrt{\pi} \left(\operatorname{erf}{\left(\frac{A a + B b + C c}{\sqrt{A^{2} + B^{2} + C^{2}}} \right)} + \operatorname{erf}{\left(\frac{A^{2} - A a + B^{2} - B b + C^{2} - C c}{\sqrt{A^{2} + B^{2} + C^{2}}} \right)}\right) e^{- a^{2} - b^{2} - c^{2} + \frac{\left(A a + B b + C c\right)^{2}}{A^{2} + B^{2} + C^{2}}}}{2 \sqrt{A^{2} + B^{2} + C^{2}}}\,.
:::

Now, we must restore our original parameters,
:::{math}
\begin{matrix}
a = \frac{d_x}{\sqrt{2}\sigma} &
A = \frac{n_xL}{\sqrt{2}\sigma} \\
b = \frac{d_y}{\sqrt{2}\sigma} &
B = \frac{n_yL}{\sqrt{2}\sigma} \\
c = \frac{d_z}{\sqrt{2}\sigma} &
C = \frac{n_zL}{\sqrt{2}\sigma} \\
\end{matrix}
:::

which gives
:::{math}
\frac{\sqrt{2} \sqrt{\pi} \sigma \left(\operatorname{erf}{\left(\frac{\sqrt{2} \left(d_{x} n_{x} + d_{y} n_{y} + d_{z} n_{z}\right)}{2 \sigma \sqrt{n_{x}^{2} + n_{y}^{2} + n_{z}^{2}}} \right)} + \operatorname{erf}{\left(\frac{\sqrt{2} \left(L n_{x}^{2} + L n_{y}^{2} + L n_{z}^{2} - d_{x} n_{x} - d_{y} n_{y} - d_{z} n_{z}\right)}{2 \sigma \sqrt{n_{x}^{2} + n_{y}^{2} + n_{z}^{2}}} \right)}\right) e^{\frac{- \left(d_{x}^{2} + d_{y}^{2} + d_{z}^{2}\right) \left(n_{x}^{2} + n_{y}^{2} + n_{z}^{2}\right) + \left(d_{x} n_{x} + d_{y} n_{y} + d_{z} n_{z}\right)^{2}}{2 \sigma^{2} \left(n_{x}^{2} + n_{y}^{2} + n_{z}^{2}\right)}}}{2 L \sqrt{n_{x}^{2} + n_{y}^{2} + n_{z}^{2}}}
:::

We know that {math}`\lvert{n}\rvert=1`, so let's restore the factored coefficient, and apply this simplification:

:::{math}
\frac{\left(\operatorname{erf}{\left(\frac{\sqrt{2} \left(d_{x} n_{x} + d_{y} n_{y} + d_{z} n_{z}\right)}{2 \sigma} \right)} + \operatorname{erf}{\left(\frac{\sqrt{2} \left(L n_{x}^{2} + L n_{y}^{2} + L n_{z}^{2} - d_{x} n_{x} - d_{y} n_{y} - d_{z} n_{z}\right)}{2 \sigma} \right)}\right) e^{\frac{- d_{x}^{2} - d_{y}^{2} - d_{z}^{2} + \left(d_{x} n_{x} + d_{y} n_{y} + d_{z} n_{z}\right)^{2}}{2 \sigma^{2}}}}{4 \pi L \sigma^{2}}
:::

Then we can simplify with known geometric identities

:::{math}
\frac{\left(\operatorname{erf}{\left(\frac{\sqrt{2} d_{dot n}}{2 \sigma} \right)} + \operatorname{erf}{\left(\frac{\sqrt{2} \left(L - d_{dot n}\right)}{2 \sigma} \right)}\right) e^{\frac{d_{dot n}^{2} - d_{mag2}}{2 \sigma^{2}}}}{4 \pi L \sigma^{2}}
:::
::::

+++

A visualisation of this likelihood function can be see in {numref}`volume-likelihood-interval`.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D volume plot of the likelihood function for a point described by a
      line interval between {math}`\pmqty{4 & 4 & 4}` and {math}`\pmqty{16 & 16 &
      16}` with {math}`\sigma = 1.0`.
    name: volume-likelihood-interval
  image:
    align: center
    width: '512'
tags: [hide-input]
---
X, Y, Z = np.mgrid[0:20:100j, 0:20:100j, 0:20:100j]
R = np.stack((X, Y, Z), axis=-1)
cost_1 = probability_point_line(R, np.r_[4, 4, 4], np.r_[16, 16, 16], sigma=1.0)

figure = k3d.plot(camera_auto_fit=False, grid_auto_fit=False, grid_visible=False)
figure += k3d.volume(
    cost_1.astype(np.float32), color_map=k3d.matplotlib_color_maps.Viridis
)
figure.camera = [
    0.7074783171639407,
    -1.0612174757459112,
    0.07074783171639523,
    0,
    0,
    0,
    0,
    0,
    1,
]

# Provide image fallback
with capture_output() as c:
    display(figure, Image("image/probability-line-interval.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

From the same dataset used to produce {numref}`ransac-greedy-1-labels` (and associated figures), a series of track fits using the PeARL algorithm (using the line interval model given by {eq}`p-point-line-solution`) were produced. Whilst {numref}`pearl-greedy-1-labels` and {numref}`pearl-greedy-2-labels` offer moderate improvements in track labelling over their respective RANSAC results in {numref}`ransac-greedy-1-labels` and {numref}`ransac-greedy-2-labels`, these represent ideal behaviour of the RANSAC algorithm. Under narrower track angles, the sequential RANSAC approach given in {numref}`content:sequential-ransac` suffers from poor fits due to earlier track fits intersecting with separate tracks. Such a pathological worst-case is depicted in {numref}`ransac-greedy-3-labels`, with the improved PeARL result shown in {numref}`pearl-greedy-3-labels`. In this case it is both the choice of bounded line intervals _and_ a global fitting approach that regularises the result.

Of fundamental importance to any track-fitting approach is the treatment of each track on an equal basis, and establishing the concept of a global (total) fit. The PeARL method provides a mechanism for this, and the relative advantages can be seen in particular in {numref}`pearl-greedy-3-labels`. A particular challenge of using PeARL with line _intervals_ (as defined above) is the increase in dimensionality of the space from whic PeARL samples candidate models. Unlike unbounded lines, line intervals do not well describe points that lie beyond the interval bounds (indeed, unbounded lines have infinite bounds). As such, the problem is more sensitive to the set of available models, as prior samples are poorly incentivised to expand their inlier set. Further work could be performed here to investigate the prior distribution from which candidate models are sampled, such as the use of scattering-vertex seeding. The use of unbounded lines with PeARL is also feasible, and retains many of the advantages of the PeARL algorithm over sequential RANSAC. However, the problem of small-angle scattering is less tractable through unbounded lines, due to the strong incentive to grow the inlier set without impedence due to a track length penalty.

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of the simulated elastic scattering reaction shown in {numref}`ransac-greedy-1-labels`. 
      Three track labels given by the PeARL algorithm are indicated by the colour map. In comparison to {numref}`ransac-greedy-1-labels`, 
      it can be seen that the PeARL fit (with line intervals) preserves a common vertex through
      distinct track separation.
    name: pearl-greedy-1-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
pearl_greedy_1 = ak.from_parquet("data/1-pearl-greedy.parquet")

plot_greedy_1 = show_event(
    pearl_greedy_1,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(pearl_greedy_1["pearl"].label)},
)


plot_greedy_1.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_1, Image("image/1-pearl-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`pearl-greedy-1-labels` using PeARL. 
      Both the track direction and end-point should be considered; these fits correspond to bounded line intervals.
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. For the same reaction as depicted
      in {numref}`ransac-greedy-1-tracks`, it can be seen that the PeARL fit (with
      line intervals) better preserves a common vertex through distinct track separation.
      The line-interval parameterisation makes it possible to clearly identify the
      estimated vertex from the end-point of the incident beam track.
    name: pearl-greedy-1-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_1_tracks = show_event(
    pearl_greedy_1,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(pearl_greedy_1["pearl"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(pearl_greedy_1["pearl"].track):
    plot_greedy_1_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.stop),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_1_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_1_tracks, Image("image/1-pearl-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of the simulated elastic scattering reaction shown in {numref}`ransac-greedy-2-labels`. 
      Three track labels given by the PeARL algorithm are indicated by the colour map. In comparison to {numref}`ransac-greedy-2-labels`, 
      it can be seen that the PeARL fit (with line intervals) avoids overfitting of the incident
      beam (blue) track, although a reduced degree of overfitting is observed in the
      scattered beam (purple) region.
    name: pearl-greedy-2-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
pearl_greedy_2 = ak.from_parquet("data/2-pearl-greedy.parquet")

plot_greedy_2 = show_event(
    pearl_greedy_2,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(pearl_greedy_2["pearl"].label)},
)


plot_greedy_2.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_2, Image("image/2-pearl-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`pearl-greedy-2-labels` using PeARL. 
      Both the track direction and end-point should be considered; these fits correspond to bounded line intervals.
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. For the same reaction as depicted
      in {numref}`ransac-greedy-2-tracks`, it can be seen that the PeARL fit (with
      line intervals) better reconstructs the angle of each track in agreement with
      the simulation. A common vertex is much more easily identified by the intersection
      of the reconstructed tracks.
    name: pearl-greedy-2-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_2_tracks = show_event(
    pearl_greedy_2,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(pearl_greedy_2["pearl"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(pearl_greedy_2["pearl"].track):
    plot_greedy_2_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.stop),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_2_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_2_tracks, Image("image/2-pearl-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D scatter plot of the simulated elastic scattering reaction shown in {numref}`ransac-greedy-3-labels`. 
      Three track labels given by the PeARL algorithm are indicated by the colour map. In comparison to 
      {numref}`ransac-greedy-3-labels`, it can be seen that the PeARL fit (with line intervals) avoids the discontinuity in the
      reconstructed incident beam (blue) track. As such, the labelling of the scattered
      beam (yellow) track has more support. The degree of overfitting in the light 
      product (purple) track is also much diminished, and all clusters are considered 
      inliers.
    name: pearl-greedy-3-labels
  image:
    align: center
    width: '512'
tags: [hide-input]
---
pearl_greedy_3 = ak.from_parquet("data/3-pearl-greedy.parquet")

plot_greedy_3 = show_event(
    pearl_greedy_3,
    0xFF0000,
    "event",
    show_simulation=False,
    cluster_kwargs={"attribute": ak.to_numpy(pearl_greedy_3["pearl"].label)},
)


plot_greedy_3.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_3, Image("image/3-pearl-greedy-label.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

```{code-cell} ipython3
---
mystnb:
  figure:
    caption: 3D visualisation of the tracks reconstructed from {numref}`pearl-greedy-3-labels` using PeARL. 
      Both the track direction and end-point should be considered; these fits correspond to bounded line intervals.
      The simulated (red) tracks and reconstructed (blue) tracks are superimposed over a semi-transparent
      point-cloud of the measured track clusters. For the same reaction as depicted
      in {numref}`ransac-greedy-3-tracks`, it can be seen that the PeARL fit (with
      line intervals) produces a far more reasonable reconstruction of the track angles,
      with the closest-point-of-approach between any two tracks producing a good starting-point
      for vertex estimation. As evidenced by its length, the incident beam track is
      slightly overfit. A bigger discrepancy lies in the light-product track, which
      is visually distinct from the simulated track. Here it can be presumed that
      secondary scattering in the simulation leads to a bending in the track, which
      lies below the resolution of the MicroMeGaS. As such, only a single track is
      observed here.
    name: pearl-greedy-3-tracks
  image:
    align: center
    width: '512'
tags: [hide-input]
---
plot_greedy_3_tracks = show_event(
    pearl_greedy_3,
    color=0xFF0000,
    label="event",
    cluster_kwargs={
        "attribute": ak.to_numpy(pearl_greedy_3["pearl"].label),
        "opacity": 0.1,
    },
)


for i, track in enumerate(pearl_greedy_3["pearl"].track):
    plot_greedy_3_tracks += k3d.line(
        np.stack(
            [
                vector_to_ndarray(track.start),
                vector_to_ndarray(track.stop),
            ]
        ),
        color=0x0000FF,
        point_size=2,
        name=f"Track {i}",
    )

plot_greedy_3_tracks.camera = [
    7.159987587605925,
    19.32128636237384,
    12.873808399614415,
    0.8849930990985254,
    20.737317744505287,
    1.1921020617616975,
    -0.8449857089887459,
    0.08698490340507949,
    0.5276672987635235,
]


# Provide image fallback
with capture_output() as c:
    display(plot_greedy_3_tracks, Image("image/3-pearl-greedy-tracks.png"))

display(c.outputs[0].data | c.outputs[1].data, raw=True)
```

+++ {"tags": ["no-latex"]}

(expt:theory:kinematic-fitting)=
## Kinematic Fitting
Many classes of problem, including those seen in track fitting, are amenable through least squares optimisation. In the context of track fitting, it is often the case that the solution is required to satisfy a set of constraints. These constraints ensure that determined solution is physically admissible.

The general case of least squares estimation with constraints is solved by linearising the constraint equations, and solving the problem iteratively. Let {math}`\vec{\eta}=\{ \eta_1, \eta_2, \dots, \eta_n \}` be a vector of {math}`N` observables, whose measured values are {math}`\vec{y}`, with errors given by the covariance matrix {math}`V\mathopen{}\pqty{\vec{y}}\mathclose{}`.
From the Least-Squares Principle {cite:ps}`frodesen_probability_1979`, the objective function {math}`\chi^2` is given by
:::{math}
:label: least-squares-problem
\chi^2 = \pqty{\vec{y}-\vec{\eta}}^TV\mathopen{}\pqty{\vec{y}}\mathclose{}^{-1}\pqty{\vec{y}-\vec{\eta}}\,.
:::
It follows that the best estimates of {math}`\vec{\eta}` satisfy
:::{math}
:label: least-squares-solution
\grad_{\vec{\eta}} {\chi^2\mathopen{}\pqty{\vec{\eta}}\mathclose{}} = \vec{0}\,.
:::
Frequently one is interested in a solution to {eq}`least-squares-solution`, subject to constraints. Consider a single constraint {math}`g`, for which {math}`S=\{ \vec{r}:g(\vec{r})=0 \}`. The minimum for {math}`f` subject to {math}`g` is the point {math}`\vec{r}_1\in S` at which any small displacement along {math}`g` yields no change in {math}`f` (to first order). If this were not the case, there would exist another point {math}`\vec{r}_2\in S` for which {math}`f(\vec{r}_2) < f(\vec{r}_1)`. It follows that level curve {math}`f(\vec{r})=k` must be parallel to {math}`g` at {math}`\vec{r}_1`, which is equivalently stated as
:::{math}
\grad{f} = \lambda\grad{g}\,,
:::
where {math}`\lambda` is a constant (see {numref}`lagrange-multipliers`). 


:::{figure} image/lagrange-multipliers.svg
:name: lagrange-multipliers
:width: 300px

Diagram illustrating a constrained optimisation problem, in which the constraint (red curve) touches an equipotential contour (blue curve) of the function being optimised. By definition, the constrained solution occur where the two curves are touching, in order for the solution to be a minimum.
:::

Instead of a single constraint {math}`g(\vec{r})`, one might have {math}`K` constraint equations,
:::{math}
g_k\mathopen{}\pqty{\vec{\eta}, \vec{\xi}}\mathclose{} = 0\,, \qquad\qquad k=1,2,\dots,K\,.
:::
where {math}`\vec{\xi}` is a set of unmeasured model variables {math}`\vec{\xi}=\{ \xi_1, \xi_2, \dots, \xi_J \}`.The solution to {eq}`least-squares-solution` is then given by reformulating the problem in terms of the Lagrangian
:::{math}
\mathcal{L} = \chi^2 + \sum_k \lambda_k g_k\,,
:::
and solving {math}`\grad_{\lambda,\vec{r}}\mathcal{L} = 0` for {math}`\vec{r}`.

Our original problem in {eq}`least-squares-problem` may be rewritten using Lagrange multipliers, such that one minimises
:::{math}
\chi^2\mathopen{}\pqty{\vec{\eta}, \vec{\xi}, \vec{\lambda}}\mathclose{} = \left(\vec{y}-\vec{\eta}\right)^TV\mathopen{}\pqty{\vec{y}}\mathclose{}^{-1}\left(\vec{y}-\vec{\eta}\right) +
2\vec{\lambda}^T\vec{g}\mathopen{}\pqty{\vec{\eta}, \vec{\xi}}\mathclose{}\,.
:::
% It follows that the best estimates of {math}`\vec{\eta}` and {math}`\vec{\xi}` satisfy
% :::{math}
%   \vec{f}\mathopen{}\pqty{\vec{\eta}, \vec{\xi}}\mathclose{} = \vec{0}
%   \,.
% :::

Setting the gradient of {math}`\chi^2` to zero gives
:::{math}
\grad_{\vec{\eta}}\chi^2 &= 2V^{-1}\mathopen{}\pqty{\vec{y}-\vec{\eta}}\mathclose{} + 2G_{\vec{\eta}}^T\vec{\lambda} = \vec{0}\\
\grad_{\vec{\xi}}\chi^2 &= 2G_{\vec{\xi}}^T\vec{\lambda} = \vec{0}\\
\grad_{\vec{\lambda}}\chi^2 &= 2\vec{g}\mathopen{}\pqty{\vec{\eta},\vec{\xi}}\mathclose{} = \vec{0}\,,
:::
where the matrices {math}`G_{\vec{\mu}}` are defined as
:::{math}
\left(G_{\vec{\mu}}\right)_{ki} = \pdv{g_k}{\mu_i}\,.
:::
It follows that to minimise the objective function, one must solve
:::{math}
:label: solution-known

V^{-1}\mathopen{}\pqty{\vec{\eta}-\vec{y}}\mathclose{} + G_{\vec{\eta}}^T\vec{\lambda} = \vec{0}\,,
:::

:::{math}
:label: solution-unknown

G_{\vec{\xi}}^T\vec{\lambda}  = \vec{0}\,,
:::
and
:::{math}
\vec{g}\mathopen{}\pqty{\vec{\eta}, \vec{\xi}}\mathclose{} 
= \vec{0}\,.
:::
Taylor expanding {math}`g(\vec{\eta},\vec{\xi})` to first order about the point {math}`\vec{\eta}^v,\vec{\xi}^v` gives
:::{math}
:label: constraint-linear

\vec{g}\mathopen{}\pqty{\vec{\eta}, \vec{\xi}}\mathclose{} =  \vec{g}\mathopen{}\pqty{\vec{\eta}^v, \vec{\xi}^v}\mathclose{} + G^v_{\vec{\eta}}\mathopen{}\pqty{\vec{\eta}-\vec{\eta}^v}\mathclose{} + G^v_{\vec{\xi}}\mathopen{}\pqty{\vec{\xi}-\vec{\xi}^v}\mathclose{}\,.
:::
Solving  {eq}`solution-known` for {math}`\vec{\eta}` and setting  {eq}`constraint-linear` to zero, it follows that
:::{math}
:label: solution-linear

\vec{g}^v + G^v_{\vec{\eta}}\mathopen{}\pqty{\vec{y}-V\mathopen{}\pqty{G_{\vec{\eta}}^v}\mathclose{}^T\vec{\lambda}-\vec{\eta}^v}\mathclose{} + G^v_{\vec{\xi}}\mathopen{}\pqty{\vec{\xi}-\vec{\xi}^v}\mathclose{} =\vec{0}\,.
:::

By the introduction of
:::{math}
\vec{r} &= \vec{g}^v + G^v_{\vec{\eta}}\mathopen{}\pqty{\vec{y}-\vec{\eta}^v}\mathclose{}\\
S &= G^v_{\vec{\eta}} V\mathopen{}\pqty{G^v_{\vec{\eta}}}\mathclose{}^T\,,
:::
{eq}`solution-linear` becomes
:::{math}
\vec{r} - S\vec{\lambda} + G^v_{\vec{\xi}}\mathopen{}\pqty{\vec{\xi}-\vec{\xi}^v}\mathclose{} = \vec{0}\,.
:::
Left multiplying by {math}`S^{-1}` one obtains
:::{math}
:label: multiplier-definition

\vec{\lambda} = S^{-1}\pqty{\vec{r} + G^v_{\vec{\xi}}\mathopen{}\pqty{\vec{\xi}-\vec{\xi}^v}\mathclose{}}\,.
:::
 {eq}`multiplier-definition` may then be substituted into {eq}`solution-unknown` to give
:::{math}
\pqty{G_{\vec{\xi}}^v}^TS^{-1}\pqty{\vec{r} + G^v_{\vec{\xi}}\mathopen{}\pqty{\vec{\xi}-\vec{\xi}^v}\mathclose{}} = \vec{0}\,,
:::
which may be solved for {math}`\vec{\xi}`:
:::{math}
:label: unknown-definition

 \vec{\xi} = \vec{\xi}^v - \pqty{\pqty{G_{\vec{\xi}}^v}^TS^{-1}G_{\vec{\xi}}^v}^{-1}\pqty{G_{\vec{\xi}}^v}^TS^{-1}\vec{r}\,.
:::
Finally,  {eq}`solution-known` can be rearranged to give
:::{math}
:label: known-definition

\vec{\eta} = \vec{y} - V\mathopen{}\pqty{G_{\vec{\eta}}^v}\mathclose{}^T\vec{\lambda}
:::

The solutions to the system are obtained by repeated application of the update equations as follows:
- Determine {math}`\vec{\xi}^{i+1}` from {math}`\vec{r}^i` and {math}`S^i` using  {eq}`unknown-definition`.
- Find {math}`\vec{\lambda}^{i+1}` from {math}`\vec{\xi}^{i+1}` using  {eq}`multiplier-definition`.
- Use {math}`\vec{\lambda}^{i+1}` to find {math}`\vec{\eta}^{i+1}` using  {eq}`known-definition`.

In this manner, the unknown variables {math}`\vec{\xi}` are initially computed, then the Lagrangian multipliers found, and finally the estimates {math}`\vec{\eta}` of the measured variables {math}`\vec{y}` are updated. This process repeats until the {math}`\chi^2` reaches a minimum, e.g. it becomes stable within successive iterations to some tolerance,
:::{math}
\abs{\frac{\left(\chi^2\right)^{i+1} - \left(\chi^2\right)^{i+1}}{\left(\chi^2\right)^{i}}} < \epsilon\,.
:::

## Conclusion

The fundamental challenge involved with reconstructing the information captured within a TPC is the ability to identify and fit the kinematics of the tracks left behind by the movement of ionising particles. This is a space of on-going research, with classical statistical techniques such as the Hough transform forming the basis of many analyses. In recent times, the RANSAC method has found popularity in its ability to overcome the limitations of the Hough transform, which suffers from poor performance in the phase space of poor track resolution and similar track properties. 

In this chapter, these two methods have been introduced and discussed, with reference to their limitations as track-finding approaches. The RANSAC method was explored in greater detail, with an application to scattering reactions simulated by the TexATSim simulation package. This package was developed by the Texas A&M group, and further enhanced during the work on this thesis, in order to improve the user-experience and the behavior of the cluster resolution fit model. From these simulations, it was shown that the sequential RANSAC technique suffers from poor performance in a number of scenarios, which represent the limits of the greedy fitting approach.

Subsequently, the reframing of the track fitting & finding task as an Uncapacitated Facility Location Problem was made, in order to explore the set of similar problems outside of nuclear physics that have already been solved. Through an introduction to the method of Graph Cuts, a novel track fitting approach that leverages the PEaRL algorithm was introduced. In support of this novel approach, the cost function of a line-interval model was derived to provide the ability to fit finite-length tracks. This new track fitting approach using line intervals was later applied to the simulation reactions shown in {numref}`content:sequential-ransac`, and the improved reconstruction performance emphasised as a function of the global, interval based fitting technique.

Finally, a discussion of the theory behind kinematic fitting (constrained optimisation) was made, in order to support the next steps in the analysis workflow described in {numref}`experiment`.
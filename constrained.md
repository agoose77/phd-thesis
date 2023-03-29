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

           The general case of least squares estimation with constraints is solved by linearising the constraint equations, and solving the problem iteratively. Let {math}`\known=\set{\eta_1, \eta_2, \dots, \eta_n}` be a vector of {math}`N` observables, whose measured values are {math}`\measured`, with errors given by the covariance matrix {math}`V\mathopen{}\left(\measured\right)\mathclose{}`.
From the Least-Squares Principle {cite:ps}`frodesen:probability-and-statistics`, the objective function {math}`\chi^2` is given by
:::{math}
:label: least-squares-problem

^2 = (-)<sup>TV()</sup>{-1}(-),.
:::
It follows that the best estimates of {math}`\known` satisfy
:::{math}
:label: least-squares-solution

\_ = ,.
:::
Frequently one is interested in a solution to {eq}`least-squares-solution`, subject to constraints. Let us consider a set of {math}`K` constraint equations,
:::{math}
g\_k(, ) = 0,, k=1,2,,K,.
:::
where {math}`\unknown` is a set of unmeasured model variables {math}`\vec{\xi}=\set{\xi_1, \xi_2, \dots, \xi_J}`.
Consider a single constraint {math}`g`, for which {math}`S=\set{\vec{r}:g(\vec{r})=0}`. The minimum for {math}`f` subject to {math}`g` is the point {math}`\vec{r}_1\in S` at which any small displacement along {math}`g` yields no change in {math}`f` (to first order). If this were not the case, there would exist another point {math}`\vec{r}_2\in S` for which {math}`f(\vec{r}_2) < f(\vec{r}_1)`. It follows that level curve {math}`f(\vec{r})=k` must be parallel to {math}`g` at {math}`\vec{r}_1`, which is equivalently stated as
:::{math}
= ,,
:::
where {math}`\lambda` is a constant. The solution to {eq}`least-squares-solution` is then given by reformulating the problem in terms of the Lagrangian
:::{math}
= ^2 + \_k \_k g\_k,,
:::
and solving {math}`\grad_{\lambda,\vec{r}}\mathcal{L} = 0` for {math}`\vec{r}`.
% Define lagrange multipliers

Our original problem in {eq}`least-squares-problem` may be rewritten using Lagrange multipliers, such that one minimises
:::{math}
^2(, , ) = (-)<sup>TV()</sup>{-1}(-) +
2^T(, ),.
:::
% It follows that the best estimates of {math}`\known` and {math}`\unknown` satisfy
% :::{math}
% (, ) =
% ,.
% :::
Setting the gradient of {math}`\chi^2` to zero gives
:::{math}
*^2 &= 2V^{-1}(-) + 2G*^T= \\
*^2 &= 2G*^T= \\
*^2 &= 2(,) = ,,
:::
where the matrices {math}`G_{\vec{\mu}}` are defined as
:::{math}
(G*{})*{ki} = ,.
:::
It follows that to minimise the objective function, one must solve
:::{math}
V^{-1}(-) + G*^T&= :label: solution-known\\

G\_^T&= :label: solution-unknown\\

(, ) &= ,.
:::
Taylor expanding {math}`g(\known,\unknown)` to first order about the point {math}`\known^v,\unknown^v` gives
:::{math}
(, ) = (^v, ^v) + G<sup>v\_(-</sup>v) + G<sup>v\_(-</sup>v):label: constraint-linear,.

:::
Solving {eq}`solution-known` for {math}`\known` and setting {eq}`constraint-linear` to zero, it follows that
:::{math}
^v + G<sup>v\_(-V(G\_</sup>v)<sup>T-</sup>v) + G<sup>v\_(-</sup>v)&=:label: solution-linear,.

:::
By the introduction of
:::{math}
&= ^v + G<sup>v\_(-</sup>v)\\
S &= G<sup>v\_V(G</sup>v\_)^T,,
:::
{eq}`solution-linear` becomes
:::{math}
- S+ G<sup>v\_(-</sup>v) = ,.
:::
Left multiplying by {math}`S^{-1}` one obtains
:::{math}
:label: multiplier-definition

= S^{-1}( + G<sup>v\_(-</sup>v)),.
:::
{eq}`multiplier-definition` may then be substituted into {eq}`solution-unknown` to give
:::{math}
(G\_<sup>v)</sup>TS^{-1}( + G<sup>v\_(-</sup>v)) = ,,
:::
which may be solved for {math}`\unknown`:
:::{math}
:label: unknown-definition

= ^v - ((G\_<sup>v)</sup>TS<sup>{-1}G\_</sup>v)<sup>{-1}(G\_</sup>v)<sup>TS</sup>{-1},.
:::
Finally, {eq}`solution-known` can be rearranged to give
:::{math}
:label: known-definition

= - V(G\_<sup>v))</sup>T
:::

The solutions to the system are obtained by repeated application of the update equations as follows:

-   Determine {math}`\unknown^{i+1}` from {math}`\vec{r}^i` and {math}`S^i` using {eq}`unknown-definition`.
-   Find {math}`\multipliers^{i+1}` from {math}`\unknown^{i+1}` using {eq}`multiplier-definition`.
-   Use {math}`\multipliers^{i+1}` to find {math}`\known^{i+1}` using {eq}`known-definition`.

In this manner, the unknown variables {math}`\unknown` are initially computed, then the Lagrangian multipliers found, and finally the estimates {math}`\known` of the measured variables {math}`\measured` are updated. This process repeats until the {math}`\chi^2` reaches a minimum, e.g. it becomes stable within successive iterations to some tolerance,
:::{math}
\< ,.
:::

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

```{code-cell}
:tags: [hide-cell]

import ipywidgets as w
import k3d
import numpy as np
from IPython.display import Code
from k3d import matplotlib_color_maps
from matplotlib import cm as mpl_cm
from matplotlib import colors as mpl_colors
from scipy import integrate
```

# Software and Infrastructure

+++

The objectives outlined in {numref}`olab:motivations` can be partitioned into development-focused priorities and product-focused outcomes. Though members of the development team had varying degrees of experience in writing Physics analyses, the landscape of modern software development spans a significant number of software packages, programming languages, and domain-specific knowledge. In order to deliver a usable, extensible platform which could be used to facilitate remote learning within the constrained time frame, a content-first, iterative approach to developing OLAB would be imperative. From these constraints, the following technological decisions were made:
:::{list-table} High-level list of software packages used to build O-Lab.
:header-rows: 1
:name: software-choices
:widths: 1 4

* - Software / Tool
  - Motivation
* - Python
  - Python is the fastest growing programming language as measured by the TIOBE index, and is frequently used in data analytics and dashboarding contexts {cite:ps}`noauthor_tiobe_nodate`. The development group already had varying experience with the language, which is renowned for its quick time-to-first-result.
* - Jupyter Notebook
  - Jupyter Notebooks are widely used in academic research. There are already a significant number of software packages that add interactive widgets, and the notebook format serves as a standard across the Jupyter ecosystem.
* - JupyterHub
  - JupyterHub provides a battle-tested multi-tenant platform around which to serve customised computing environments to individual users. It provides hooks to integrate with LTI authentication systems such as those used by the Canvas LMS.
* - ROOT
  - ROOT is a standard tool used in the particle physics domain for all stages of the analysis lifecycle. 
* - ipywidgets
  - ipywidgets provides a well-tested suite of interactive widgets, which can easily be composed to build complex layouts.
* - Voilà
  - The Voilà server was used alongside jupyter-flex to present linear notebook documents as a customised user-friendly dashboard.
* - Kubernetes on GCP
  - To orchestrate the multi-tenant JupyterHub containers, Kubernetes was deployed on Google Cloud Platform.
:::

Further discussion of the merits and motivations behind this set of software packages is given later in this chapter.

+++

## Jupyter & Interactive Dashboarding

+++

The Jupyter (a loose acronoym meaning Julia-Python-R) project is a 
> non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages. Jupyter will always be 100% open-source software, free for all to use and released under the liberal terms of the modified BSD license {cite:ps}`noauthor_project_nodate`.

It encompasses a range of open source protocols and repositories around which a collaborative, interoperable ecosystem has been established. Through these common protocols and standards, a project building a particular Jupyter project is able to integrate with a range of other Jupyter-aware applications and software libraries. The Jupyter kernel standard, and the Jupyter notebook format are of particular relevance to this project; around these two standards, a strong separation between code, evaluation, and presentation has been established. This separation facilitates specialised workflows in which content authorship can use different tools to those used for the final presentation. {numref}`jupyter-lab-ide` shows an example notebook of the Lorenz attractor open in the JupyterLab IDE. It can be seen that both narrative and computational components are present in the same editor workflow {cite:ps}`stewart_lorenz_2000`. The same notebook can be served via the Voila server, which presents end-users with pre-rendered interactive representations of Jupyter notebooks. {numref}`voila-lorenz` shows a screenshot of Voila serving the Lorenz attractor notebook. It can be seen that the editable code cell has been hidden (removed) from the end user, which places greater emphasis on the narrative and interactive portions of the document.

+++

:::{figure} image/jupyter-lab-ide.png
:name: jupyter-lab-ide
:width: 512px
:align: center

Screenshot of the `Lorenz` demonstration notebook within the JupyterLab next-generation IDE. Rich computational narratives can easily be constructed by interweaving code and markup (Markdown) cells. Rich outputs, such as interactive widgets and rendered plots, can be embedded to support exploratory analyses.
:::

+++

:::{figure} image/voila-lorenz.png
:name: voila-lorenz
:width: 512px
:align: center

Screenshot of the `Lorenz` demonstration notebook presented using Voila. Voila templates can be customised and configured: from re-arranging content or changing the formatting, to building entire applications.
:::

```{code-cell}
---
mystnb:
  figure:
    align: left
    caption: A 3D interactive plot of a particular solution to the Lorentz attractor.
      This particular example does not include any parameterisation; full interactivity
      is frequently is provided by a running "server" (kernel) that executes computations
      and returns the results. This plot was generated with a Jupyter notebook; this
      _thesis_ is written in Jupyter Book, which itself can be driven by these documents.
    name: lorenz-attractor-widget
tags: [hide-input, no-latex]
---
N = 10
angle = 0.0
max_time = 4.0
sigma = 10.0
beta = 8.0 / 3
rho = 28.0


def lorenz_deriv(x_y_z, t0, sigma=sigma, beta=beta, rho=rho):
    """Compute the time-derivative of a Lorenz system."""
    x, y, z = x_y_z
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N, 3))

# Solve for the trajectories
t = np.linspace(0, max_time, int(250 * max_time))
x_t = np.asarray([integrate.odeint(lorenz_deriv, x0i, t) for x0i in x0])

# choose a different color for each trajectory
colors = mpl_cm.viridis(np.linspace(0, 1, N))

plot = k3d.plot(camera_rotate_speed=4, grid_visible=False)

for i in range(N):
    plot += k3d.line(
        x_t[i, :, :].astype(np.float32),
        width=0.6,
        color=int(mpl_colors.rgb2hex(colors[i]).replace("#", "0x"), base=16),
    )
plot.display()
```

Jupyter Notebook (or Lab) is already an established tool for aiding research within the academic sphere. It is used across a range of disciplines, and is particularly popular in the science and engineering fields. It follows that the OLab development team were already partially familiar with parts of the Jupyter ecosystem, and the choice to commit to the Jupyter software stack provided a low barrier to entry for authoring virtual laboratory content.

+++

As discussed in {numref}`olab:learning-tools`, a prospective benefit of virtual laboratories is the ability to unify and maintain the software and content deployment process. A key component of this within the Jupyter project is JupyterHub.
> JupyterHub brings the power of notebooks to groups of users. It gives users access to computational environments and resources without burdening the users with installation and maintenance tasks. Users - including students, researchers, and data scientists - can get their work done in their own workspaces on shared resources which can be managed efficiently by system administrators {cite:ps}`noauthor_project_nodate-1`.

Within institutions, JupyterHub is increasingly popular, with a number of universities building MOOCs upon the platform such as Berkley's Data8 course {cite:ps}`adhikari_issue_2021`. Though these institutions predominantly utilise JupyterHub to provision JupyterLab instances, i.e. to provide a partially homogeneous computing environment, there are an increasing number of groups using JupyterHub to serve third-party software such as RStudio. JupyterHub is built from a series of composable resources that facilitate integration of a multi-tenant compute platform with existing virtual learning systems and compute resources. Users can be authenticated using OAuth or LTI solutions. User environments (containers) can easily be configured by platform maintainers, and can be run on a range of cloud providers e.g. via Kubernetes, or using on-prem infrastructure via SLURM, Torque, or even Docker spawners.  It was for these reasons that the Jupyter technologies listed in {numref}`software-choices` were employed to build O-Lab.

+++

## Containerisation

+++

Just as there exists a challenge in supporting students with installation and management of software packages, the same concerns are present when working with a team of developers to build software. Modern software development typically involves the usage of solutions that guarantee the reproducibility of an environment, such as `conda`, or Node JS's `npm` {cite:ps}`gruning_practical_2018`. These package managers make use of a "lockfile" to solve a set of software dependencies ahead-of-time for a known set of architectures (in the later case, exclusively Node). In doing so, it is guaranteed that users of these lockfiles can reproduce the same environment, avoiding the often seen "this works on my machine" complaint. Of these two examples, Conda is the more general; it provides binary packages for multiple platforms, fulfilling the role of a general-purpose package manager. 

Despite this, there are times when even an equivalent set of packages is insufficient to guarantee a working environment; existing software installed on the host operating system can sometimes "bleed" into the Conda environment, e.g. through environment variables, or additional constraints may be required, such as a particular file-system layout, or port availability. It follows that reproducibility of packages alone is not sufficient to fully reproduce a software environment. Containers are a tool which provide this abstraction by not only "locking" the application state (installed packages), but also the filesystem. They support mechanisms for remapping ports, binding external files, and can be deployed as immutable artefacts, avoiding problems of state corruption. For this reason, they can be a powerful tool in distributing the same development environment to a team of software developers. Indeed, tools such as Visual Studio Code and IntelliJ IDEA now provide remote development workflows that are powered by containers. 

The container concept has undergone many iterations and realisations in the last decade, with recent popularity driven by Docker, which has seen vast adoption since its introduction in 2013 {cite:ps}`zhu_if_2018`. Since that time, industry-wide efforts have focused upon standardisation, with the Open Container Initiative developing standards for container images (that contain the container filesystem) and container runtimes (that extract the container image and setup the relevant namespaces for execution). JupyterHub supports a number of spawners which work with user-defined container images, including `KubeSpawner` and `DockerSpawner`. The benefit of using containers in this context is predominantly to reduce development time; user containers can be tested locally on a local JupyterHub instance, and subsequently deployed with high confidence to remote / cloud-based Hubs. The ease of local development conserves developer time that would otherwise be spent on administering the remote deployment. At the time of O-Lab development, Docker was still a popular choice of image builder and container runtime, and was used to implement both the reproducible development environment, and the final production user image (see {numref}`olab-dockerfile`).

+++

## Cloud Deployment & Provisioning

An impediment to deploying a JupyterHub within an academic institution is the lack of appropriate compute resources. Whilst universities often maintain on-prem compute facilities, these are usually designed to tackle conventional (homogeneous) HPC workloads, rather than the heterogeneous demands of general-purpose user containers. Whilst these systems can be leveraged to host a JupyterHub instance, e.g. using the aforementioned SLURM spawner, in practice the limitations of these systems are encountered fairly immediately. On an administrative level, HPC resources are typically earmarked for research purposes; deployment of teaching resources usually requires a separate treatment. Nonetheless, a trial deployment using the SLURM spawner was trialed to evaluate the viability of the HPC platform as a compute layer. There were several notable drawbacks identified during this trial period: users required VPN access in order to access the Hub from outside the University network, and the startup times were considerable; in some instances, on the order of tens of minutes. In general, this is a drawback of HPC-oriented schedulers; users are rewarded for short-running jobs. Meanwhile, JupyterHub jobs are unknown in duration, and therefore we must ask the schedule for long runtimes on the order of many hours, which leads to low job priorities. 

It follows that a more versatile deployment solution was needed. Without dedicated on-prem compute to power O-Lab, a cloud solution was sought after. In this space, the dominant approach is to use Kubernetes as the lingua-franca of cloud compute providers. Kubernetes defines an abstract set of primitives that collectively facilitate large-scale container orchestration and deployment (see {numref}`kubernetes-diagram`). It is supported by the majority of cloud providers, meaning that an investment in a particular cloud provider is not fraught with the perils of vendor lock-in, as is common with bespoke cloud platforms. 

:::{figure} https://upload.wikimedia.org/wikipedia/commons/b/be/Kubernetes.png
:name: kubernetes-diagram
:width: 512px
:align: center

Architecture diagram of a Kubernetes deployment. Several black-box containers are run within Kubernetes "pods", and communicate with one another over a shared network. Through horizontal and vertical autoscaling, Kubernetes can ensure that available resources are optimally distributed across the running pods. Healthy deployments are ensured through monitoring and subsequent redeployment, providing a mechanism for failure tolerance.
Figure by Khtan66, distributed under a [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en) license.
:::

These building blocks are configured through declarative YAML templates, which can be parameterised by user values to easily customise the deployment through centralised configuration files. See {numref}`kubernetes-certificate` for an example of such a template. Kubernetes is a "lingua franca" for cloud providers because it abstracts over the details of how these platforms expose e.g. routing, disk allocation, etc. Instead, Kubernetes provides a standard interface with which tools like JupyterHub's `KubeSpawner` can communicate, allowing a write-once use-everywhere design. This flexibility was employed during the O-Lab trials; an initial deployment was made onto Microsoft Azure, before subsequent migration to Google Kubernetes Engine (GKE).

+++

:::{code-block} yaml
---
name: kubernetes-certificate
caption: |
    YAML template for a Kubernetes resource configuring the HTTPS certificates of the ingress node.
---

apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: ingress-certificate
spec:
  domains:
    {{- range $.Values.domains }}
    - {{ . }}
    {{- end }}    
:::

+++

Whilst Kubernetes is a powerful tool for managing deployments of scalable applications in the cloud, it does not address the challenge of setting up the infrastructure upon which it runs. For this, Terraform (after investigations with Ansible) was used. Like Kubernetes, a fundamental advantage of Terraform is its declarative configuration files; infrastructure state is expressed through intent (infrastructure as code), rather than imperative procedures. Although a unique Terraform configuration is required for each cloud provider, the building blocks provided by Terraform significantly reduce the maintenance burden. When building cloud-hosted distributed applications, the ability to automate the provisioning and deployment of infrastructure is invaluable.

+++

:::{code-block} terraform
---
name: terraform-gke
caption: |
    Example Terraform Resource configuration file, provisioning a node pool of three compute nodes on Google Kubernetes Engine (GKE).
---

resource "google_container_node_pool" "user_nodes" {
  name       = "user"
  cluster    = google_container_cluster.primary.name
  node_count = 3

  node_config {
    preemptible  = false
    machine_type = "e2-standard-2"

    # Google recommends custom service accounts that have 
    # cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email

    oauth_scopes = [
      ...
    ]

    # To prevent non-user nodes being scheduled here
    labels = {
      "hub.jupyter.org/node-purpose" = "user"
    }

    taint = [
      {
        effect = "NO_SCHEDULE"
        key    = "hub.jupyter.org_dedicated"
        value  = "user"
      }
    ]
  }

  autoscaling {
    min_node_count = 0
    max_node_count = 3
  }
}
:::

+++

A significant drawback of using cloud infrastructure is the runtime costs. Whilst these services take responsibility for managing the infrastructure upon which they operate, this comes with an associated penalty with respect to usage tariffs; users are typically charged according to the number of nodes (and their respective configurations) required to run the cluster. Cloud operators increasingly offer managed Kubernetes deployments, such as Google Kubernetes Engine's Autopilot, in which the baseline runtime cost is governed by the number of _pods_ running, rather than the nodes upon which they run. In this model, even more of the work associated with deploying an application on Kubernetes is managed by the cloud provider, simplifying the task of deploying an application. In general, the tradeoffs and benefits of using a managed service over a self-managed deployment yield an inflection point in the baseline load below which it is more affordable to manage the deployment one's self. Furthermore, managed Kubernetes services often do not benefit from the same "free tier" benefits that providers such as Google Cloud make available. As such, this self-managed scheme was used in the O-Lab. For this reason, infrastructure-as-code was of particular importance; the ability to programmatically tear down and subsequently re-establish the cluster infrastructure enabled the implementation cost-saving shutdowns during quiet period (e.g. weekends).

+++

JuypterHub has several distributions according to the needs of the user. For small deployments _The Littlest JupyterHub_ (TLJH) runs on a single machine, without containerisation. For larger deployments in which scaling is important, and containers are required, there is _Zero to JupyterHub with Kubernetes_. It is this distribution that was chosen for O-Lab. In this distribution, JupyterHub employs two primary Kubernetes pods: a proxy pod, and a Hub pod, that together comprise "JupyterHub". The proxy is used to route network traffic between different endpoints according to a cookie that is associated with each user request. If a user already exists, the proxy pod routes their traffic to the appropriate user pod. Otherwise, the request is instead sent to he Hub pod, which creates the user container. The Hub pod, meanwhile, is responsible for administrative tasks, such as authentication (is the user logged in?), container spawning (provisioning an environment for new users), and an administrative panel for maintenance and deployment information (e.g. who is logged in) (see {numref}`jupyterhub-admin`).

+++

:::{figure} image/jupyterhub-admin.png
:name: jupyterhub-admin
:width: 512px
:align: center

Screenshot of the JupyterHub administrator panel, showing a list of previously seen users, and their server status. Individual user servers can be stopped and started by the administrator; enabling remote troubleshooting in the event of a problem.
:::

+++

:::{admonition} To Do
`ipywidgets`?
`xeus-python`?
modular configuration - how modules connect?
:::

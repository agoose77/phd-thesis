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

# Appendix

+++

:::{code-block} dockerfile
---
name: olab-dockerfile
caption: |
    Sample from the O-Lab Dockerfile configuration. This Dockerfile was used to build both the production and development targets, using a multi-stage build.
---

# Base image ###############################################################################
FROM rootproject/root:6.22.00-ubuntu20.04@sha256:f1013a28f03e91a886ce2e2a3954428258c4fe8901770645b286b159e5fcf20e as base

# Derived from https://github.com/thomasms/docker-g4root/blob/master/ubuntu/Dockerfile.ubuntu18.04
MAINTAINER Angus Hollands <a.d.hollands@pgr.bham.ac.uk>

# See http://label-schema.org
LABEL org.label-schema.name="O-Lab Runtime Container" \
      org.label-schema.description="Runtime environment for O-Lab project" \
      org.label-schema.url="https://gitlab.com/uob-nuclear-olab/olab" \
      org.label-schema.vcs-url="https://gitlab.com/uob-nuclear-olab/olab.git" \
      org.label-schema.vendor="" \
      org.label-schema.license="Apache-2.0" \
      org.label-schema.schema-version="1.0"

      
# Allow builder to specify UID
ARG NB_USER=olab
ARG NB_UID=1000

ENV NB_USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE 0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.1.0rc1
ENV POETRY_PREVIEW=1

# Load requirejs for ROOT
ADD https://requirejs.org/docs/release/2.3.6/minified/require.js ${ROOTSYS}/js/components/requirejs/require.js

# Install packages
RUN apt-get update -qq \
 && apt-get -y install python3-pip python3-venv git ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 # Add a user
 && adduser --disabled-password \
     --gecos "Default user" \
     --uid ${NB_UID} \
     ${NB_USER} \
  && chown -R ${NB_UID} ${HOME} \
  && echo "${NB_USER}:${NB_USER}" | chpasswd \
 # Fix PyROOT v22.
 && sed -i "s/gStyle, style)/gStyle, obj)/" ${ROOTSYS}/js/scripts/JSRootPainter.v6.js \
 # Change permissions of downloaded requirejs
 && chmod 775 ${ROOTSYS}/js/components/requirejs/require.js 

 # Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
RUN chmod og+x -R ${POETRY_HOME}/bin
# Install poetry as user
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Setup virtualenv
ENV VIRTUAL_ENV=/opt/olab-venv
RUN python3 -m venv "$VIRTUAL_ENV" \
  && chown -R "${NB_USER}:${NB_USER}" "${VIRTUAL_ENV}"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Production (base) image  ##########################################################################
FROM base as production-base

WORKDIR /usr/src/olab

# Setup user
RUN chown -R "${NB_USER}:${NB_USER}" /usr/src/olab
USER ${NB_USER}

# Install dependencies
COPY --chown="${NB_USER}:${NB_USER}" pyproject.toml poetry.lock ./
COPY --chown="${NB_USER}:${NB_USER}" extern extern/
RUN poetry install --no-root --no-dev

# Copy Jupyter configuration directory
COPY --chown="${NB_USER}:${NB_USER}" etc/jupyter /usr/local/etc/jupyter/
COPY --chown="${NB_USER}:${NB_USER}" share/jupyter /usr/local/share/jupyter/

# Install olab
COPY --chown="${NB_USER}:${NB_USER}" olab olab/

# Install dependencies
RUN poetry install --no-dev

# Copy resources
COPY --chown="${NB_USER}:${NB_USER}" notebooks notebooks/
COPY --chown="${NB_USER}:${NB_USER}" templates templates/


# Production image  ###############################################################################
FROM production-base as production
WORKDIR /usr/src/olab/notebooks
ENTRYPOINT ["jupyterhub-singleuser"]


# Test image ######################################################################################
FROM production-base as test
COPY tests tests/
RUN poetry install
ENTRYPOINT ["/usr/bin/env", "bash"]


# Development image ###############################################################################
FROM base as development
USER ${NB_USER}
ENTRYPOINT ["/usr/bin/env", "bash"]
  
:::

```{code-cell}

```

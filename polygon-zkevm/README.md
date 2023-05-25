# Main Repo
https://github.com/ledgerwatch/erigon

## Description
This Docker container has installed main tools to work with vault, Azure, Kubernetes ... and is intended to be used as k8s jobs.

**This Image** is used by namespace helm to populate secrets so it **MUST BE PUBLIC**

Entrypoints (or cmd) can be provided with helm (via configmaps).

## Build and Run

`docker build --rm -t erigon:latest .`

## To Run the Image

`docker run -it erigon:latest bash`

You can run Geth and configs will be in the `/node` folder

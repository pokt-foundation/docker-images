# Description

This docker container has installed main tools to work with vault, Azure, kubernetes ... and is intended to be used as k8s jobs.

**This image** is used by namespace helm to populate secrets so it **MUST BE PUBLIC**

Entrypoins (or cmd) can be provided with helm (via configmaps).


# Build and Run

`docker build --rm -t bsc:latest .`

To run the image

`docker run -it bsc:latest bash`

You can run geth and configs will be in /node folder


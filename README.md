# WUR Event Driven Analysis

This project has a goal of exploring event-driven analytics for the purposes of DNA sequencing.
Data should be processed automatically, using a pre-defined pipeline, upon arrival in iRODS.

This repository contains all relevant code used to interact with a Kubernetes cluster set up temporarily at https://145.100.57.119.surf-hosted.nl/ 

The `k8s` directory contains all code which is used to interract with Kubernetes.

The `task_distributor` contains all code which is used as an endpoint to iRODS.

## WUR resources

- [gitlab repo](https://gitlab.com/wurssb)
- [Docker hub](https://hub.docker.com/r/wurssb/unlock_fastp)      

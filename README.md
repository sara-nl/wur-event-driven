# WUR Event Driven Analysis

This project has a goal of exploring event-driven analytics for the purposes of DNA sequencing.
Data should be processed automatically, using a pre-defined pipeline, upon arrival in iRODS.

This repository contains all relevant code used to interact with a Kubernetes cluster set up temporarily at https://145.100.58.53/ 

The `k8s` directory contains all code which is used to interract with Kubernetes.

The `task_distributor` contains all code which is used as an endpoint to iRODS.
## The setup
![Overview](WUR-event-driven.png)
## iRODS setup
The following test rule has been added to iRODS (add location on server).

    acPostProcForPut {

            if($objPath=="/tempZone/home/haukurp/testwebhook") {
                    msiExecCmd("webhook","","","","",*Result);
            }

            *errcode=errorcode(msiGoodFailure);

    }

The rule will simply execute a script called `webhook` when a file is placed in a certain directory.
The webook script which is executed is simply a curl command which sends the necessary information to process the file over HTTP (currently not HTTPS).
The receiving end will then handle the event.
This is a 'fire and forget' pattern as the iRODS rule/script does not validate the response from the backend.
Since there is no validation on response, there are no retries if an event sending fails.

## Useful resources
- [This repo](https://github.com/sara-nl/wur-event-driven/)
- [gitlab repo](https://gitlab.com/wurssb) for code related to DNA processing.
- [Docker hub](https://hub.docker.com/r/wurssb/unlock_fastp) for docker images for DNA processing. The platform will use this image (and potentially others) as a binary to run on uploaded files to iRODS.



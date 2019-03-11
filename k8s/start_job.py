#!/usr/bin/env python3
import logging
import os

import kubernetes
import pendulum
LOGGING_FORMAT = '[%(asctime)-15s][%(levelname)-7s] %(message)s'


def get_logger(name):
    logging.basicConfig(format=LOGGING_FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel('DEBUG')
    return logger


def get_kubernetes_client():
    # If the job is started on kubernets, the config is in a different place.
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        kubernetes.config.load_incluster_config()
    else:
        kubernetes.config.load_kube_config()
    return kubernetes.client


def get_kubernetes_job_template(image, commands, args, name):
    return kubernetes.client.V1Job(
        metadata={},
        api_version='batch/v1',
        kind='Job',
        spec={
            'ttlSecondsAfterFinished': 3600,
            'backoff_limit': 6,
            'template': {
                'spec': {
                    'containers': [
                        {
                            'name': name,
                            'image': image,
                            'command': commands,
                            'args': args,
                            'resources': [
                                {
                                    'requests': {
                                        'memory': '4Gi',
                                        'cpu': '1'
                                    }
                                },
                                {
                                    'limits': {
                                        'memory': '4Gi',
                                        'cpu': '1'
                                    }
                                }
                            ],
                            'restartPolicy': 'OnFailure'
                        }
                    ]
                }
            }
        }
    )

def main():
    # Create job from template
    client= get_kubernetes_client()
    job= get_kubernetes_job_template(
        image='wurssb/unlock_fastp',
        commands=[],
        args=['-c', '/tempZone/home/demo/P_project/I_investigation/S_study/DNA/A_assayX'],
        name='test-job'
    )
    job_name= f'{pendulum.now().format("YYYY-MM-DD-HHmm")}'
    job.metadata['name']= job_name

    # Fire it

    api= client.BatchV1Api()
    api.create_namespaced_job('default', job)


if __name__ == '__main__':
    main()

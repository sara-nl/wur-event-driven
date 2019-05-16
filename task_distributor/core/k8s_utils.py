# -*- coding: utf-8 -*-
"""Kubernets utils."""

import logging
import os
import json
import yaml
import pathlib
from configparser import ConfigParser
import kubernetes.client
from kubernetes.client.rest import ApiException
import time
import copy
from jinja2 import Template


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Read config file.
config = ConfigParser()
config_file = str(pathlib.Path(__file__).parent / '..' / 'app.cfg')
config.read(config_file)
namespace = config.get('K8S', 'namespace')
cm_name = config.get('K8S', 'config_map_name')

# The config file is in a different location when a job is started
# from within the Kubernetes cluster.
if os.getenv('KUBERNETES_SERVICE_HOST'):
    kubernetes.config.load_incluster_config()
else:
    kubernetes.config.load_kube_config()


def create_config_map(cm_json):
    """Create a config map with the job configuration template.

    The template can contain Jinja2 templates that will be rendered later on
    when submitting job with the create_job method, using the dictionary
    passed as an argument.
    """

    body = kubernetes.client.V1ConfigMap(
            api_version='v1',
            kind='ConfigMap',
            metadata={
                'name': cm_name,
                'namespace': namespace
                },
            data=cm_json)

    api = kubernetes.client.CoreV1Api()

    try:
        res = api.create_namespaced_config_map(namespace, body)
        #res = api.replace_namespaced_config_map(cm_name, namespace, body)
        logger.info(res)
    except ApiException as e:
        logger.error("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)


def get_config_map():
    """Get the job configuration template from a config map."""

    api = kubernetes.client.CoreV1Api()

    try:
        res = api.read_namespaced_config_map(cm_name, namespace)
        logger.info(res)
        # If the job description was provided in yaml, we read it like that.
        if 'job.yaml' in res.data:
            return yaml.load(res.data['job.yaml'])
        elif 'job.json' in res.data:
            return json.loads(res.data['job.json'])
        else:
            raise ApiException("Did not find the job description.")
    except ApiException as e:
        logger.error("Exception when calling CoreV1Api->read_namespaced_config_map: %s\n" % e)


def create_job(context):
    """Create job in Kubernetes.

    The job configuration is obtained from a config map.
    The config map can contain Jinja2 templates that are rendered here,
    using the dictionary passed as an argument.

    Arguments:
        context: Dictionary for the Jinja2 rendering.
    """

    job_name = f'{time.time():.0f}'

    job_json = get_config_map()
    job_json["metadata"]["name"] = job_name

    # Replace the Jinja2 templates.
    if context:
        job_json = json.loads(Template(json.dumps(job_json)).render(context))

    job = kubernetes.client.V1Job(
            api_version=job_json["apiVersion"],
            kind=job_json["kind"],
            metadata=job_json["metadata"],
            spec=job_json["spec"])

    api = kubernetes.client.BatchV1Api()

    try:
        res = api.create_namespaced_job(namespace, job)
        logger.info(res)
        return res
    except ApiException as e:
        logger.error("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)

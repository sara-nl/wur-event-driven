# -*- coding: utf-8 -*-
"""Kubernetes endpoint."""

from flask_restplus import Namespace, Resource
import core.k8s_utils as k8s_utils
from kubernetes.client.rest import ApiException
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

api = Namespace('Kubernetes', description='Kubernetes endpoint.')


@api.route('/cm')
class ConfigMapResource(Resource):

    @api.doc('Create config map with the job configuration template.')
    @api.response(200, "Config map created.")
    @api.response(500, "Config map cannot be created.")
    def post(self):
        logger.debug(api.payload)
        if k8s_utils.create_config_map(api.payload):
            return "Config map created.", 200
        else:
            api.abort(500, "Config map cannot be created.")


@api.route('/job')
class JobResource(Resource):

    @api.doc('Create job.')
    @api.response(200, "Job created.")
    @api.response(500, "Job cannot be created.")
    def post(self):
        if k8s_utils.create_job():
            return "Job created.", 200
        else:
            api.abort(500, "Job cannot be created.")

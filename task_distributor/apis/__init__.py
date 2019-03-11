from flask import Blueprint
from flask_restplus import Api

from .k8s import api as ns_k8s

blueprint = Blueprint('Temperature Hose Server', __name__)
api = Api(blueprint)

api.add_namespace(ns_k8s, path='/k8s')

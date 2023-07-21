# janusgraph_client.py

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from flask import current_app

def get_janusgraph_connection():
    graph = Graph()
    janusgraph_server = current_app.config['JANUSGRAPH_SERVER']
    return DriverRemoteConnection(janusgraph_server, 'g')

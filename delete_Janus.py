from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# Connect to JanusGraph server
connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
g = Graph().traversal().withRemote(connection)

# Delete the graph (all vertices and edges)
g.V().drop().iterate()

# Close the connection
connection.close()

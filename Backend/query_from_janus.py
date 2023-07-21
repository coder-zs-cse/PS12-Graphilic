#query_from_json.py


from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __

# Connect to JanusGraph server


# Query and Print Data
# Example: Retrieve all vertices of type 'person'
def query_vertex_by_id(id):
    connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = Graph().traversal().withRemote(connection)
    result =  g.V().has('Item', 'id', id).repeat(__.out()).emit().values('id').toList()
    connection.close()
    return result

def get_Count():
    connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = Graph().traversal().withRemote(connection)
    print("Count", g.V().count().next())
    connection.close()

# print("Total Count", g.V().count().next())
# Close the connection
# print(query_vertex_by_id("0006386709"))


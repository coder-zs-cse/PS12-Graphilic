from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# from gremlin_python.process.anonymous_traversal_source import traversal

connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
graph = Graph()
# The connection should be closed on shut down to close open connections with connection.close()
g = graph.traversal().withRemote(connection)
prev_vertex = None
def store_adjlist_data(filename):
    global prev_vertex
    with open(filename, 'r') as file:
        lines = file.readlines()[3:]  # Skip the first two lines (comments)

        for line in lines:
            values = line.strip().split()
            if len(values) >= 1:
                key = None
                for value in values:
                    print(value)
                    if key is None:
                        key = value
                        g.addV('Item').property('id', value).next()
                    else:
                        vertex = g.addV('Item').property('id', value).next()
                        # g.V(key).addE('follows').to(vertex).next()
                    # if prev_vertex is not None:
                    #     g.V(prev_vertex).addE('follows').to(vertex).next()
                    # prev_vertex = vertex
                break

def addEdge(id1, id2):
    vertex1 = g.V().has('Item', 'id', id1).next()
    vertex2 = g.V().has('Item', 'id', id2).next()
    g.V(vertex1).addE('follows').to(vertex2).next()


input_file_path = "Data/graph.adjlist"
store_adjlist_data(input_file_path)

# addEdge(1,3)


connection.close()
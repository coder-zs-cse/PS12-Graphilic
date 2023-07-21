from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# Connect to JanusGraph server
connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
g = Graph().traversal().withRemote(connection)

# Query and Print Data
# Example: Retrieve all vertices of type 'person'
def query_vertex_by_id(id):
    result =  g.V().has('Item', 'id', id)
    if result.hasNext():
        print(f"Vertex with ID '{id}' exists.")
        print("Properties:")
        print(result.values())
        # while result.hasNext():
        #     print(result)
        #     result.next()
            # properties = vertex.properties()
            # for key in properties.keys():
            #     print(f"{key}: {properties[key].value}")
    else:
        print(f"Vertex with ID '{id}' does not exist.")

# Print the details of all persons
# print("Persons:")
# for person in persons:
#     print("Name:", person.get('name')[0])
#     print("Age:", person.get('age')[0])
#     print("----")

# Example: Retrieve all edges of type 'knows'
# knows_edges = g.E().hasLabel('knows').toList()

# Print the details of all 'knows' edges
# print("Knows Edges:")
# print(knows_edges)

def get_Count():
    print("Count", g.V().count().next())

print("Total Count", g.V().count().next())
# Close the connection
query_vertex_by_id(5)

connection.close()

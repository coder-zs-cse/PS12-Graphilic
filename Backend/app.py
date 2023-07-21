from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
from flask_cors import CORS
from janusgraph_client import get_janusgraph_connection
import pickle
import networkx as nx
import pandas as pd
import json

with open(r'C:\\Users\\Omkar Borker\\OneDrive\\Desktop\\PS12-Graphilic\\Model\\node2vec_for_bipartite.pkl','rb') as f:
    model = pickle.load(f)

with open(r'C:\\Users\\Omkar Borker\\OneDrive\\Desktop\\PS12-Graphilic\\Data\\user_user_graph.json','rb') as f:
    data = json.load(f)
graph = nx.node_link_graph(data)

dataset = pd.read_csv(r"C:\\Users\\Omkar Borker\\OneDrive\\Desktop\\PS12-Graphilic\\Data\\user-user-dataframe.csv")

MONGO_URL = "mongodb+srv://zubinshah:dbUsUK95LA6^@hackrx.dl9muyr.mongodb.net/"
client = MongoClient(MONGO_URL)
collection = client["HackRx"]["MetaData"]

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

def get_similarity_list(model,customerID,list_items):
    cust_embed = model.wv[customerID]
    final_items = {}

    for i in list_items:
        i = re.findall(r'\d+', i)
        i = ''.join(i)
        try:
            item_embedding = model.wv[i]
            final_items[i] = int(cust_embed.dot(item_embedding))
        except KeyError:
            continue
    return final_items

@app.route('/login', methods=['POST'])
def handle_login_request():
    try:
        data = request.json.get('data')
        if data is not None:
            # Bad request
            print(data)
            return jsonify({"message" : "200"}), 200
        else:
            # Return the custom message for POST request
            return jsonify({"this is a bad request"}), 400
    except:
        return jsonify({"error": "Invalid JSON data"}), 400
    
@app.route('/recommend_to_user', methods=['POST'])
def handle_request():
    try:
        data = request.json.get('data')
        if data is not None:
            # Bad request
            print(data)
            return jsonify({"message" : "200"}), 200
        else:
            # Return the custom message for POST request
            return jsonify({"this is a bad request"}), 400
    except:
        return jsonify({"error": "Invalid JSON data"}), 400

    
    
@app.route('/recommend_item', methods=['GET', 'POST'])
def handle_item_request():
    if request.method == 'GET':
        return jsonify({"message": "Request ""item"" successful"}), 200
    elif request.method == 'POST':
        try:
            data = request.get_json()
            received_data = data.get("data")
            if received_data is not None:
                ## bad request 
                return jsonify({"error": "POST requests not allowed"}), 400
            else:
                ## model chages here
                return jsonify({"message": "Request successful"}), 200
        except:
            return jsonify({"error": "Invalid JSON data"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405
    

@app.route('/search_query', methods=['POST'])
def search_item():
    try:
        data = request.json.get('data')
        if data is not None:
            query_title = data.get("query_title", "")
            # Regular expression for partial matching of the queried title
            regex_query = re.compile(query_title, re.IGNORECASE)

            # Find books with titles matching the partial query and limit the results to 10
            similar_books = collection.find({"title": {"$regex": regex_query}}).limit(10)

            # Get the book category based on the first match found
            similar_data = []
            for book in similar_books:
                title = book["title"]
                category = book.get("group", "")
                categories_data = book.get("categories", {}).get("ASIN ID", [])
                categories = [category.split('|')[-1] for category in categories_data]

                similar_data.append({"title": title, "category": category, "categories": categories})

            return jsonify({"query_title": query_title, "similar_books": similar_data}), 200
        else:
            return jsonify({"error": "Invalid JSON data"}), 400
    except:
        return jsonify({"error": "Invalid JSON data"}), 400

@app.route('/books_by_category', methods=['GET'])
def books_by_category():
    # Get the category choice from the query parameter
    category_choice = 'Clergy'

    if not category_choice:
        return jsonify({"error": "Category parameter missing"}), 400

    # Regular expression for partial matching of the queried category
    regex_query = re.compile(re.escape(category_choice), re.IGNORECASE)

    # Find books with categories matching the partial query
    matching_books = collection.find({"categories.ASIN ID": {"$regex": regex_query}}).limit(20)

    books_data = []
    for book in matching_books:
        title = book["title"]
        category = book.get("group", "")
        categories_data = book.get("categories", {}).get("ASIN ID", [])
        categories = [category.split('|')[-1] for category in categories_data]

        books_data.append({"title": title, "category": category, "categories": categories})

    return jsonify({"category_choice": category_choice, "matching_books": books_data}), 200

# @app.route('/recommend_similar', methods=['GET'])
# def recommend_similar():
#     # ASIN of the main product
#     cust_id = "A2JW67OY8U6HHK"

#     # Find the document for the main ASIN
#     neighbours = list(graph.neighbors(cust_id))
#     list_items = []
#     for node in neighbours:
#         list_items.append(dataset.loc[dataset['customer id']==node,'ASIN'].iloc[0])

#     if len(list_items) < 0:
#         return jsonify({"error": "Main product not found"}), 200

#     # Retrieve the ASIN IDs of similar items from the "similar" column
#     prediction = get_similarity_list(model,'A2JW67OY8U6HHK',list_items)

#     return  prediction

@app.route('/recommend_similar', methods=['POST'])
def recommend_similar():
    try:
        data = request.get_json()
        cust_id = data.get("cust_id")
        if not cust_id:
            return jsonify({"error": "Username (cust_id) not provided"}), 400

        # Find the document for the main ASIN
        neighbours = list(graph.neighbors(cust_id))
        list_items = []
        for node in neighbours:
            list_items.append(dataset.loc[dataset['customer id'] == node, 'ASIN'].iloc[0])

        # If there are no similar items, return an empty list
        if not list_items:
            return jsonify({"error": "No similar items found"}), 200

        # Retrieve the ASIN IDs of similar items from the "similar" column
        # Replace this with your actual implementation of 'get_similarity_list'
        prediction = get_similarity_list(model, cust_id, list_items)

        return jsonify({"title":prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/graph-data', methods=['GET'])
def get_graph_data():
    connection = get_janusgraph_connection()
    
    try:
        g = connection.remote_traversal()
        # Perform your Gremlin queries using the 'g' object
        result = g.V().limit(10).valueMap().toList()
    finally:
        connection.close()
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)



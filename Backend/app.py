from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
from flask_cors import CORS
from janusgraph_client import get_janusgraph_connection


MONGO_URL = "mongodb+srv://zubinshah:dbUsUK95LA6^@hackrx.dl9muyr.mongodb.net/"
client = MongoClient(MONGO_URL)
collection = client["HackRx"]["MetaData"]

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

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
    

@app.route('/search_query', methods=['GET', 'POST'])
def search_item():
    query_title = "school"

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

@app.route('/recommend_similar', methods=['GET'])
def recommend_similar():
    # ASIN of the main product
    main_asin = "0827229534"

    # Find the document for the main ASIN
    main_product = collection.find_one({"ASIN": main_asin})

    if not main_product:
        return jsonify({"error": "Main product not found"}), 404

    # Retrieve the ASIN IDs of similar items from the "similar" column
    similar_asins = main_product.get("similar", {}).get("ASIN ID", [])

    # If there are no similar ASIN IDs, return an empty list
    if not similar_asins:
        return jsonify({"message": "No similar items found"}), 200

    # Retrieve information of the first similar item from the ASIN ID
    similar_item_asin = "0687023955"
    similar_item = collection.find_one({"ASIN": similar_item_asin})

    # Extract relevant information of the similar item
    similar_item_title = similar_item.get("title", "")
    similar_item_group = similar_item.get("group", "")
    similar_item_salesrank = similar_item.get("salesrank", "")

    return jsonify({
        "main_asin": main_asin,
        "similar_item_asin": similar_item_asin,
        "similar_item_title": similar_item_title,
        "similar_item_group": similar_item_group,
        "similar_item_salesrank": similar_item_salesrank
    }), 200
    
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



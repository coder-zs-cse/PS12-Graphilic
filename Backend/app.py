from flask import Flask, request, jsonify
from collections import OrderedDict
from pymongo import MongoClient
import re
from flask_cors import CORS
from query_from_janus import query_vertex_by_id
import pickle
import networkx as nx
import pandas as pd
import json
alpha = 20
beta = 80
with open(r'D:\\Projects\\Hackx\\PS12-Graphilic\\Model\\node2vec_for_bipartite.pkl','rb') as f:
    model = pickle.load(f)

with open(r'D:\\Projects\\Hackx\\PS12-Graphilic\Data\\user_user_graph.json','rb') as f:
    data = json.load(f)
graph = nx.node_link_graph(data)

dataset = pd.read_csv(r"D:\\Projects\\Hackx\\PS12-Graphilic\Data\\user-user-dataframe.csv")
priceset = pd.read_csv(r"D:\\Projects\\Hackx\\PS12-Graphilic\Data\\new_data_profit.csv")

MONGO_URL = "mongodb+srv://zubinshah:dbUsUK95LA6^@hackrx.dl9muyr.mongodb.net/"
client = MongoClient(MONGO_URL)
collection = client["HackRx"]["MetaData"]

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)

search_ASIN = None

def get_profit_values(similarity_dict):
    # Read the CSV file containing the profit data
    print(similarity_dict)
    # Create a dictionary to store the profit values corresponding to keys in the similarity dictionary
    profit_values = {}

    # Iterate through the keys in the similarity dictionary
    for key in similarity_dict.keys():
        # Get the similarity value from the similarity dictionary
        similarity_value = similarity_dict[key]

        # Search for the corresponding key in the CSV file
        matching_rows = priceset.loc[priceset['ASIN'] == key]

        # Check if the key exists in the DataFrame and if it has at least one matching row
        if not matching_rows.empty:
            # Get the profit value from the first matching row in the DataFrame
            profit_value = matching_rows['Profit'].iloc[0]

            # Store the profit value in the profit_values dictionary
            profit_values[key] = profit_value
        else:
            # If the key is not found in the DataFrame, set the profit value to None or any default value
            profit_values[key] = None

    return profit_values

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

def custom_sort(items, alpha, beta,profit_values):
    sorted_items = sorted(items.items(), key=lambda x: alpha * x[1] + beta * profit_values[x[0]], reverse=True)
    
    return sorted_items


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

    
    
@app.route('/recommend_item', methods=['POST'])
def handle_item_request():
    try:
        data = request.get_json()
        # print(data)
        received_data = data.get('data')
        # print(received_data)
        if received_data is None:
            ## bad request 
            return jsonify({"error": "POST requests not allowed"}), 400
        else:
            ## model chages here
            similar_asins = query_vertex_by_id(received_data)
            print(similar_asins)
            # similar_data =[]
            # for asin in similar_asins:
            #     query_result = collection.find_one({"ASIN": asin})
            #     print("query:",query_result)
            #     if query_result is not None:
            #         similar_data.append(query_result)
            return jsonify({"message": "Request successful", "ASINs": similar_asins}), 200
    except:
        return jsonify({"error": "Invalid JSON data"}), 400
    else:
        return jsonify({"error": "Method not allowed"}), 405
    

@app.route('/search_query', methods=['POST'])
def search_item():
    global search_ASIN
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
                ASIN = book["ASIN"]
                category = book.get("group", "")
                categories_data = book.get("categories", {}).get("ASIN ID", [])
                categories = [category.split('|')[-1] for category in categories_data]

                similar_data.append({"ASIN":ASIN,"title": title, "category": category, "categories": categories})
            search_ASIN = similar_data[0]["ASIN"]
            return jsonify({"query_title": query_title, "similar_books": similar_data, "stored": search_ASIN}), 200
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
    global alpha,beta
    try:
        data = request.get_json()
        cust_id = data.get("data")
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
        print(prediction)
        profit_values = get_profit_values(prediction)
        combined_dict = {asin: alpha * prediction[asin] + beta * profit_values[asin] for asin in prediction}
        # Sort the combined dictionary based on the calculated values
        sorted_combined = custom_sort(combined_dict, alpha, beta,profit_values)

        # Display the sorted ASINs and their corresponding calculated values
        for asin, calculated_value in sorted_combined:
            print(f"ASIN: {asin}, Calculated Value: {calculated_value}")   
        sorted_combined_dict = OrderedDict(sorted_combined)
        # Prepare the JSON response with IDs as keys and values as values
        response = {asin: score for asin, score in sorted_combined_dict.items()}
        print(response)
        return jsonify({"res": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/slider',methods=['POST'])
def update_slider_value():
    global alpha, beta
    
    try:
        data = request.json
        slider_value = data.get('slider_value')
        
        # Update global variables alpha and beta based on the slider value received
        alpha = 100 - slider_value
        beta = slider_value
        print(alpha)
        print(beta)
        
        # Prepare and return the response
        response_data = {
            'alpha': alpha,
            'beta': beta
        }
        
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)



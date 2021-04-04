import flask
import json
from flask import request, jsonify
from flask import render_template
import pandas as pd
import psycopg2


app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = json.load(open ("data/api.json", "r"))

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/books/all', methods=['GET'])
def api_all():
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
    )


    sql = """select * from api;"""

    a = pd.read_sql(sql, con=connection).to_dict()
    return jsonify(a)


@app.route('/api/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/books/add', methods=['GET'])
def add_data():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'name' in request.args and 'number' in request.args:
        name = request.args['name']
        number = request.args['number']
    else:
        return "Error: No id field provided. Please specify an id."

    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
    )

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO api VALUES(%s, %s)", (name, number))

    connection.commit()  # <- We MUST commit to reflect the inserted data
    if cursor.rowcount:
        cursor.close()
        return "SUCCESS!"
    else:
        cursor.close()
        return "FAILED!"



app.run()

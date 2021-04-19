import urllib.request
import flask
import json
from flask import request, jsonify
from flask import render_template, redirect
import pandas as pd
import psycopg2
from linkedin import linkedin
from urllib.request import urlopen
app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = json.load(open("data/api.json", "r"))

@app.route('/', methods=['GET'])
def home():
    if 'code' in request.args:
        code = request.args['code']
        client_id = "78yuk1i7oafw90"
        client_secret = "UHo4QTDPugd9BdRH"
        redirect_uri = "http://localhost:5000"

        s = """https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&client_id=%s&client_secret=%s&code=%s&redirect_uri=%s""" % (client_id, client_secret, code, redirect_uri)
        # return s
        return redirect(s)

        # application = linkedin.LinkedInApplication(token=token)
        # return application.get_profile()
    url = "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78yuk1i7oafw90&scope=r_liteprofile&state=123456&redirect_uri=http://localhost:5000"
    # return urllib.request.urlopen(url).read().decode()
    return url

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


@app.route('/code', methods=['GET'])
def linkedin_all():
    if 'code' in request.args:
        token = request.args['code']
        application = linkedin.LinkedInApplication(token = token)
    return "<h2>" + str(application.get_profile()) + "</h2>"



app.run()

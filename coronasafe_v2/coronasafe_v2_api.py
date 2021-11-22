from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
# getting the api key
import os
import coronasafe_v2_backend as cs_backend
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(".\\coronasafe_v2\\g_api_key.env")
load_dotenv(dotenv_path=dotenv_path)
G_API_KEY = str(os.getenv('G_API_KEY'))

app = Flask(__name__)
api = Api(app)

# test
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"
# actual http request handler

@app.route('/getPlaces/', methods=["GET"])
def search():
    thingToSearch = request.args.get('search_query')
    data = cs_backend.places_search(thingToSearch)
    return {'data': data}, 200,


app.debug = True
app.run()  # run our Flask app
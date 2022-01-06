from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import os
import coronasafe_v2_backend as cs_backend

app = Flask(__name__)
api = Api(app)


@app.route('/getPlaces/', methods=["GET"])
def search():
    thingToSearch = request.args.get('search_query')
    data = cs_backend.places_search(thingToSearch)
    print(data)
    return {'data':data}, 200

@app.route('/getNumbers/', methods=["GET"])
def getNumbers():
    thingToSearch = request.args.get('search_query')
    data = cs_backend.master_risk_calculator(thingToSearch)
    return {'data':data}, 200

app.debug = True
app.run()  
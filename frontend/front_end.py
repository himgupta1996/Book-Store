from flask import Flask
import requests 
from flask import request
from flask import jsonify
from response_util import get_failed_response,get_success_response 
import sys
sys.path.insert(1, '../')
from const import CATALOG_SERVER, ORDER_SERVER

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to Book Store!"

@app.route('/buy', methods=['GET'])
def buy():
    try:
        data = request.args
        id=data["id"]
        results=requests.get("%s:%s/buy/%s"%(ORDER_SERVER["IP"],ORDER_SERVER["PORT"],id))
        results=results.json()
        return results
    except Exception as e:
        get_failed_response(message=str(e))


#query_by_topic
@app.route('/search',methods=['GET'])
def search():
    try:
        if 'topic' in request.args:
            topic=request.args['topic']
        else:
            return "Error: No topic field provided. Please specify a topic."
        results=requests.get("%s:%s/item?topic=%s"%(CATALOG_SERVER["IP"],CATALOG_SERVER["PORT"],topic))
        results=results.json()
        return results
    except Exception as e:
        get_failed_response(message=str(e))


#query_by_id
@app.route('/lookup',methods=['GET'])
def lookup():
    try:
        if 'id' in request.args:
            id=request.args['id']
        else:
            return "Error: No id field provided. Please specify an id."
        results=requests.get("%s:%s/item/%s"%(CATALOG_SERVER["IP"],CATALOG_SERVER["PORT"],id))
        results=results.json()
        return results
        
    except Exception as e:
        get_failed_response(message=str(e))

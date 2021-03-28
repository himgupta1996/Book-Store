from flask import Flask
import requests 
from flask import request
from flask import jsonify
from response_util import get_failed_response,get_success_response 
import sys,os
sys.path.append('..')
import const 

order_ip=const.ORDER_SERVER['IP']
order_port=const.ORDER_SERVER['PORT']

catalog_ip=const.CATALOG_SERVER['IP']
catalog_port=const.CATALOG_SERVER['PORT']


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to Book Store!"

@app.route('/buy', methods=['POST'])
def buy():
    try:
        data = request.args
        id=data["id"]
        results=requests.get(order_ip+":"+str(order_port)+"/buy/"+id)
        results=results.json()
        return get_success_response('item',results)
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
        results=requests.get(catalog_ip+":"+str(catalog_port)+"/item?topic="+topic)
        results=results.json()
        return get_success_response('item',results)
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
        results=requests.get(catalog_ip+":"+str(catalog_port)+"/item/"+id)
        results=results.json()
        return get_success_response('item',results)
        
    except Exception as e:
        get_failed_response(message=str(e))

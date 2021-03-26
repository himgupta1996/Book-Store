from flask import Flask
import requests 
from flask import request
from flask import jsonify
from response_util import get_failed_response,get_success_response 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Welcome to Book Store!"

    
# curl -d "id=1" -X POST https://example.com/buy
@app.route('/buy', methods=['POST']) 
def buy():
    try:
        data = request.json
        id=data["id"]
        results=requests.get("http://localhost:8001/buy?item="+id)
        return get_success_response('item',results)
        # if(results==200):
        #     return {"Purchase":"success"}
        # else:
        #     return{"Error":"Unable to Purchase"}
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
        results=requests.get("http://localhost:8080/item?topic="+topic)
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
        results=requests.get("http://localhost:8080/item/"+id)
        results=results.json()
        return get_success_response('item',results)
        
    except Exception as e:
        get_failed_response(message=str(e))

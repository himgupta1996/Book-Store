from flask import Flask
import requests 
from flask import request
from flask import jsonify 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!"

@app.route('/test', methods=['GET'])
def test():
    if 'id' in request.args:
        return "Do something" + str(id)
    else:
        return "Error: No id field provided. Please specify an id."
    
# # Usage: /buy?id=[id of book to buy]
# @app.route('/buy',methods=['GET'])
# def buy():
#     if 'id' not in request.args:
#         return "Error: No id field provided. Please specify an id."
#     results=requests.get("http://localhost:8001/buy?item="+id)
#     if(results==200):
#         return {"Purchase":"success"}
#     else:
#         return{"Error":"Unable to Purchase"}
    


# curl -d "id=1" -X POST https://example.com/buy
@app.route('/buy', methods=['POST']) 
def buy():
    data = request.json
    id=data["id"]
    results=requests.get("http://localhost:8001/buy?item="+id)
    if(results==200):
        return {"Purchase":"success"}
    else:
        return{"Error":"Unable to Purchase"}


#query_by_topic
@app.route('/search',methods=['GET'])
def search():
    if 'topic' in request.args:
        topic='topic'
    else:
        return "Error: No topic field provided. Please specify a topic."
    results=requests.get("http://localhost:8002/query_by_topic/"+id)
    return results['response']


#query_by_id
@app.route('/lookup',methods=['GET'])
def lookup():
    if 'id' in request.args:
        id='id'
    else:
        return "Error: No id field provided. Please specify an id."
    results=requests.get("http://localhost:8002/query_by_id/"+id)
    return results['response']



if __name__ == '__main__':
    # debug mode
    app.run(host='0.0.0.0', debug=True, port=6060)
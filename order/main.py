# from application import app
from flask import Flask, render_template, request, Response, json, redirect, flash, url_for, session, Markup, jsonify
from config import Config
from response_util import get_failed_response, get_success_response
import requests
from datetime import datetime

catalog_url = Config.catalog_server['ip'] + ":" + Config.catalog_server['port']

app = Flask(__name__)
app.config.from_object(Config)

from sqlite_db import order

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	return {"response": "Hi! You have reached the order server."}

@app.route('/orders')
def orders():
	order_db = order()
	orders = order_db.get_orders()
	print(orders)
	return get_success_response('order', orders)

@app.route('/buy/<item_id>', methods = ['GET'])
def buy(item_id = None):
	if not item_id:
		get_failed_response(message = "Item id has to be passed for buying.", status_code = 400)
	order_db = order()

	##Check wether the item id is there in the catalog server
	r = requests.get(catalog_url+"/item/%s"%(item_id))
	if r.status_code == 200:
		#get the item 
		item = r.json()['item']
		if item:
			item_count = r.json()['item'][0]['count']
			print("TRhe item count is %s" % (item_count))
			
		else:
			return get_failed_response(status_code = 404, message =  "Item with id %s not found in the catalog server." % (item_id))
	else:
		get_failed_response(message = "Couldn't fetch item status from the catalog server.")

	#If present issue a update request to the catalog server
	if item_count>0:
		payload = {"count" : -1}
		r = requests.put(catalog_url+"/item/%s"%(item_id), data = json.dumps(payload))
		order_id = order_db.add_order({'item_id': item_id, 'created':  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})
		return get_success_response("order", output = {'id': order_id}, message = "Item with id %s bought successfully." % (item_id))
	else:
		payload = {"count": 10}
		r = requests.put(catalog_url+"/item/%s"%(item_id), data = json.dumps(payload))
		return get_failed_response(message = "The item with id %s is no longer present in the catalog server" % (item_id), status_code = 404)
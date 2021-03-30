import os
import time
import subprocess
import time
import sys
import re
import pexpect
import pexpect.popen_spawn
import argparse
import requests
import json
import logging
import random
# sys.path.insert(1, '../')
from const import FRONTEND_SERVER, CATALOG_SERVER, ORDER_SERVER, CATALOG_ITEMS, BOOK_TOPICS

##Initializing logger object
logging.basicConfig(filename="client.log",
					format='%(asctime)s %(message)s',
					filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

#taking arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--times", required=False,
   help="Provide the number of times you want to run the look,search and buy methods.")
args = vars(ap.parse_args())

##Starting the servers  
try:
	subprocess.Popen("cd frontend && python -m flask run -p %s"%(FRONTEND_SERVER['PORT']), shell = True)
	subprocess.Popen("cd catalog && python -m flask run -p %s"%(CATALOG_SERVER['PORT']), shell = True)
	subprocess.Popen("cd order && python -m flask run -p %s" % (ORDER_SERVER['PORT']), shell = True)
	logger.info("Waiting for the servers to deploy.")
	time.sleep(5)
except Exception as e:
	print("Failed to start servers. Error: %s" % (str(e)))

##call to frontend server to lookup for a particular item
def frontend_lookup(item_id):
	logger.info("Looking up the item with id '%s' in frontend server." % (item_id))
	try:
		r = requests.get("%s:%s/lookup?id=%s"%(FRONTEND_SERVER["IP"],FRONTEND_SERVER["PORT"],item_id))
		if r.status_code == 200:
			logger.info("Lookup of item '%s' successfull."%(item_id))
			return r.json()['item'][0]['count']>0
		else:
			logger.info("Lookup of item '%s' failed with status_code: %s"%(item_id, r.status_code))

	except Exception as e:
		logger.info("Failed to connect to frontened server. Error: %s" % (str(e)))
		raise

##call to frontend to buy a particular item
def order_buy(item_id):
	logger.info("Buying the item with id '%s' from front server." % (item_id))
	try:
		r = requests.get("%s:%s/buy?id=%s"%(FRONTEND_SERVER["IP"],FRONTEND_SERVER["PORT"],item_id))
		if r.status_code == 200:
			logger.info("Succesfully bought the item '%s'" % (item_id))
			return r.json()['order']
		else:
			logger.info("Buy of item '%s' failed with status_code: %s"%(item_id, r.status_code))
	except Exception as e:
		logger.info("Failed to connect to frontened server. Error: %s" % (str(e)))
		raise

##call to the frontend to search a particular topic
def frontend_search(topic):
	logger.info("Searching catalog server for the topic '%s'" % (topic_to_search))
	try:
		r = requests.get("%s:%s/search?topic=%s"%(FRONTEND_SERVER["IP"],FRONTEND_SERVER["PORT"],topic))
		status_code = r.status_code
		if status_code == 200:
			logger.info("Search of topic '%s' successfull."%(topic))
			return r.json()['item']
		else:
			logger.info("Search of topic '%s' failed with status_code: %s"%(topic, status_code))
	except Exception as e:
		logger.info("Failed to connect to frontened server. Error: %s" % (str(e)))
		raise
##
n=5
if args['times']:
	n = int(args['times'])
for i in range(n):
	##selecting a random topic to search
	index = random.randint(0,len(BOOK_TOPICS)-1)
	topic_to_search = BOOK_TOPICS[index]

	#getting all the items with a particular topic
	items = frontend_search(topic_to_search)

	##taking a random item from the list and checking the presence of the same in the server
	item_to_lookup = items[random.randint(0,len(items)-1)]
	id_ = item_to_lookup['id']
	item_present = frontend_lookup(id_)

	##if item is present, call the order server to buy the particular item
	if item_present:
		item_bought=order_buy(id_)
	else:
		logger.info("Item with id '%s' got finished in the server." % (id_))
	logger.info("---------------------------------------------------------")
	time.sleep(2)




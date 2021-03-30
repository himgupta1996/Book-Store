from flask import Flask,request
import sqlite3
from pydantic import BaseModel
from response_util import get_failed_response,get_success_response
import json
import logging

logging.basicConfig(filename="catalog.log",level=logging.DEBUG,
					format='%(asctime)s %(message)s')
# logger=logging.getLogger()
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

class Book(BaseModel):
        id_:int = None    
        title:str = None
        count:int = None
        cost:int = None
        topic:str = None
        
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def catalog():
    
    '''
    DB initialization code below
    Uncomment to re-initialize the database
    '''
    '''
    con = sqlite3.connect('catalog.db')
    cur = con.cursor()
    cur.execute("DROP TABLE catalog");
    cur.execute("create table IF NOT EXISTS catalog (id INTEGER PRIMARY KEY,title text,count INTEGER, cost INTEGER, topic text)")
    sql_query ="INSERT INTO catalog(id,title,count,cost,topic) VALUES(?,?,?,?,?) "
    values_1 = (1, 'How to get a good grade in 677 in 20 minutes a day.', 5, 10, 'distributed systems');
    values_2 = (2, 'RPCs for Dummies.', 5, 10, 'distributed systems');
    values_3 = (3, 'Xen and the Art of Surviving Graduate School.', 5, 10, 'graduate school');
    values_4 = (4, 'Cooking for the Impatient Graduate Student.', 5, 10, 'graduate school');
    cur.execute(sql_query,values_1)
    cur.execute(sql_query,values_2)
    cur.execute(sql_query,values_3)
    cur.execute(sql_query,values_4)
    con.commit()
    con.close()
    '''
    
    return 'Hello, catalog!'

'''
item route is used for search, lookup and update.
There are 4 cases which are overall covered here - 
1. item route with an id_, method  = ['GET']
    Returns the item for the corresponding id
2. item route with a topic parameter in the query parameters, method  = ['GET']
    Returns the items for the corresponding topic
3. item route with no id and no payload, method  = ['GET']
    Returns the list of the items in the catalog database
4. item route with an id_,update payload, method  = ['PUT']
    Updates the item having id=id_ with the update data passed in payload.
    The update data contains fields 'cost' and 'count' to update the cost 
    and count of the entry with id=id_. Note that the cost update is direct 
    whereas the count update is addtional in nature since the order server 
    will pass the number of books which the frontend wants to buy.
'''


@app.route("/item/<id_>",methods = ['GET'])
@app.route("/item",methods = ['GET'])
def item(id_ = None):
    try:
        con = sqlite3.connect('catalog.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        sql_query = ""
        if id_ == None:
            if request.args.get('topic') != None:
                app.logger.info("Looking up the items with topic '%s' in catalog database." % (request.args.get('topic')))
                sql_query ="select * from catalog where topic = ?;"
                values = (request.args.get('topic'),)
            else:
                app.logger.info("Looking up the all the items in the catalog database.")
                sql_query = "select * from catalog"
                values = ()
        else:
            app.logger.info("Looking up the item with id '%s' in catalog database." % (id_))
            sql_query ="select * from catalog where id = ?;"
            values = (id_,)
        cur.execute(sql_query,values)
        response = cur.fetchall()
        if response != None:
            app.logger.info("Lookup Successful")
        con.commit()
        con.close()
        return get_success_response('item',response,status_code = 200)
    except Exception as e:
        get_failed_response(message=str(e))
    

@app.route("/item/<id_>",methods = ['PUT'])
def update_by_id(id_):
    try:
        con = sqlite3.connect('catalog.db')
        con.row_factory = dict_factory
        cur = con.cursor()
        sql_query ="select * from catalog where id = ?;"
        select_values = (id_,)
        app.logger.info("Looking up the item with id '%s' in catalog database for updating the item." % (id_))
        cur.execute(sql_query,select_values)
        response = cur.fetchone()
        book = Book(id_ = response['id'],title = response['title'],count = response['count'],cost = response['cost'],topic = response['topic'])
        data = json.loads(request.data)
        
        if data.get('cost') != None:
            book.cost = data.get('cost')
            app.logger.info("Updating the cost of the book with id = '%s'" % (id_))    
        if data.get('count') != None and book.count > 0:
            app.logger.info("Updating the count of the book with id = '%s'" % (id_))  
            book.count += data.get('count')
        
        sql_query ="REPLACE INTO catalog(id,title,count,cost,topic) VALUES(?,?,?,?,?)"
        values = (book.id_,book.title,book.count,book.cost,book.topic);
        cur.execute(sql_query,values)   
        app.logger.info('Catalog database update successful')  
        con.commit()
        con.close()
        return get_success_response('item',book.dict(),status_code=201)
    
    except Exception as e:
        get_failed_response(message=str(e))
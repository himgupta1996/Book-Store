from flask import Flask,request
import sqlite3
from pydantic import BaseModel
from response_util import get_failed_response,get_success_response
import json

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
                sql_query ="select * from catalog where topic = ?;"
                values = (request.args.get('topic'),)
            else:
                sql_query = "select * from catalog"
                values = ()
        else:
            sql_query ="select * from catalog where id = ?;"
            values = (id_,)
        cur.execute(sql_query,values)
        response = cur.fetchall()
        con.commit()
        con.close()
        return get_success_response('item',response)
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
        cur.execute(sql_query,select_values)
        response = cur.fetchone()
        book = Book(id_ = response['id'],title = response['title'],count = response['count'],cost = response['cost'],topic = response['topic'])
        
        data = json.loads(request.data)
        if data.get('cost') != None:
            book.cost = data.get('cost')
        if data.get('count') != None:
            book.count += data.get('count')
        
        
        sql_query ="REPLACE INTO catalog(id,title,count,cost,topic) VALUES(?,?,?,?,?)"
        values = (book.id_,book.title,book.count,book.cost,book.topic);
        cur.execute(sql_query,values)   
        con.commit()
        con.close()
        raise
        return get_success_response('item',book.dict())
    
    except Exception as e:
        get_failed_response(message=str(e))
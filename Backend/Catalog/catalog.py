from flask import Flask,request
import sqlite3
from pydantic import BaseModel

app = Flask(__name__)

class Book(BaseModel):
        id_:int = None    
        title:str = None
        count:int = None
        cost:int = None
        topic:str = None

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
    cur.execute("create table catalog (id INTEGER PRIMARY KEY,title text,count INTEGER, cost INTEGER, topic text)")
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

@app.route('/get_full_catalog',methods = ['GET'])
def get_catalog():
    con = sqlite3.connect('catalog.db')
    cur = con.cursor()
    cur.execute("select * from catalog")
    catalog_response = cur.fetchall() 
    con.commit()
    con.close()
    return {'response':catalog_response}


@app.route("/query_by_topic/<topic>",methods = ['GET'])
def query_by_topic(topic):
    con = sqlite3.connect('catalog.db')
    cur = con.cursor()
    sql_query ="select * from catalog where topic = ?;"
    values = (topic,);
    cur.execute(sql_query,values)
    response = cur.fetchall()
    con.commit()
    con.close()
    return {'response':response}

@app.route("/query_by_id/<id_>",methods = ['GET'])
def query_by_id(id_):
    con = sqlite3.connect('catalog.db')
    cur = con.cursor()
    sql_query ="select * from catalog where id = ?;"
    values = (id_,);
    cur.execute(sql_query,values)
    response = cur.fetchall()
    con.commit()
    con.close()
    return {'response':response}

@app.route("/update_by_id/<id_>",methods = ['PUT'])
def update_by_id(id_):
    con = sqlite3.connect('catalog.db')
    cur = con.cursor()
    sql_query ="select * from catalog where id = ?;"
    select_values = (id_,)
    cur.execute(sql_query,select_values)
    response = cur.fetchone()
    book = Book(id_ = response[0],title = response[1],count = response[2],cost = response[3],topic = response[4])
    
    if request.json.get("cost") != None:
        book.cost = request.json.get('cost')
    if request.json.get('count') != None:
        book.cost += request.json.get('count')
    
    sql_query ="REPLACE INTO catalog(id,title,count,cost,topic) VALUES(?,?,?,?,?)"
    values = (book.id_,book.title,book.count,book.cost,book.topic);
    cur.execute(sql_query,values)    
    con.commit()
    con.close()
    return {'response':'Update Successful'}
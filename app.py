from flask import Flask,render_template,url_for,g,request
import sqlite3
import database
import datetime
import json

app=Flask(__name__)
app.config['DEBUG']=True


#DATABASE HELPER FUNCTION
def connect_db():
    conn=sqlite3.connect('data.db')
    conn.row_factory=sqlite3.Row
    return conn

def get_db():
    if hasattr(g,'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(err):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


#DATABASE HELPER FUNCTIONS FINISHED


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        rawdate=request.form.get('date')
        entry_date=datetime.datetime.strptime(rawdate,'%Y-%m-%d')
        entry_date=datetime.datetime.strftime(entry_date,'%Y%m%d')
        database.insert_row(entry_date,'log_date')
        all_dates=database.query_dates()
        pretty_dates=list(map(lambda di: datetime.datetime.strptime(str(di['entry_date']),'%Y%m%d'),all_dates))
        pretty_dates=list(map(lambda dobj: datetime.datetime.strftime(dobj,'%B%d %Y'),pretty_dates))
        pretty_dates=list(map(lambda dobj: str(dobj),pretty_dates))
        return render_template('home.html',all_dates=pretty_dates)
    else:    
        return render_template('home.html')

@app.route('/view/<date>',methods=['GET','POST'])
def view(date):
    if request.method=='POST':
        food_id=int(request.form.get('food-id'))
        date=str(date)
        dateobj=datetime.datetime.strptime(date,'%B %d %Y')
        dateobj=datetime.datetime.strftime(dateobj,'%Y%m%d')
        date_dic=database.query_date_id(dateobj)
        date_id=int(date_dic['id'])
        database.insert_fooddate(date_id,food_id)
        return 'jd'

    date=str(date)
    dateobj=datetime.datetime.strptime(date,'%B%d %Y')
    ndateobj=datetime.datetime.strftime(dateobj,'%B %d %Y')
    qdateobj=datetime.datetime.strftime(dateobj,'%Y%m%d')    
    list_dic=database.query_food_id()

    date_dic=database.query_date_id(qdateobj)
    date_id=int(date_dic['id'])
    return render_template('day.html',pretty_date=str(ndateobj),food_dic=list_dic)

@app.route('/food',methods=['GET','POST'])
def food():
    if request.method=='GET':
        return render_template('add_food.html')
    else:
        food_data=dict()
        food_data['name']=request.form.get('food-name')
        food_data['protein']=request.form.get('protein')
        food_data['carb']=request.form.get('carb')
        food_data['fat']=request.form.get('fat')
        database.insert_row(food_data,'food')
        list_food_data=database.query_all('food')
        return render_template('add_food.html',list_food_data=list_food_data)

if __name__ == "__main__":
    app.run()

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

        total_nutri=[]
        for pdate in all_dates:
            total_nutri.append(total_nutri_all_dates(pdate['entry_date']))

        pretty_dates=list(map(lambda dobj: datetime.datetime.strftime(dobj,'%B %d %Y'),pretty_dates))
        pretty_dates=list(map(lambda dobj: str(dobj),pretty_dates))
        return render_template('home.html',all_dates=pretty_dates,total_nutri=total_nutri)
    else:
        all_dates=database.query_dates()
        pretty_dates=list(map(lambda di: datetime.datetime.strptime(str(di['entry_date']),'%Y%m%d'),all_dates))

        total_nutri=[]
        for pdate in all_dates:
            total_nutri.append(total_nutri_all_dates(pdate['entry_date']))

        pretty_dates=list(map(lambda dobj: datetime.datetime.strftime(dobj,'%B %d %Y'),pretty_dates))
        pretty_dates=list(map(lambda dobj: str(dobj),pretty_dates))    
        return render_template('home.html',all_dates=pretty_dates,total_nutri=total_nutri)

@app.route('/view/<date>',methods=['GET','POST'])
def view(date):
    date=str(date)
    dateobj=datetime.datetime.strptime(date,'%B %d %Y')
    ndateobj=datetime.datetime.strftime(dateobj,'%B %d %Y')
    qdateobj=datetime.datetime.strftime(dateobj,'%Y%m%d')    
    list_dic=database.query_food_id()
    date_dic=database.query_date_id(qdateobj)
    date_id=int(date_dic['id'])


#handling post req
    if request.method=='POST':
        food_id=int(request.form.get('food-id'))
        date=str(date)
        dateobj=datetime.datetime.strptime(date,'%B %d %Y')
        dateobj=datetime.datetime.strftime(dateobj,'%Y%m%d')
        date_dic=database.query_date_id(dateobj)
        date_id=int(date_dic['id'])
        database.insert_fooddate(date_id,food_id)

        foods_per_day=database.query_foods_per_day(qdateobj)
        total_nutrients=list()
        p=carb=f=cal=0
        for food in foods_per_day:
            p+=food['protein']
            carb+=food['carb']
            f+=food['fat']
            cal+=food['calories']
        total_nutrients.append(p)
        total_nutrients.append(carb)
        total_nutrients.append(f)
        total_nutrients.append(cal)
        
        return render_template('day.html',pretty_date=str(ndateobj),food_dic=list_dic,foods_per_day=foods_per_day,total_nutri=total_nutrients)




    foods_per_day=database.query_foods_per_day(qdateobj)
    total_nutrients=list()
    p=carb=f=cal=0
    for food in foods_per_day:
        p+=food['protein']
        carb+=food['carb']
        f+=food['fat']
        cal+=food['calories']
    total_nutrients.append(p)
    total_nutrients.append(carb)
    total_nutrients.append(f)
    total_nutrients.append(cal)
    return render_template('day.html',pretty_date=str(ndateobj),food_dic=list_dic,foods_per_day=foods_per_day,total_nutri=total_nutrients)



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




#some useful functions
def total_nutri_all_dates(qdateobj):
    foods_per_day=database.query_foods_per_day(qdateobj)
    total_nutrients=list()
    p=carb=f=cal=0
    for food in foods_per_day:
        p+=food['protein']
        carb+=food['carb']
        f+=food['fat']
        cal+=food['calories']
    total_nutrients.append(p)
    total_nutrients.append(carb)
    total_nutrients.append(f)
    total_nutrients.append(cal)
    return total_nutrients

if __name__ == "__main__":
    app.run()

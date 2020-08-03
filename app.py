from flask import Flask,render_template,url_for,g,request
import sqlite3
import database
import datetime

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
        date=str(request.form.get('date'))
        database.insert_date(date)
        ids_list=database.query_tables('log_data')
        foods_list=database.query_tables('food')
        list_details=do_list_details()
        return render_template('home.html')
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

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
        date_arry=str(str(datetime.datetime.now()).split()[0])
        print(date_arry)
        database.insert_row(food_data,'food',date_arry)
        list_food_data=database.query_all('food')
        return render_template('add_food.html',list_food_data=list_food_data)



#usefull functions
def do_list_details(date_ids_list,foods_id_list):
    results=list()
    for ids in date_ids_list:
        for food_id_list in foods_id_list:
            if (database.check_existence(date_ids_list,foods_id_list)):
                pass
                

if __name__ == "__main__":
    app.run()

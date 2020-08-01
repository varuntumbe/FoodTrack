import sqlite3

def create_table():
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.executescript(""" 
        CREATE TABLE IF NOT EXISTS log_date(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            entry_date DATE NOT NULL 
        );
        CREATE TABLE IF NOT EXISTS food(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT NOT NULL,
            protein INTEGER NOT NULL,
            carb INTEGER NOT NULL,
            fat INTEGER NOT NULL,
            calories INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS food_date(
            date_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            PRIMARY KEY(date_id,food_id)
        )
    """)
    conn.commit()
    conn.close()

#insert row function
def insert_row(table_data,tablename):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cal=int((int(table_data['protein'])*4 + int(table_data['carb'])*4 + int(table_data['fat'])*9 ))
    if tablename=='food':
        cur.execute(""" 
            INSERT INTO food (name,protein,carb,fat,calories)
            VALUES (?,?,?,?,?)
        """,(table_data['name'],table_data['protein'],table_data['carb'],table_data['fat'],cal))
        conn.commit()
        conn.close()


#query database
def query_all(tablename):
    conn=sqlite3.connect('data.db')
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute('SELECT * FROM {} '.format(tablename))
    list_food_data=cur.fetchall()
    conn.close()
    return list_food_data




#executing
create_table()

import sqlite3

def create_table():
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.executescript(""" 
        CREATE TABLE IF NOT EXISTS log_date(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            entry_date TEXT NOT NULL UNIQUE
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
def insert_row(table_data,tablename,timedata):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cal=int((int(table_data['protein'])*4 + int(table_data['carb'])*4 + int(table_data['fat'])*9 ))
    if tablename=='food':
        cur.execute(""" 
            INSERT INTO food (name,protein,carb,fat,calories)
            VALUES (?,?,?,?,?)
        """,(table_data['name'],table_data['protein'],table_data['carb'],table_data['fat'],cal))
        conn.commit()    
        #adding date 
        cur.execute("""
        INSERT OR IGNORE INTO log_date (entry_date)
        VALUES(?)
        """,(timedata,))
        conn.commit()
        #adding to food_date
        cur.execute(""" 
        SELECT id FROM food WHERE name=(?) AND protein=(?) AND carb=(?) AND fat=(?)
        AND calories=(?)
        """,(table_data['name'],table_data['protein'],table_data['carb'],table_data['fat'],cal))
        food_id=cur.fetchone()[0]

        cur.execute(""" 
        SELECT id FROM log_date WHERE entry_date=(?)
        """,(timedata,))
        date_id=cur.fetchone()[0]

        cur.execute(""" 
        INSERT OR IGNORE INTO food_date (date_id,food_id)
        VALUES (?,?)
        """,(date_id,food_id))
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


#query just dates' id
def query_tables(tablename):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.execute('SELECT id FROM {}'.format(tablename))
    id_list=list(map(lambda tu: tu[0],cur.fetchall()))
    conn.close()
    return id_list


#just insert date
def insert_date(date):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.execute(""" 
    INSERT OR IGNORE INTO  log_date (entry_date)
    VALUES (?)
    """,(date,))
    conn.commit()
    conn.close()

#checking the existance of date_id_list and food_id_list
def check_existence(d_id,f_id):
    conn=sqlite3.connect('data.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM food_date WHERE date_id=(?) AND food_id=(?)',(d_id,f_id))
    if len(cur.fetchall()) > 0:
        conn.close()
        return True
    else:
        conn.close()
        return False
    


create_table()

import mysql.connector
import random

import menuFunction

connect, database = menuFunction.connection()

def format(result):
    print(f"{"ID":<11} {"Name":<20} {"Price":<10}")
    if result is None:
        return 
    for r in result:
        price = f"{r[2]:,}"
        print(f"{r[0]:<11} {r[1]:<20} {price:<10}")

def append(name, price):
    while True:
        id = f"DR{str(random.randint(0, 9999)).zfill(4)}"
        database.execute("SELECT COUNT(*) FROM drinks")
        result = database.fetchone()
        
        if result[0] == 0:  
            break
        isID = "SELECT id FROM drinks WHERE id = %s"
        database.execute(isID, (id,))
        if database.fetchone() is None:
            break
    query = "INSERT INTO drinks (id, name, price) VALUES (%s, %s, %s)"
    database.execute(query, (id,name,price))
    connect.commit()

def show(value = None):
    format(menuFunction.view('*','drinks',value))


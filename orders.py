import mysql.connector

import menuFunction

connect, database = menuFunction.connection()

def format(result):
    print(f"{"":<11} {"":<20} {"Quantity":<10} {"Price":<15} {"Total":<20}")
    for r in result:
        price = f"{r[2]:,}"
        total = f"{r[3]:,}"
        print(f"{"":<11} {r[0]:<20} {r[1]:<10} {price:<15} {total:<20}")

def append(bill_id,drinks_id,quantity):
    if not drinks_id.lstrip('DR').isdigit():
        database.execute("SELECT id FROM drinks WHERE name = %s", (drinks_id,))
        id = database.fetchone()[0]
        database.execute("SELECT price FROM drinks WHERE name = %s", (drinks_id,))
    else:
        database.execute("SELECT price FROM drinks WHERE ID = %s", (drinks_id,))
        id = database.fetchone()[0]
    result = database.fetchone()

    price = result[0]
    total = price * quantity 
        
    insert = "INSERT INTO orders (bill_id, drinks_id, quantity, price, total) VALUES (%s, %s, %s, %s, %s)"
    database.execute(insert, (bill_id, id, quantity, price, total))
        
    connect.commit()

def show(value = None):
    format(menuFunction.view('d.name, quantity, d.price, o.total','orders o JOIN drinks d ON o.drinks_id = d.id JOIN bill b ON o.bill_id = b.id ',value))

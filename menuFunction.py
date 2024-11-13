import mysql.connector

def close_connection(connect, database):
    database.close()
    connect.close()

def connection():
    connect = mysql.connector.connect (
        host="localhost",
        user="root",
        password="123456",
        database="coffeepayment")
    database = connect.cursor(buffered=True)
    return connect, database

connect, database = connection()

def delete(table, value = None):
    if value is None:
        database.execute(f"DELETE FROM {table}")
    else:
        if isFind(table,value):
            condition = " AND ".join(value)
            database.execute(f"DELETE FROM {table} WHERE {condition}")
            print("Deleted successfully.")
        else:
            print(f"{table} not exist!.")
    connect.commit()

def update(value, new_value,table):
    if isFind(table,value):
        condition = " AND ".join(value)
        database.execute(f"UPDATE {table} SET {new_value} WHERE {condition}")
        print("Updated successfully.")
    else:
        print(f"Update failure! {table} not exist!.")
    connect.commit()

def view(text, table, value = None):
    if value is None:
        database.execute(f"SELECT {text} FROM {table}")
    else:
        if isFind(table, value):
            condition = " AND ".join(value)
            database.execute(f"SELECT {text} FROM {table} WHERE {condition}")
        else:
            print(f"{table} not exist.")
            return 
    connect.commit()
    return database.fetchall()

def isFind(table,value = None):
    if value is None:
        database.execute(f"SELECT * FROM {table}")
    else:
        if isinstance(value, str):
            value = [value]
        condition = " AND ".join(value)
        database.execute(f"SELECT * FROM {table} WHERE {condition}")
    connect.commit()
    return database.fetchone() is not None

def renueve():
    database.execute('SELECT SUM(total) AS turnover FROM bill')
    turnover = database.fetchone()
    print(f"Turnover: {turnover[0]}")
    database.execute('SELECT SUM(quantity) as quantity FROM orders')
    quantity = database.fetchone()
    print(f"Quantity: {quantity[0]}")
    database.execute("""SELECT d.name, SUM(quantity) AS quantity_best_seller FROM orders o JOIN drinks d ON o.drinks_id = d.id JOIN bill b ON o.bill_id = b.id GROUP BY d.name
ORDER BY quantity_best_seller DESC LIMIT 3""")
    best_seller = database.fetchall()
    print("Best Seller: ")
    for bs in best_seller:
        print(f"\t{bs[0]}\t Quantity: {bs[1]}")
    database.execute("""SELECT d.name, SUM(quantity) AS quantity_best_seller FROM orders o JOIN drinks d ON o.drinks_id = d.id JOIN bill b ON o.bill_id = b.id GROUP BY d.name
ORDER BY quantity_best_seller ASC LIMIT 3""")
    worst_seller = database.fetchall()
    print("Worst Seller: ")
    for ws in worst_seller:
        print(f"\t{ws[0]}\t Quantity: {ws[1]}")

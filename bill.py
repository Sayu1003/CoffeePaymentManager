import mysql.connector
from datetime import datetime

import orders
import menuFunction

connect, database = menuFunction.connection()

def format(result):
    for r in result:
        total = f"{r[2]:,}"
        date = r[4].strftime('%Y-%m-%d %H:%M:%S') 
        customer = r[1] if r[1] is not None else "Null"
        print(f"ID: {r[0]:<11}\t Customer: {customer:<20}\t Total: {total:<15}\t Method: {r[3]:<15}\t {date:<20}")
        orders.show([f"bill_id = {r[0]}"])

def create():
    query = "INSERT INTO bill (customer, total, method, date) VALUES (%s,%s,%s, NOW())"
    customer = input('Name of customer (Enter to skip): ')
    database.execute(query, (customer,0,'Cash',))
    connect.commit()
    database.execute("SELECT LAST_INSERT_ID()")
    bill_id = database.fetchone()[0]
    while True:
        drink = input('Enter ID or Name of drink (Done -> please just Enter): ')
        if drink == "":
            break
        if not drink.lstrip('DR').isdigit():
            get_drink_ID = "SELECT id FROM drinks WHERE name = %s"
            database.execute(get_drink_ID,(drink,))
            result = database.fetchone()
            if result:
                drink = result[0]
            else:
                print('Drink not found!.')
                continue
        else:
            isID = "SELECT 1 FROM drinks WHERE id = %s"
            database.execute(isID,(drink,))
            if not database.fetchone():
                print('Drink not found!.')
                continue
        quantity = int(input('Enter quantity: '))
        orders.append(bill_id,drink,quantity)
    update_total = "UPDATE bill SET total = (SELECT SUM(total) FROM orders WHERE orders.bill_id = bill.id) WHERE id = %s"
    database.execute(update_total,(bill_id,))
    connect.commit()
    database.execute(f"SELECT total FROM bill WHERE id = {bill_id}")
    getTotal = database.fetchone()
    print(f"Total: {getTotal[0]}")
    if getTotal[0] == 0:
        condition = [f"id = {bill_id}"]
        menuFunction.delete('bill',condition)
        print('Cancel create bill.')
        return
    while True:
        try: 
            method = int(input('1\Cash\n2\Credit card\n3\Debit card\n4\Prepaid card\n5\E-Wallet\n6\Banking\nMethod for payment: '))
            if method == 1: 
                method = 'Cash'
                break
            elif method == 2: 
                method = 'Credit card'
                break
            elif method == 3: 
                method = 'Debit card'
                break
            elif method == 4: 
                method = 'Prepaid card'
                break
            elif method == 5: 
                method = 'E-Wallet'
                break
            elif method == 6: 
                method = 'Banking'
                break
            else: print('Enter a number in list.')
        except ValueError:
            print('Enter a number in list.')
    update_method = f"UPDATE bill SET method = '{method}' WHERE id = {bill_id}"
    database.execute(update_method)
    connect.commit()
    print('Bill created successfully.')

def show(value = None):
    format(menuFunction.view('*','bill',value))

def createAuto(customer, drink, quantity, method):
    query = "INSERT INTO bill (customer, total, method, date) VALUES (%s,%s,%s, NOW())"
    database.execute(query, (customer,0,'Cash',))
    connect.commit()
    database.execute("SELECT LAST_INSERT_ID()")
    bill_id = database.fetchone()[0]
    for d, q in zip(drink,quantity):
        orders.append(bill_id,d,q)
    update_total = "UPDATE bill SET total = (SELECT SUM(total) FROM orders WHERE orders.bill_id = bill.id) WHERE id = %s"
    database.execute(update_total,(bill_id,))
    connect.commit()
    if method == 1: method = 'Cash'
    elif method == 2: method = 'Credit card'
    elif method == 3: method = 'Debit card'
    elif method == 4: method = 'Prepaid card'
    elif method == 5: method = 'E-Wallet'
    elif method == 6: method = 'Banking'
    update_method = f"UPDATE bill SET method = '{method}' WHERE id = {bill_id}"
    database.execute(update_method)
    connect.commit()


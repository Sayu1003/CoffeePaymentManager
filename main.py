import mysql.connector
import os
import re

import menuFunction
import bill
import drinks_menu
import orders
import AutoAddDatabase

connect, database = menuFunction.connection()

def help():
    print("""add d <điền tên> <điền giá>: thêm dữ liệu vào bảng đồ uống.
new b: tạo mới hóa đơn mới.
view <b or d> (with) [điều kiện 1] (and) [điều kiện 2] ...: xem dữ liệu bảng hóa đơn (b) hoặc đồ uống (d) -> (Nếu không có điều kiện nó sẽ hiện tất cả).
del <b or d> (with) [điều kiện 1] (and) [điều kiện 2] ...: xóa dữ liệu bảng hóa đơn (b) hoặc đồ uống (d) (Nếu không điều kiện nó sẽ xóa tất cả)
up <b or d> [<Cột> = <Giá trị>] with <điều kiện 1> (and) [điều kiện 2] ...: cập nhật dữ liệu bảng hóa đơn (b) hoặc đồ uống (d).
renueve: Xem doanh thu và số lượng bán hàng.
cls: dọn bảng terminal.
exit: thoát khỏi chương trình.
          
AAD: tự động thêm dữ liệu được tạo sẵn.
""")
def menu():
    os.system('cls')
    print("Enter 'help' to show command if you need\n")
    while True:
        try:
            n = input("Coffeepayment -> ")
            n = n.strip()
            if n == 'help':
                help()
            elif n.startswith("add d"):
                value = n.split()
                price = value[-1]
                name = ' '.join(value[2:-1])
                if len(value) < 4 or name == ' ':
                   print('Please enter NAME and PRiCE.\nExample: add d Latte 75000')
                   continue
                try:
                   price = int(price)
                   drinks_menu.append(name,price)
                   print("Add successfully")
                except ValueError:
                   print("Price must be a number.")
                   continue
            elif n == "new b" or n == 'New b':
                drinks_menu.show()
                bill.create()
            elif n.startswith("view") or n.startswith('View'):
                value = n.split()
                if len(value) == 2:
                    if value[1] =='d':
                        drinks_menu.show()
                    elif value[1] == 'b':
                        bill.show()
                    else:
                        print("Example: view b with id > 5 and total > 75000\nExample: view d with id = 'DR0001' and price >= 20000")
                elif len(value) > 2 and value[2] == 'with':
                    conditions = n.split("with", 1)[1].strip()
                    get_condition =  conditions.split('and')
                    if value[1] =='d':
                        drinks_menu.show(get_condition)
                    elif value[1] == 'b':
                        bill.show(get_condition)
                    else:
                        print("Example: view b with id > 5 and total > 75000\nExample: view d with id = 'DR0001' and price >= 20000")
                else:
                    print("Example: view b with id > 5 and total > 75000\nExample: view d with id = 'DR0001' and price >= 20000")
            elif n.startswith("del") or n.startswith('Del'):
                value = n.split()
                if len(value) == 2:
                    if value[1] =='d':
                        check = input("Are you sure (Y/n): ")
                        if check == 'y' or check == 'Y':
                            menuFunction.delete('drinks',None)
                            print('Deleted all.')
                        else:
                            print("Cancel delete.")
                    elif value[1] == 'b':
                        check = input("Are you sure (Y/n): ")
                        if check == 'y' or check == 'Y':
                            menuFunction.delete('bill',None)
                            database.execute('ALTER TABLE bill AUTO_INCREMENT = 1')
                            connect.commit()
                            print('Deleted all.')
                        else:
                            print("Cancel delete.")
                    else:
                        print("Example: del b with id > 5 and total > 75000\nExample: del d with id = 'DR0001' and price >= 20000")
                elif len(value) > 2 and value[2] == 'with':
                    conditions = n.split("with", 1)[1].strip()
                    get_condition = conditions.split('and')
                    if value[1] == 'd':
                        menuFunction.delete('drinks',get_condition)
                    elif value[1] == 'b':
                        menuFunction.delete('bill',get_condition)
                    else:
                        print("Example: del b with id > 5 and total > 75000\nExample: del d with id = 'DR0001' and price >= 20000")
                else:
                    print("Example: del b with id > 5 and total > 75000\nExample: del d with id = 'DR0001' and price >= 20000")
            elif n.startswith('up') or n.startswith('Up'):
                value = n.split()
                if len(value) > 2:
                    get_value = n.split(' ',2)[2].strip()
                    new = get_value.split('with')[0]
                    conditions = get_value.split('with')[1].split('and')
                    if value[1] == 'd':
                        menuFunction.update(conditions,new,'drinks')
                    elif value[1] == 'b':
                        menuFunction.update(conditions,new,'bill')
                    else:
                        print("Example for up: up d price with id = 'DR0001' and price > 20000 ")
                else:
                    print("Example for up: up d price with id = 'DR0001' and price > 20000")
            elif n == 'renueve' or n == 'Renueve':
                menuFunction.renueve()
            elif n == 'AAD' or n == 'aad':
                AutoAddDatabase.get()
            elif n == 'cls' or n == 'Cls':
                os.system('cls')
                print("Enter 'help' to show command if you need\n")
            elif n == 'exit' or n == 'Exit':
                menuFunction.close_connection(connect,database)
                print('Well done!')
                break
            else:
                print('Command not found!.')
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Start the menu
menu() 
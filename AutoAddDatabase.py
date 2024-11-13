import mysql.connector
import random\

import menuFunction
import bill
import drinks_menu
import orders

connect, database = menuFunction.connection()

def get():
    name = ['CÀ PHÊ ĐEN','CÀ PHÊ SỮA','TRÀ ĐÀO','TRÀ TẮC XÍ MUỘI','TRÀ VẢI','TRÀ SỮA','TRÀ XANH','SÔ-CÔ-LA','AQUAFINA','LATTE','CAPPUCCINO','DỪA TƯƠI']
    price = [55000,65000,65000,65000,65000,50000,75000,75000,30000,75000,75000,55000]
    for n,p in zip(name,price):
        drinks_menu.append(n,p)
    
    customer = ['Trần Hà Linh','Nguyễn Minh Tuấn','Trần Thị Lan','Bùi Ngọc Linh','Ngô Thị Thu Hương','Vũ Hoàng Nam','Nguyễn Thị Thanh Bình']
    for c in customer:
        cus1, cus2 = random.randint(0, 11), random.randint(0, 11)
        q1, q2 = random.randint(1, 9), random.randint(1, 9)
        method = random.randint(1,6)
        bill.createAuto(c, [name[cus1], name[cus2]], [q1, q2], method)
    print('Successflly')


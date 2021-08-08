#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS stock (
#         id INTEGER PRIMARY KEY,
#         symbol TEXT NOT NULL UNIQUE,
#         company TEXT NOT NULL,
#         nse_name TEXT NOT NULL
#     )
# """)
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS stock_price (
#         id INTEGER PRIMARY KEY,
#         stock_id INTEGER,
#         date NOT NULL,
#         open NOT NULL,
#         high NOT NULL,
#         low NOT NULL,
#         close NOT NULL,
#         adjusted_close NOT NULL,
#         volume NOT NULL,
#         FOREIGN KEY (stock_id) REFERENCES stock (id)
#     )
# """)
#
# connection.commit()
#



# import sqlite3
# excel_file = r'C:\Users\raj\Desktop\my trade.xls'
# import pandas as pd
# connection = sqlite3.connect("app.db")
# cursor = connection.cursor()
#
# df = pd.read_excel(excel_file, sheet_name='yahoofinance_mapping')
# dftolist = df.values.tolist()
# class Stock:
#     def __init__(self, symbol, company):
#         self.symbol = symbol
#         self.company = company
#
# stocks = []
# for item in dftolist:
#     stocks.append(Stock(item[0],item[1]))
#
# for stock in stocks:
#     # print(asset)
#
#     cursor.execute("""
#             INSERT INTO stock (symbol, company)
#             VALUES (?, ?)
#     """, (stock.symbol, stock.company))
#
# connection.commit()
import numpy as np

excel_file = r'C:\Users\raj\Desktop\TorisProductionOrder\TPF PLANT PRO DAY. SHEET.xlsm'
excel_file_plant_production = r'C:\Users\raj\Desktop\plant production.csv'
excel_file_order = r'C:\Users\raj\Desktop\order.csv'
import pandas as pd
import time,psycopg2
import datetime
from datetime import date
from datetime import datetime
from nsepy import get_history
pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 50)
today = datetime.today()
params = {
    "host": "localhost",
    "database": "toris",
    "user": "postgres",
    "password": "raja"
    }

class Product:
    def __init__(self,color_code_no ,color_marking_on_bobin, tape_color, denier, gramage,
                 tape_width, cutter_spacing,stock_of_bobin,streanth_per_tape_in_kg,elongation,
                 tanacity,pp,filler,shiner,color,TPT,UV,color_name,is_deleted):
        self.color_code_no = color_code_no
        self.color_marking_on_bobin = color_marking_on_bobin
        self.tape_color=tape_color
        self.denier = denier
        self.gramage = gramage
        self.tape_width = tape_width
        self.cutter_spacing = cutter_spacing
        self.stock_of_bobin = stock_of_bobin
        self.streanth_per_tape_in_kg = streanth_per_tape_in_kg
        self.elongation = elongation
        self.tanacity = tanacity
        self.pp = pp
        self.filler = filler
        self.shiner = shiner
        self.color = color
        self.TPT = TPT
        self.UV = UV
        self.color_name = color_name
        self.is_deleted = is_deleted

class PlantProduction:
    def __init__(self,date, shift,  no_of_winderman, end_reading,start_reading,wastage, operator_name,plant,
                 product_code,is_deleted):

        self.date = date
        self.shift=shift
        self.operator_name = operator_name
        self.no_of_winderman = no_of_winderman
        self.product_code = product_code
        self.end_reading = end_reading
        self.start_reading = start_reading
        self.plant = plant
        self.wastage = wastage
        self.is_deleted = is_deleted

class Order:
    def __init__(self,order_date, customer_name,  product_code, order_qty,pi_number,is_deleted):

        self.order_date = order_date
        self.customer_name=customer_name
        self.product_code = product_code
        self.order_qty = order_qty
        self.product_code = product_code
        self.pi_number = pi_number
        self.is_deleted = is_deleted



def Product_List():
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT * FROM toris_product
        """)
    rows = cursor.fetchall()
    product_list = [row[0] for row in rows]
    return product_list



def insert_production_table() :

    df = pd.read_csv(excel_file_plant_production)
    df = df.replace([np.NAN],0)
    df = df.astype(
        {'date': 'datetime64[ns]'})
    dftolist = df.values.tolist()
    print(dftolist)
    productions = []

    for item in dftolist:
        productions.append(PlantProduction(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                         item[8], item[9]))

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    for production in productions:

        try:

                cursor.execute("""
                                INSERT INTO toris_plantproduction (date, shift, no_of_winderman,  
                                 end_reading, start_reading, wastage, operator_name_id, plant_id,
                                 product_code_id, is_deleted)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (production.date,production.shift,production.no_of_winderman,production.end_reading,
                              production.start_reading,production.wastage,production.operator_name,production.plant,
                              production.product_code,production.is_deleted))
                print(f"Added production no - {production.product_code} successfully into plant production table")
        except (Exception, psycopg2.Error) as error:
            print(f"{production.product_code} Failed to insert  into plant production table", error)

    connection.commit()

def insert_order_table() :

    df = pd.read_csv(excel_file_order)
    df = df.replace([np.NAN],0)
    df = df.astype({'order_date': 'datetime64[ns]'})
    dftolist = df.values.tolist()
    print(dftolist)
    orders = []

    for item in dftolist:
        orders.append(Order(item[0], item[1], item[2], item[3], item[4], item[5]))

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    print(orders)
    for order in orders:

        try:

                cursor.execute("""
                                INSERT INTO toris_order (order_date, customer_name, product_code_id,  
                                 order_qty, pi_number,is_deleted)
                                VALUES (%s,%s,%s,%s,%s,%s)
                        """, (order.order_date,order.customer_name,order.product_code,order.order_qty,
                              order.pi_number,order.is_deleted))
                print(f"Added order no - {order.customer_name} successfully into order table")
        except (Exception, psycopg2.Error) as error:
            print(f"{order.customer_name} Failed to insert  into order table", error)

    connection.commit()



def insert_product_table() :
    product_list = Product_List()
    df = pd.read_excel(excel_file, sheet_name='color_code')
    df = df.replace([np.NAN],0)
    dftolist = df.values.tolist()
    print(dftolist)
    productds = []

    for item in dftolist:
        productds.append(Product(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                         item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15],
                                         item[16], item[17], item[18]))

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    for product in productds:
        print(product.color_code_no)
        try:
            if product.color_code_no not in product_list:
                cursor.execute("""
                                INSERT INTO toris_product (product_code, color_marking_on_bobin, tape_color, 
                                denier, gramage, tape_width, cutter_spacing, stock_of_bobin,
                                streanth_per_tape_in_kg, elongation_percent,  tanacity,pp_percent,
                                filler_percent, shiner_percent, color_percent, tpt_percent, uv_percent, 
                                color_name,is_deleted)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (product.color_code_no,product.color_marking_on_bobin,product.tape_color,
                              product.denier,product.gramage,product.tape_width,product.cutter_spacing,
                              product.stock_of_bobin,product.streanth_per_tape_in_kg,product.elongation,
                              product.tanacity,product.pp,product.filler,product.shiner,product.color,
                              product.TPT,product.UV,product.color_name,product.is_deleted))
                print(f"Added color code no - {product.color_code_no} successfully into product table")
        except (Exception, psycopg2.Error) as error:
            print(f"{product.color_code_no} Failed to insert  into product table", error)

    connection.commit()

if __name__ == '__main__':

    # insert_product_table()
    # insert_production_table()
    # insert_order_table()
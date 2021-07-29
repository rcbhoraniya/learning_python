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

class PlantProduction:
    def __init__(self,color_marking_on_bobin, tape_color, color_code_no , req_denier, req_gramage,
                 req_tape_width, cutter_spacing,stock_of_bobin,req_streanth_per_tape_in_kg,req_elongation,streanth,
                 tanacity,pp,filler,shiner,color,TPT,UV,color_name):

        self.color_marking_on_bobin = color_marking_on_bobin
        self.tape_color=tape_color
        self.color_code_no = color_code_no
        self.req_denier = req_denier
        self.req_gramage = req_gramage
        self.req_tape_width = req_tape_width
        self.cutter_spacing = cutter_spacing
        self.stock_of_bobin = stock_of_bobin
        self.req_streanth_per_tape_in_kg = req_streanth_per_tape_in_kg
        self.req_elongation = req_elongation
        self.streanth = streanth
        self.tanacity = tanacity
        self.pp = pp
        self.filler = filler
        self.shiner = shiner
        self.color = color
        self.TPT = TPT
        self.UV = UV
        self.color_name = color_name
def Product_List():
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT * FROM toris_product
        """)
    rows = cursor.fetchall()
    product_list = [row[0] for row in rows]
    return product_list

def insert_product_table() :
    product_list = Product_List()
    df = pd.read_excel(excel_file, sheet_name='color_code')
    df = df.replace([np.NAN],0)
    dftolist = df.values.tolist()
    # print(dftolist)
    productds = []

    for item in dftolist:
        productds.append(PlantProduction(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],
                                         item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15],
                                         item[16], item[17], item[18]))

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    for productd in productds:
        print(productd.color_code_no)
        try:
            if productd.color_code_no not in product_list:
                cursor.execute("""
                                INSERT INTO toris_product (product_code, color_marking_on_bobin, tape_color, 
                                req_denier, req_gramage, req_tape_width, cutter_spacing, stock_of_bobin,
                                req_streanth_per_tape_in_kg, req_elongation_percent, streanth, tanacity,pp_percent,
                                filler_percent, shiner_percent, color_percent, tpt_percent, uv_percent, color_name)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (productd.color_code_no,productd.color_marking_on_bobin,productd.tape_color,productd.req_denier,
                              productd.req_gramage,productd.req_tape_width,productd.cutter_spacing,productd.stock_of_bobin,
                              productd.req_streanth_per_tape_in_kg,productd.req_elongation,productd.streanth,productd.tanacity,
                              productd.pp,productd.filler,productd.shiner,productd.color,productd.TPT,productd.UV,productd.color_name))
                print(f"Added color code no - {productd.color_code_no} successfully into product table")
        except (Exception, psycopg2.Error) as error:
            print(f"{productd.color_code_no} Failed to insert  into product table", error)

    connection.commit()

if __name__ == '__main__':

    insert_product_table()


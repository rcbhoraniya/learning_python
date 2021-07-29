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
excel_file = r'C:\Users\raj\Desktop\my trade.xls'
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
from datetime import datetime
import yfinance as yf
from pandas_datareader import data as web
import requests
params = {
    "host": "localhost",
    "database": "app",
    "user": "raj",
    "password": "raja"
    }



class Stock:
    def __init__(self, yahoo_symbol, name, nse_symbol):

        self.yahoo_symbol = yahoo_symbol
        self.name = name
        self.nse_symbol = nse_symbol
class Stock_Price:
    def __init__(self, date,  open, high, low , close, prev_close, volume, deliverable_volume,stock_id,):
        self.stock_id = stock_id
        self.date = date
        self.prev_close=prev_close
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.deliverable_volume = deliverable_volume
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE stock (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(50) NOT NULL,
            company VARCHAR(200) NOT NULL,
            nse_name VARCHAR(50) NOT NULL
        )
        """,
        """
    CREATE TABLE IF NOT EXISTS stock_price (
        id SERIAL PRIMARY KEY,
        stock_id INTEGER NOT NULL,
        date date NOT NULL,
        prev_close numeric NOT NULL,
        open numeric NOT NULL,
        high numeric NOT NULL,
        low numeric NOT NULL,
        close numeric NOT NULL,
        volume integer NOT NULL,
        deliverable_volume integer NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
        """
        )
    conn = None
    try:

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def Symbol_List():
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    cursor.execute("""
            SELECT yahoo_symbol, name ,nse_symbol FROM stockapp_stock
        """)
    rows = cursor.fetchall()
    symbols_list = [row[2] for row in rows]
    # for row in rows:
    #     print(row[0])
    return symbols_list

def insert_stock_table() :

    symbols = Symbol_List()
    df = pd.read_excel(excel_file, sheet_name='yahoofinance_mapping')
    dftolist = df.values.tolist()
    stocks = []

    for item in dftolist:
        stocks.append(Stock(item[0], item[1], item[2]))

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    for stock in stocks:
        # print(asset)

        try:
            if stock.nse_symbol not in symbols:
                cursor.execute("""
                                INSERT INTO stockapp_stock (yahoo_symbol, name, nse_symbol)
                                VALUES (%s,%s,%s)
                        """, (stock.nse_symbol, stock.name, stock.nse_symbol))
                print(f"Added new {stock.nse_symbol}{stock.name} successfully into stock table")
        except (Exception, psycopg2.Error) as error:
            print(f"{stock.nse_symbol} Failed to insert  into stock table", error)

    connection.commit()
def convert(val):
    new_val = val.replace("/", "-")
    return str(new_val)

def load_data_in_stock_price():
    symbols = []
    stock_dict = {}
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()
    cursor.execute("""
            SELECT * FROM stockapp_stock
        """)
    rows = cursor.fetchall()
    for row in rows:
        symbol = row[3]
        symbols.append(symbol)
        stock_dict[symbol] = row[0]
    cursor.execute("""
                SELECT DISTINCT stock_id_id,date FROM stockapp_stock_price
            """)
    datas = cursor.fetchall()
    list_stock_id = [data[0] for data in datas]
    list_stock_id.sort()
    list_dates = [data[1] for data in datas]
    list_dates.sort()

    if len(list_dates) == 0 :
        start_date = pd.to_datetime('2011-01-01')
        end_date = today
    else:
        end_date = list_dates[len(list_dates) - 1]
        start_date = list_dates[0]
    print(end_date)
    print(start_date)
    print(stock_dict)
    for symbol in symbols:
        stock_prices = []
        stock_id = stock_dict[symbol]
        if stock_id not in list_stock_id:

            df = get_history(symbol=symbol,
                             start=date(start_date.year, start_date.month, start_date.day),
                             end=date(today.year, today.month, today.day))
            df['Date'] = df.index
            df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Prev Close', 'Volume', 'Deliverable Volume']]

        else:
            if today != end_date:
                # print(stock_id)
                df = get_history(symbol=symbol,
                                 start=date(end_date.year, end_date.month, end_date.day+1 ),
                                 end=date(today.year, today.month, today.day))
                df['Date'] = df.index
                df = df[['Date',  'Open', 'High', 'Low', 'Close', 'Prev Close','Volume', 'Deliverable Volume']]

            else:
                print(f'{stock_id}-is already uptodate')
                break
        DfToList = df.values.tolist()

        for item in DfToList:
            stock_prices.append(
                Stock_Price(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7],stock_id))

        for stock_price in stock_prices:
            cursor.execute("""
                                INSERT INTO stockapp_stock_price ( date, open, high, low, close, prev_close, volume,delivary_volume,stock_id_id)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """, (
            stock_price.date, stock_price.open, stock_price.high,
            stock_price.low, stock_price.close, stock_price.prev_close,
            stock_price.volume, stock_price.deliverable_volume ,stock_price.stock_id,))

            connection.commit()
        print(f"Processing -{symbol}")

        # time.sleep(1)

    connection.close()

if __name__ == '__main__':

    # create_tables()
    # insert_stock_table()
    load_data_in_stock_price()
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute("""
                SELECT * FROM stockapp_stock
            """)
    stocks = cursor.fetchall()
    stock_list = [stock[3] for stock in stocks]
    print(stock_list)
    for ticker in stock_list:
        symbol = ticker
        command = f"SELECT nse_symbol, date, open, high, low, close FROM stockapp_stock_price JOIN stockapp_stock on stockapp_stock.id = stockapp_stock_price.stock_id_id WHERE nse_symbol = '{symbol}' ORDER BY date"
        cursor.execute(command)

        rows = cursor.fetchall()
        # print(symbol)
        # print(rows)
        if len(rows) ==0:
            rows=[[ticker,0,0,0,0,0]]
            df = pd.DataFrame(rows)
            df.columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close']
            print(df)
        else:
            df = pd.DataFrame(rows)
            df.columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close']
            print(df)
        # datas = []
        # for row in rows:
        #     data = [row[0],row[1],row[2],row[3],row[4],row[5]]
        #     datas.append(data)
        #
        # if len(datas)==0:
        #     datas = [[ticker,0,0,0,0,0]]
        #     df=pd.DataFrame(datas)
        # df = pd.DataFrame(datas)
        # df.columns = ['Symbol','Date','Open','High','Low','Close']
        #
        # records = df.to_records()
        # print(records)
        # nse_name = row[0]
        # date = row[1]
        # open = row[2]
        # high = row[3]
        # low = row[4]
        # close = row[5]
        # print(f"nse_name={nse_name}-date={date}-open={open}-high={high}-low={low}-close={close}")
    # SELECT
    # nse_symbol, date, open, high, low, close
    # FROM
    # stockapp_stock_price
    # JOIN
    # stockapp_stock
    # on
    # stockapp_stock.id = stockapp_stock_price.stock_id_id
    # WHERE
    # nse_symbol = 'ASIANPAINT'
    # ORDER
    # BY
    # date
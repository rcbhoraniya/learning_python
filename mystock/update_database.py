import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import xlsxwriter
from datetime import datetime, timedelta, date
import yfinance as yf

pd.set_option('display.width', 1500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 50)

filepath = r'C:\Users\raj\Desktop\my_trade.xlsx'
conn_string = "postgresql://postgres:raja@localhost:5432/stockdb"

to_day = datetime.now()
today = datetime.now().strftime('%Y-%m-%d')
cday = today
t = ' 15:31:00'
today = today + t
today = pd.to_datetime(today)

def convert_lower(list):
    col = []
    for item in list:
        i = item.lower()
        v = i.replace(" ", "_")
        col.append(v)
    return col
def str_to_float(string):
    bad_chars = [';', ':', '!', "*",
                 '?', '/', '₹', ',']
    test_string = string
    for i in bad_chars:
        test_string = test_string.replace(i, '')

    return float(test_string)

conn = create_engine(conn_string).connect()

# df = pd.read_sql(
#     f'SELECT date,company_name, side, quantity, price FROM stocks_stockmap INNER JOIN stocks_stockdata ON stocks_stockmap.id=stocks_stockdata.company_id  ORDER BY date DESC LIMIT 1',
#     con=conn)
# obj = df.to_records(index=False)
#
# last_date_db = obj[0].date
# last_stock_name = obj[0].company_name
# print(f'Last Date of Data Entry is {last_date_db} and Name is {last_stock_name} ')
#
#
# df = pd.read_excel(filepath, sheet_name="Data")
# column = convert_lower(list(df.columns))
# df.columns = column
# df['price'] = df['price'].apply(str_to_float)
# # print(df)
# df = df.astype({'date': 'str', 'trade_time': 'str'})
# df['DateAndTime'] = df['date'].str.cat(df['trade_time'], sep=" ")
# df['date'] = pd.to_datetime(df['DateAndTime'])
# df = df.drop(columns=['DateAndTime'])
# df.sort_values("date", inplace=True)
# df = df.reset_index(drop='index')
# # sorting by first name
# df = df.replace([np.nan], 0.0)
# df['side'] = df['side'].map({'B': 1, 'S': -1, 'Buy': 1, 'Sell': -1})
# df = df.astype(
#     {'date': 'datetime64[ns]', 'company': 'str', 'trade_num': 'int64', 'side': 'int', 'quantity': 'int',
#      'price': 'float'})
#
# df = df.drop_duplicates(keep='first')
# col = df.columns
# df = df[
#     ['date',  'side', 'quantity', 'price', 'trade_num','company',]]
#
# # print(df)
# if df.empty:
#
#     print(f'There is no Data in {filepath} for Upload in stock_purchase_data table')
#     ans = input(f'Enter any key for continue....... ')
#     pass
# else:
#     map_df = pd.read_sql(f'SELECT * FROM stocks_stockmap ORDER BY company_name', con=conn)
#     # print(map_df)
#     df = df.merge(map_df, left_on='company', right_on='company_name', how='left').drop(
#         columns=['company_name', 'company','is_portfolio_stock'])
#     # print(df)
#     df.rename(columns={'id': 'company_id'}, inplace=True)
#     df = df[['is_deleted','deleted_at','date', 'side', 'quantity', 'price', 'trade_num','company_id']]
#     print(df)
#     # df.to_sql(con=conn, name='stocks_stockdata', if_exists='append', index=False)
#
#     # dfe = pd.DataFrame(columns=col)
#     # outXLSX = pd.ExcelWriter(filepath, engine='xlsxwriter')
#     # dfe.to_excel(outXLSX, sheet_name='Data', index=False)
#     # while True:
#     #     try:
#     #         outXLSX.save()
#     #     except xlsxwriter.exceptions.FileCreateError as e:
#     #         # For Python 3 use input() instead of raw_input().
#     #         decision = input("Exception caught in workbook.close(): %s\n"
#     #                          "Please close the file if it is open in Excel.\n"
#     #                          "Try to write file again? [Y/n]: " % e)
#     #         if decision != 'n':
#     #             continue
#     #
#     #     break
#
# ans = input("Are you want to Update Historical Price data (yes/no) : ")
# if ans == "yes" or ans == "y":
#     map_df = pd.read_sql(f'SELECT * FROM stocks_stockmap WHERE is_portfolio_stock = True ORDER BY company_name', con=conn)
#     yahoo_symbol_list = zip(map_df['id'].to_list() , map_df['yahoo_symbol'].to_list())
#     print(yahoo_symbol_list)
#     for i, (stock_id, ticker) in enumerate(yahoo_symbol_list):
#
#         name = ticker[:-3].lower()
#
#         print(f' {name}')
#         if datetime.today() < today:
#             end_date = datetime.today() - timedelta(days=1)
#         else:
#             end_date = datetime.today()
#
#         df = pd.read_sql(
#             f'SELECT date,open,high,low,close,adj_close,volume FROM historical_data WHERE company = {stock_id} ORDER BY date DESC LIMIT 1',
#             con=conn)
#         if df.empty:
#             start_date = date(2001, 1, 1)
#         else:
#             obje = df.to_records(index=False)
#             start_date = obje[0].date
#             start_date = pd.to_datetime(start_date)
#             start_date += timedelta(days=1)
#         if start_date > end_date:
#             print(f"Already Upto Date no need to update")
#             pass
#         else:
#             print(start_date, end_date)
#             df = yf.download(ticker, start=start_date, end=end_date)
#             df['Date'] = df.index
#             df['company_id'] = stock_id
#             df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
#             column = convert_lower(list(df.columns))
#             df.columns = column
#             df = df[[ 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume','company_id']]
#             print("df", df)
#             # df.to_sql(con=conn, name='stocks_historicaldata', if_exists='append', index=False)
#
#
# else:
#     pass
#





# csv = r'C:\Users\raj\Desktop\stocks_sector.csv'
# df = pd.read_csv(csv)
# df = df.drop(columns='id')
# df.to_sql(con=conn, name='stocks_sector', if_exists='append', index=False)
#
# print(df)

# csv = r'C:\Users\raj\Desktop\stocks_stockmap.csv'
# df = pd.read_csv(csv)
# df = df.drop(columns='id')
# df = df[['is_deleted','deleted_at','company_name','nse_symbol','moneycontrol_symbol','yahoo_symbol','scrip_code','is_portfolio_stock','m_cap_id','sector_id']]
# df.to_sql(con=conn, name='stocks_stockmap', if_exists='append', index=False)
#
# print(df)

# csv = r'C:\Users\raj\Desktop\stocks_stockdata.csv'
# df = pd.read_csv(csv)
# df = df.drop(columns='id')
# df.to_sql(con=conn, name='stocks_stockdata', if_exists='append', index=False)
#
# print(df)

# csv = r'C:\Users\raj\Desktop\stocks_historicaldata.csv'
# df = pd.read_csv(csv)
# df = df.drop(columns='id')
# df.to_sql(con=conn, name='stocks_historicaldata', if_exists='append', index=False)
#
# print(df)

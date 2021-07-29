import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from gspread_pandas import Spread, Client
from google.oauth2.service_account import Credentials
excel_out_file = r'C:\Users\raj\Desktop\stock.xlsx'

df = pd.read_excel(excel_out_file, sheet_name='Portfolio')
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

docid = "178fDdajaXZm8SbguxQQi2J5mZz-tZ8LIhTXIDlJH_LU"
wb_name = '15XwsT5WNgVM6x2otkEom-8Nu0vu1yYEHwpVrK3sESvE'
client = gspread.authorize(credentials)

# spreadsheet = client.open_by_key(docid)
spreadsheet= client.open_by_key(docid).get_worksheet(0).get_all_records()
# print(spreadsheet)
# fr = pd.DataFrame(spreadsheet)
# print(fr)
# result = spreadsheet.get_all_records()
# worksheet = spreadsheet.get_worksheet()

# data = worksheet.get_all_values()
df1 = pd.DataFrame(spreadsheet)
print(df)
# print(df1)
df1 = df1.merge(df, left_on='nse_name', right_on='nse_name',
                   how='left').drop(columns=['nse_name'])
# df1.to_excel("gsheet.xlsx",index=False)
df1 = df1[['sr No.','Stock Code','Company','Sector','Market Cap','Holdings_y','buy_average']]
print(df1)
# print(df.info())
# # df['2'].dtype(int)
# df.to_excel("gsheet.xlsx",index=False)
# filename = wb_name + '-worksheet' + str(0) + '.csv'
# f = open(filename, 'w')
# writer = csv.writer(f)
# writer.writerows(worksheet.get_all_values())

# for i, worksheet in enumerate(spreadsheet.worksheets()):
#     filename = docid + '-worksheet' + str(i) + '.csv'
#     with open(filename, 'w') as f:
#         writer = csv.writer(f)
#         writer.writerows(worksheet.get_all_values())
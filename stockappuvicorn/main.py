import uvicorn
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
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import JSONResponse
params = {
    "host": "localhost",
    "database": "app",
    "user": "raj",
    "password": "raja"
    }

app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def index(request:Request):

    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute("""
                    SELECT * FROM stockapp_stock
                """)
    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html",{"request":request,"stocks":rows})
    # return {"title":"dashbord","stocks":rows}
@app.get("/stock/{symbol}")
def stock_detail(request:Request,symbol):
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    cursor.execute("""
                        SELECT * FROM stockapp_stock WHERE nse_symbol = %s
                    """,(symbol,))
    row = cursor.fetchone()

    return templates.TemplateResponse("detail.html", {"request": request, "stock": row})

plant_csv = r'C:\Users\raj\Desktop\Toris\plant.csv'
plant_production_csv = r'C:\Users\raj\Desktop\Toris\plant_production.csv'
order_csv = r'C:\Users\raj\Desktop\Toris\order.csv'
operator_csv = r'C:\Users\raj\Desktop\Toris\operator.csv'
product_csv = r'C:\Users\raj\Desktop\Toris\product.csv'


import csv
import psycopg2

params = {
    "host": "localhost",
    "database": "toris",
    "user": "postgres",
    "password": "raja"
    }

def plant_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(plant_csv, 'r') as f:
        data = csv.reader(f)
        next(data) # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute( """INSERT INTO toris_plant(name,is_deleted) VALUES (%s,%s)""", row)
    conn.commit()

def plant_Production_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(plant_production_csv, 'r') as f:
        data = csv.reader(f)
        next(data) # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute( """INSERT INTO toris_plantproduction(date,shift,no_of_winderman,end_reading,
            start_reading,wastage,operator_name_id,plant_id,product_code_id,is_deleted) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", row)
    conn.commit()

def operator_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(operator_csv, 'r') as f:
        data = csv.reader(f)
        next(data) # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute( """INSERT INTO toris_operator(name,is_deleted)
            VALUES (%s,%s)""", row)
    conn.commit()

def product_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(product_csv, 'r') as f:
        data = csv.reader(f)
        next(data) # Skip the header row.
        print(data)

        for row in data:
            # row = ['0' if x == 'NULL' else x for x in row]
            print(row)
            cur.execute( """INSERT INTO toris_product(product_code,color_marking_on_bobin,
            tape_color,denier,gramage,tape_width,cutter_spacing,stock_of_bobin,streanth_per_tape_in_kg,
            elongation_percent,tanacity,pp_percent,filler_percent,shiner_percent,color_percent,tpt_percent,
            uv_percent,color_name,is_deleted)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", row)
    conn.commit()

def order_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(order_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_order(order_date,customer_name,
            product_code_id,order_qty,pi_number,is_deleted)
            VALUES (%s,%s,%s,%s,%s,%s)""", row)
    conn.commit()

if __name__ == '__main__' :

    plant_upload()
    operator_upload()
    product_upload()
    order_upload()
    plant_Production_upload()



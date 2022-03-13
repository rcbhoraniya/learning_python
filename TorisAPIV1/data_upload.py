
import psycopg2
import csv
plant_csv = r'C:\Users\raj\Desktop\Toris\plant.csv'
plant_production_csv = r'C:\Users\raj\Desktop\Toris\plant_production.csv'
order_csv = r'C:\Users\raj\Desktop\Toris\order.csv'
employee_csv = r'C:\Users\raj\Desktop\Toris\employee.csv'
product_csv = r'C:\Users\raj\Desktop\Toris\product.csv'
designation_csv = r'C:\Users\raj\Desktop\Toris\designation.csv'
state_csv = r'C:\Users\raj\Desktop\Toris\state.csv'
districts_csv = r'C:\Users\raj\Desktop\Toris\state_districts.csv'
union_teratories_csv = r'C:\Users\raj\Desktop\Toris\union teratories.csv'
union_district =  r'C:\Users\raj\Desktop\Toris\union_teritories_distics.csv'
country_csv = r'C:\Users\raj\Desktop\Toris\country.csv'
params = {
    "host": "localhost",
    "database": "torisapi",
    "user": "postgres",
    "password": "raja"
}


def plant_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(plant_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute(
                """INSERT INTO toris_plant(name,is_deleted) VALUES (%s,%s)""", row)
    conn.commit()


def designation_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(designation_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute(
                """INSERT INTO toris_designation(designation,is_deleted) VALUES (%s,%s)""", row)
    conn.commit()


def plant_Production_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(plant_production_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute("""INSERT INTO toris_plantproduction(date,shift,no_of_winderman,end_reading,start_reading,wastage,operator_name_id,plant_id,product_code_id,is_deleted) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", row)
    conn.commit()


def employee_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(employee_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:
            print(row)
            cur.execute("""INSERT INTO toris_employee(name,mname,lname,city,state_id,district_id,address,
            mobile1,mobile2,aadhhar_no,designation_id,photo_image,is_deleted)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", row)
    conn.commit()


def product_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(product_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:
            # row = ['0' if x == 'NULL' else x for x in row]
            print(row)
            cur.execute("""INSERT INTO toris_product(product_code,color_marking_on_bobin,
            tape_color,denier,gramage,tape_width,cutter_spacing,stock_of_bobin,streanth_per_tape_in_kg,elongation_percent,tenacity,pp_percent,filler_percent,shiner_percent,color_percent,tpt_percent,uv_percent,color_name,is_deleted)
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

def state_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(state_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_state(name,is_deleted)
            VALUES (%s,%s)""", row)
    conn.commit()

def union_teritories_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(union_teratories_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_state(name,is_deleted)
            VALUES (%s,%s)""", row)
    conn.commit()

def district_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(districts_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_district(code,name,headquarters,state_id,is_deleted)
            VALUES (%s,%s,%s,%s,%s)""", row)
    conn.commit()

def union_district_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(union_district, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_district(code,name,headquarters,state_id,is_deleted)
            VALUES (%s,%s,%s,%s,%s)""", row)
    conn.commit()

def country_upload():

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    with open(country_csv, 'r') as f:
        data = csv.reader(f)
        next(data)  # Skip the header row.
        print(data)

        for row in data:

            print(row)
            cur.execute("""INSERT INTO toris_country(name,un_continental,is_deleted)
            VALUES (%s,%s,%s)""", row)
    conn.commit()
if __name__ == '__main__':
    # country_upload()
    # state_upload()
    # district_upload()
    # plant_upload()
    # designation_upload()
    # employee_upload()
    # product_upload()
    # order_upload()
    # plant_Production_upload()



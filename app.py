from flask import Flask,flash, jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import requests
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener



from datetime import date
from flask import jsonify
import calendar
import os
import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

from dotenv import load_dotenv

from r2connect.r2client import R2Client
from r2connect.exceptions.cloudflare.r2 import ObjectAlreadyExists, ObjectDoesNotExist
import boto3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif','heic'}
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB


app.config['CLOUDFLARE_API_TOKEN'] = 'rBG0XF6-fclPR1uojxYulSSIPHtWJO6Znv0lPF3Z'
app.config['CLOUDFLARE_ACCOUNT_ID'] = 'dad4cd92b66b10176ae784292d55b95c'

# Defining custom filters
def days_diff(end_date, start_date):
    if end_date is None or start_date is None:
        return 'N/A' 
    return (end_date - start_date).days

# Register a custom filter
app.jinja_env.filters['days_diff'] = days_diff


#ACCOUNT_ID: dad4cd92b66b10176ae784292d55b95c
#Token value: lFwIn4vv96cYRiAOZqbJ4Ag0b3QIk8QJjcY7atMT
#Access Key ID 3455257ecd50107af1661ade6a531a9d
#Secret Access Key 4edd7e87535ea96f8fe7844c217b50aa982d31418a2b4a64ef6c7897282dab16
#https://dad4cd92b66b10176ae784292d55b95c.r2.cloudflarestorage.com


dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

register_heif_opener()

try:
    r2_client = R2Client()
except Exception as error:
    # A required environment variable is missing
    print(error)
# except r2connect.exceptions.cloudflare.r2.MissingConfig as error:
#     # A required environment variable is missing
#     print(error)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def upload_to_cloudflare(file_path, filename):
    try:
        try:
            r2_client.upload_file(file_path, filename, "secondhand")
        except Exception as error:
            print(error)
        # with open(file_path, 'rb') as f:
        #     url = f"https://api.cloudflare.com/client/v4/accounts/dad4cd92b66b10176ae784292d55b95c/images/v1"
        #     headers = {
        #         "Authorization": "Bearer rBG0XF6-fclPR1uojxYulSSIPHtWJO6Znv0lPF3Z"
        #     }
        #     files = {
        #         'file': (filename, f)
        #     }
        #     # print(f"URL: {url}")
        #     # print(f"Headers: {headers}")
        #     response = requests.post(url, headers=headers, files=files)
        #     # print(f"Response: {response.text}")
        #     response.raise_for_status()

        #     data = response.json()
        #     if data['success']:
        #         return data['result']['variants'][0]
        #     else:
        #         flash('Failed to upload image to Cloudflare.', 'danger')
        #         return None
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return None





@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            product_name = request.form['product_name']
            category_id = request.form['product_category']
            status_id = request.form['product_status']
            buy_date = request.form['buy_date']
            buy_price = request.form['buy_price']
            buy_platform_id = request.form['buy_platform']
            sell_date = request.form.get('sell_date') or None
            sell_price = request.form.get('sell_price') or None
            sell_platform_id = request.form.get('sell_platform') or None
            fees = request.form.get('fees') or 0
            file = request.files['product_image']
            if file and allowed_file(file.filename):
                connection = getCursor()
                connection.execute("""INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id)
                    VALUES (%s, %s, %s, %s, %s, %s);""",(product_name, category_id, status_id, buy_date, buy_price, buy_platform_id))

                connection.execute("SELECT LAST_INSERT_ID();")
                product_id = connection.fetchone()[0]
                 # Generate a new filename
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{product_id}.{file_ext}"
                # print("new_filename",filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
               
                # Convert HEIC to JPEG if necessary
                if filename.lower().endswith('.heic'):
                    try:
                        img = Image.open(file_path)
                        jpeg_path = file_path.rsplit('.', 1)[0] + '.jpeg'
                        img.save(jpeg_path, "JPEG")
                        os.remove(file_path)  # Remove the original HEIC file
                        file_path = jpeg_path
                        filename = os.path.basename(file_path)
                    except Exception as e:
                        os.remove(file_path)
                        flash('The uploaded HEIC file could not be converted.', 'danger')
                        return redirect(url_for('home'))

                upload_to_cloudflare(file_path, filename)
                # os.remove(file_path)
                connection1 = getCursor()
                connection1.execute("""Update products SET image_url=%s WHERE product_id=%s;""",(filename,product_id,))
                if sell_date and sell_price and sell_platform_id:
                    connection.execute("""INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
                        VALUES (%s, %s, %s, %s, %s);""",(product_id, sell_date, sell_price, sell_platform_id, fees))

                flash('A new product was successfully added!', 'success')
                return redirect(url_for('home'))
        
            else:
                flash('Invalid file format or no file uploaded.', 'danger')
                return redirect(url_for('home'))
                
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('home'))
    else:
        connection1 = getCursor()
        connection1.execute("""SELECT category_id,category_name FROM category;""")
        categoryList = connection1.fetchall()
        connection2 = getCursor()
        connection2.execute("""SELECT status_id,status_name FROM status;""")
        statusList = connection2.fetchall()
        connection3 = getCursor()
        connection3.execute("""SELECT platform_id,platform_name FROM platform;""")
        platformList = connection3.fetchall()
        active_page ="home"
        return render_template("index.html",categoryList=categoryList,statusList=statusList,platformList=platformList,active_page=active_page)



@app.route("/items", methods=["GET"])
def items():
    search_query = request.args.get("search_query", default="", type=str)
    filter = request.args.get("filter","")
    today_date = date.today()
    connection = getCursor()
    if filter:
        if filter == 'today':
            connection.execute("""SELECT p.product_name,
                c.category_name,
                s.status_name,
                p.buy_date,
                p.buy_price,
                p.image_url,
                p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            WHERE p.buy_date = %s ORDER BY p.buy_date DESC;""", (today_date,))
        elif filter == 'this_week':
            today = datetime.today()
            start_of_week = today - timedelta(days=today.weekday())  # Get Monday's date
            end_of_week = start_of_week + timedelta(days=6)  # Get Sunday's date
            connection.execute("""SELECT p.product_name,
                c.category_name,
                s.status_name,
                p.buy_date,
                p.buy_price,
                p.image_url,
                p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id WHERE p.buy_date BETWEEN %s AND %s ORDER BY p.buy_date DESC;""", (start_of_week,end_of_week,))
        elif filter == 'this_month':
            start_of_month = datetime(datetime.now().year, datetime.now().month, 1).date()
            end_of_month = datetime(datetime.now().year, datetime.now().month + 1, 1).date() - timedelta(days=1)
            connection.execute("""SELECT p.product_name,
                c.category_name,
                s.status_name,
                p.buy_date,
                p.buy_price,
                p.image_url,
                p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id WHERE p.buy_date BETWEEN %s AND %s ORDER BY p.buy_date DESC;""", (start_of_month,end_of_month,))
        elif filter == 'this_year':
            start_of_year = datetime(datetime.now().year, 1, 1).date()
            end_of_year = datetime(datetime.now().year, 12, 31).date()
            connection.execute("""SELECT p.product_name,
                c.category_name,
                s.status_name,
                p.buy_date,
                p.buy_price,
                p.image_url,
                p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id WHERE p.buy_date BETWEEN %s AND %s ORDER BY p.buy_date DESC;""", (start_of_year,end_of_year,))
    else:
        search_query_like = f"%{search_query}%"
        connection.execute("""SELECT p.product_name,
                c.category_name,
                s.status_name,
                p.buy_date,
                p.buy_price,
                p.image_url,
                p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id WHERE p.product_name LIKE %s ORDER BY p.buy_date DESC;""", (search_query_like,))
                
    productList = connection.fetchall()
    if not productList:
        flash('No data available!', 'error')

    
    active_page ="items"
    # print('filter',filter)
    return render_template("items.html", product_list = productList,active_page=active_page,filter=filter)

@app.route('/get_product', methods=['GET'])
def get_product():
    product_id = request.args.get('productId', type=int)
    cursor = getCursor()
    cursor.execute("""SELECT * FROM products WHERE products.product_id = %s""", (product_id,))
    product = cursor.fetchone()
    
    cursor1 = getCursor()
    cursor1.execute("""SELECT * FROM sales WHERE sales.product_id = %s""", (product_id,))
    sales_list = cursor1.fetchall()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product_data = {
        'id': product[0],
        'name': product[1],
        'category': product[2],
        'status': product[3],
        'buy_date': product[4],
        'buy_price': product[5],
        'buy_platform': product[6],
        'image_name': product[7],
    }

    if sales_list:
        for i, sales in enumerate(sales_list):
            product_data[f'sell_id{i+1}'] = sales[0]
            product_data[f'sell_date{i+1}'] = sales[2]
            product_data[f'sell_price{i+1}'] = sales[3]
            product_data[f'sell_platform{i+1}'] = sales[4]
            product_data[f'fees{i+1}'] = sales[5]

    # print("product_data",product_data)
    return jsonify(product_data)



@app.route('/update_item', methods=['POST'])
def update_item():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    category_id = request.form['product_category']
    status_id = request.form['product_status']
    buy_date = request.form['buy_date']
    buy_price = request.form['buy_price']
    buy_platform_id = request.form['buy_platform']
    file = request.files['product_image']
    # print("file",file)
    if file and allowed_file(file.filename):
        connection = getCursor()
        connection.execute("""SELECT image_url FROM products 
            WHERE product_id = %s;""",(product_id,))
        image_name = connection.fetchone()[0]
        print('image_name',image_name)
        if image_name:
            try:
                r2_client.delete_file(image_name, "secondhand")
            except Exception as error:
                print(error)

        file_ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{product_id}.{file_ext}"
        # print("new_filename",filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert HEIC to JPEG if necessary
        if filename.lower().endswith('.heic'):
            try:
                img = Image.open(file_path)
                jpeg_path = file_path.rsplit('.', 1)[0] + '.jpeg'
                img.save(jpeg_path, "JPEG")
                os.remove(file_path)  # Remove the original HEIC file
                file_path = jpeg_path
                filename = os.path.basename(file_path)
            except Exception as e:
                os.remove(file_path)
                flash('The uploaded HEIC file could not be converted.', 'danger')
                return redirect(url_for('home'))

        upload_to_cloudflare(file_path, filename)
        os.remove(file_path)
        
        # Execute the SQL query
        connection1 = getCursor()
        connection1.execute("""UPDATE products SET 
            image_url =%s
            WHERE product_id = %s;""",(filename,product_id,))
   
    connection = getCursor()
    # Execute the SQL query
    connection = getCursor()
    connection.execute("""UPDATE products SET 
        product_name = %s,
        category_id = %s,
        status_id = %s,
        buy_date = %s,
        buy_price = %s,
        buy_platform_id = %s
        WHERE product_id = %s;""",(product_name, category_id, status_id, buy_date, buy_price,
        buy_platform_id,product_id,))

    for i in range(1, 4):
        sell_date = request.form.get(f'sell_date{i}')or None
        sell_price = request.form.get(f'sell_price{i}')or None
        sell_platform = request.form.get(f'sell_platform{i}')or None
        fee = request.form.get(f'fees{i}')or 0
        sell_id = request.form.get(f'sell_id{i}')or None
        # print("sell_id",sell_id)
        connection = getCursor()
        if sell_id and sell_id!= 'undefined':
            if sell_date and sell_price and sell_platform:
                connection.execute("""UPDATE sales SET 
                sell_date = %s,
                sell_price = %s,
                sell_platform_id = %s,
                fees = %s
                WHERE sale_id = %s;""",(sell_date,sell_price,sell_platform,fee,sell_id,))
            elif sell_date is None and sell_price is None and sell_platform is None:
                connection.execute("""DELETE FROM sales 
                WHERE sale_id = %s;""",(sell_id,))
                connection.execute("""SELECT * FROM sales 
                WHERE product_id = %s;""",(product_id,))
                sales_list = connection.fetchall()
                if not sales_list :
                    connection.execute("""UPDATE products SET 
                    status_id = (SELECT status_id FROM status WHERE status_name = 'Selling')
                    WHERE product_id = %s;""",(product_id,))

        else:
            if sell_date and sell_price and sell_platform:
                connection.execute("""INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
                                VALUES (%s, %s, %s, %s, %s);""",
                            (product_id, sell_date, sell_price, sell_platform,fee))
                connection.execute("""UPDATE products SET 
                    status_id = (SELECT status_id FROM status WHERE status_name = 'Sold')
                    WHERE product_id = %s;""",(product_id,))
                

    flash('The product was successfully updated!', 'success')
    return redirect(url_for('product', productId=product_id))


@app.route("/report", methods=['GET'])
def report():
    active_page ="report"
    range_value = request.args.get("range", default="", type=str)
    
    if range_value=='year':
        connection3 = getCursor()
        connection3.execute("""SELECT MONTH(sell_date) AS Month,
       SUM(CASE WHEN sell_price IS NOT NULL AND buy_price IS NOT NULL THEN sell_price - buy_price - fees
           ELSE 0 END) AS total_revenue
        FROM sales s JOIN products p on s.product_id = p.product_id WHERE sell_date IS NOT NULL AND YEAR(sell_date) = YEAR(CURDATE())
        GROUP BY MONTH(sell_date)
        ORDER BY Month;""")
        monthlylist = connection3.fetchall()
        month_list = [calendar.month_name[row[0]] for row in monthlylist]
        mIncome_list = [float(item[1]) for item in monthlylist] 

        connection4 = getCursor()
        connection4.execute("""SELECT p.product_name,c.category_name,st.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
                s.sell_date,s.sell_price,spf.platform_name AS sell_platform_name,s.fees,image_url,p.product_id
                FROM sales s JOIN products p on s.product_id = p.product_id 
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN status st ON p.status_id = st.status_id
                LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
                LEFT JOIN platform spf ON s.sell_platform_id = spf.platform_id WHERE st.status_name = 'Sold' AND YEAR(sell_date) = YEAR(CURDATE())
                ORDER BY s.sell_date DESC;""")
                
        productList = connection4.fetchall()

        return render_template("report_year.html",active_page=active_page,month_list=month_list,mIncome_list=mIncome_list,monthlylist=monthlylist,product_list=productList )
    elif range_value=='month':
        connection3 = getCursor()
        connection3.execute("""SELECT DAY(sell_date) AS Day,
           SUM(CASE WHEN sell_price IS NOT NULL AND buy_price IS NOT NULL THEN sell_price - buy_price - fees
                    ELSE 0 END) AS daily_revenue
            FROM sales s JOIN products p on s.product_id = p.product_id
            WHERE sell_date IS NOT NULL AND MONTH(sell_date) = MONTH(CURDATE()) AND YEAR(sell_date) = YEAR(CURDATE())
            GROUP BY DAY(sell_date)
            ORDER BY Day;""")
        daylist = connection3.fetchall()
        day_list = [row[0] for row in daylist]
        dIncome_list = [float(item[1]) for item in daylist]
        total_income = sum(dIncome_list)

        connection4 = getCursor()
        connection4.execute("""SELECT p.product_name,c.category_name,st.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
                s.sell_date,s.sell_price,spf.platform_name AS sell_platform_name,s.fees,image_url,p.product_id
                FROM sales s JOIN products p on s.product_id = p.product_id 
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN status st ON p.status_id = st.status_id
                LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
                LEFT JOIN platform spf ON s.sell_platform_id = spf.platform_id WHERE st.status_name = 'Sold' AND YEAR(sell_date) = YEAR(CURDATE()) AND MONTH(sell_date) = MONTH(CURDATE())
                ORDER BY s.sell_date DESC;""")
                
        productList = connection4.fetchall()

        return render_template("report_month.html",active_page=active_page,day_list=day_list,dIncome_list=dIncome_list,daylist=daylist,total_income=total_income,product_list=productList )
    else:
        connection1 = getCursor()
        connection1.execute("""SELECT c.category_name, sum(s.sell_price -s.fees -p.buy_price) as income 
            FROM products p JOIN sales s on s.product_id = p.product_id 
            join category c on c.category_id=p.category_id
                    where p.status_id =1
                    group by c.category_name
                    order by income desc;""")
        incomelist = connection1.fetchall()
        category_list = [item[0] for item in incomelist]
        income_list = [float(item[1]) for item in incomelist] 
        # print("incomelist",incomelist)
        connection2 = getCursor()
        connection2.execute("""SELECT YEAR(sell_date) AS year,
        SUM(CASE WHEN sell_price IS NOT NULL AND buy_price IS NOT NULL THEN sell_price - buy_price - fees
            ELSE 0 END) AS total_revenue FROM products p JOIN sales s on s.product_id = p.product_id 
        WHERE  sell_date IS NOT NULL
        GROUP BY YEAR(sell_date)
        ORDER BY year;""")
        yearlylist = connection2.fetchall()
        year_list = [item[0] for item in yearlylist]
        yIncome_list = [float(item[1]) for item in yearlylist] 
        total_income = sum(yIncome_list)

        connection4 = getCursor()
        connection4.execute("""SELECT 
            (SELECT SUM(buy_price) FROM products WHERE status_id = 2) AS total_buy_price_selling,
            SUM(buy_price) AS total_buy_price_all
            FROM products;""")
        paylist = connection4.fetchall()

        connection5 = getCursor()
        connection5.execute("""SELECT p.product_name,c.category_name,st.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
                s.sell_date,s.sell_price,spf.platform_name AS sell_platform_name,s.fees,image_url,p.product_id
                FROM products p JOIN sales s on s.product_id = p.product_id 
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN status st ON p.status_id = st.status_id
                LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
                LEFT JOIN platform spf ON s.sell_platform_id = spf.platform_id WHERE p.status_id = 1 ORDER BY s.sell_date DESC;""")
                
        productList = connection5.fetchall()
        # print('productListhh',productList)
        connection6 = getCursor()
        connection6.execute("""SELECT p.product_name, s.sell_price - s.fees- p.buy_price AS income
                FROM products p JOIN sales s on s.product_id = p.product_id 
                WHERE status_id = 1
                ORDER BY income DESC
                LIMIT 10;""")
        pIncomelist = connection6.fetchall()

        return render_template("report_all.html",range_value=range_value,active_page=active_page,incomelist=incomelist,category_list=category_list,income_list =income_list,yearlylist=yearlylist,year_list=year_list,yIncome_list=yIncome_list,total_income=total_income,paylist=paylist,product_list=productList,pIncomelist=pIncomelist)
    # print('range_value ',range_value )
   
def get_lists():
    connection = getCursor()
    
    connection.execute("""SELECT category_id, category_name FROM category;""")
    categoryList = connection.fetchall()
    
    connection.execute("""SELECT status_id, status_name FROM status;""")
    statusList = connection.fetchall()
    
    connection.execute("""SELECT platform_id, platform_name FROM platform;""")
    platformList = connection.fetchall()
    
    return categoryList, statusList, platformList



@app.route("/product", methods=['GET'])
def product():
    product_id = request.args.get("productId")
    income=''
    sold_length=1
    connection = getCursor()
    connection.execute("""SELECT p.product_name,
            c.category_name,
            s.status_name,
            p.buy_date,
            p.buy_price,
            pf_buy.platform_name AS buy_platform_name,
            p.image_url,
            p.product_id
        FROM products p
        LEFT JOIN category c ON p.category_id = c.category_id
        LEFT JOIN status s ON p.status_id = s.status_id
        LEFT JOIN platform pf_buy ON p.buy_platform_id = pf_buy.platform_id
        WHERE p.product_id= %s;""", (product_id,))
    productList = connection.fetchall()
    if productList:
        buy_price_decimal =productList[0][4]
        buy_price= float(buy_price_decimal)
    connection1 = getCursor()
    connection1.execute("""SELECT sell_date,sell_price,platform_name,fees
        FROM sales s 
        LEFT JOIN platform p ON s.sell_platform_id = p.platform_id
        WHERE s.product_id= %s;""", (product_id,))
    soldList = connection1.fetchall()
    # print('productList',soldList)
    if soldList:
        sold_item = [float(item[1]) - float(item[3]) for item in soldList] 
        total_sold = sum(sold_item)
        income = "{:.2f}".format(total_sold - buy_price)
        sold_length = len(soldList)
        # print("total_sold",sold_length )
    # print('productList',productList)
    categoryList, statusList, platformList = get_lists()
    return render_template("product.html",productList=productList,categoryList=categoryList,statusList=statusList,platformList=platformList,product_id=product_id,soldList=soldList, income= income,sold_length=sold_length)



@app.route("/markSold", methods=['POST'])
def markSold():
    product_id = request.form['product_id']
    sell_date = request.form.get('sellDate') or None
    sell_price = request.form.get('sellPrice') or None
    sell_platform_id = request.form.get('sellPlatform') or None
    fees = request.form.get('fee') or 0
    # Execute the SQL query
    connection = getCursor()
    connection.execute("""INSERT INTO sales (product_id, sell_date, sell_price, sell_platform_id, fees)
                                    VALUES (%s, %s, %s, %s, %s);""",
                                (product_id, sell_date, sell_price, sell_platform_id,fees))
    connection.execute("""
        UPDATE products SET
            status_id = (SELECT status_id FROM status WHERE status_name = 'Sold')
        WHERE product_id = %s;
        """, (product_id,))
    
    flash('The product was successfully updated!', 'success')
    return redirect(url_for('product', productId=product_id))


@app.route("/delete", methods=['GET'])
def delete():
    product_id = request.args.get("productId")
    connection = getCursor()
    
    # Get Image Path
    connection.execute("""
        SELECT image_url 
        FROM products 
        WHERE product_id = %s;
        """, (product_id,))
    img_result = connection.fetchone()
    if img_result:
        try:
            r2_client.delete_file(img_result, "secondhand")
        except Exception as error:
            print(error)
        
    
    # Delete product record
    connection.execute("""
        DELETE FROM products 
        WHERE product_id = %s;
        """, (product_id,))

    flash('The product was successfully deleted!', 'success')
    return redirect(url_for('items'))



@app.route("/manage", methods=['GET','POST'])
def manage():
    categoryList, statusList, platformList = get_lists()
    manage_type = request.args.get("type")
    # print("manage_type",manage_type) 
    active_page ='management'
    categoryId_dele = request.args.get("categoryId")
    platformId_dele = request.args.get("platformId")
    statusId_dele = request.args.get("statusId")
    if manage_type =="cate":
        return render_template("manage_category.html",category_list=categoryList,active_page=active_page)
    elif manage_type =="plat":
        return render_template("manage_platform.html",platform_list=platformList,active_page=active_page)
    elif manage_type =="status":
        return render_template("manage_status.html",status_list=statusList,active_page=active_page)



    if categoryId_dele:
        connection = getCursor()
        connection.execute("""
        SELECT product_name,category_id 
        FROM products 
        WHERE category_id = %s;
        """, (categoryId_dele,))
        category_result = connection.fetchone()
        if category_result:
            flash('There are products under this category, so you cannot delete the category.', 'error')
            return redirect(url_for('manage',type='cate'))
        else:
            connection.execute("""
            DELETE FROM category 
            WHERE category_id = %s;
            """, (categoryId_dele,))
            flash('The category was successfully deleted!', 'success')
            return redirect(url_for('manage',type='cate'))
    elif platformId_dele:
        connection = getCursor()
        connection.execute("""
        SELECT product_name 
        FROM products 
        WHERE buy_platform_id = %s OR sell_platform_id= %s;
        """, (platformId_dele,platformId_dele,))
        platform_result = connection.fetchone()
        if platform_result:
            flash('There are products under this platform, so you cannot delete the platform.', 'error')
            return redirect(url_for('manage',type='plat'))
        else:
            connection.execute("""
            DELETE FROM platform 
            WHERE platform_id = %s;
            """, (platformId_dele,))
            flash('The platform was successfully deleted!', 'success')
            return redirect(url_for('manage',type='plat'))
    elif statusId_dele:
        connection = getCursor()
        connection.execute("""
        SELECT product_name,status_id
        FROM products 
        WHERE status_id = %s;
        """, (statusId_dele,))
        status_result = connection.fetchone()
        if status_result:
            flash('There are products under this status, so you cannot delete the status.', 'error')
            return redirect(url_for('manage',type='status'))
        else:
            connection.execute("""
            DELETE FROM status 
            WHERE status_id = %s;
            """, (statusId_dele,))
            flash('The status was successfully deleted!', 'success')
            return redirect(url_for('manage',type='status'))




    



@app.route("/manage_add", methods=[ 'POST'])
def manage_add():
    data = request.json
    category_name = data.get('category_name')
    platform_name = data.get('platform_name')
    status_name = data.get('status_name')
    if category_name:
        category_name_lower = category_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT category_id, category_name
        FROM category
        WHERE LOWER(category_name) = %s;
        """, (category_name_lower,))
        category_result = connection.fetchone()
        if category_result:
            flash("The category of "+category_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("INSERT INTO category (category_name) VALUES (%s);", (category_name,))
            flash(category_name+" is added successfully.", 'success')
            return jsonify(success=True)
    elif platform_name:
        platform_name_lower = platform_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT platform_id, platform_name
        FROM platform
        WHERE LOWER(platform_name) = %s;
        """, (platform_name_lower,))
        platform_result = connection.fetchone()
        if platform_result:
            flash("The category of "+platform_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("INSERT INTO platform (platform_name) VALUES (%s);", (platform_name,))
            flash(platform_name+" is added successfully.", 'success')
            return jsonify(success=True)
    elif status_name:
        status_name_lower = status_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT status_id, status_name
        FROM status
        WHERE LOWER(status_name) = %s;
        """, (status_name_lower,))
        status_result = connection.fetchone()
        if status_result:
            flash("The category of "+status_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("INSERT INTO status (status_name) VALUES (%s);", (status_name,))
            flash(status_name+" is added successfully.", 'success')
            return jsonify(success=True)
    else:
        return jsonify(success=False, error=" somethings is going wrong.")



@app.route("/manage_update", methods=['POST'])
def manage_update():
    data = request.json
    category_id = data.get('category_id')
    category_name = data.get('category_name')
    platform_id = data.get('platform_id')
    platform_name = data.get('platform_name')
    status_id = data.get('status_id')
    status_name = data.get('status_name')
    if category_id and category_name:
        category_name_lower = category_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT category_id
        FROM category
        WHERE LOWER(category_name) = %s AND category_id != %s;
        """, (category_name_lower, category_id))
        category_result = connection.fetchone()
        if category_result:
            flash("The category of "+category_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("UPDATE category SET category_name = %s WHERE category_id = %s;", (category_name, category_id))
            flash(category_name+" is updated successfully.", 'success')
            return jsonify(success=True)

    if platform_id and platform_name:
        platform_name_lower = platform_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT platform_id
        FROM platform
        WHERE LOWER(platform_name) = %s AND platform_id != %s;
        """, (platform_name_lower, platform_id))
        platform_result = connection.fetchone()
        if platform_result:
            flash("The platform of "+platform_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("UPDATE platform SET platform_name = %s WHERE platform_id = %s;", (platform_name, platform_id))
            flash(platform_name+" is updated successfully.", 'success')
            return jsonify(success=True)
    
    if status_id and status_name:
        status_name_lower = status_name.lower()
        connection = getCursor()
        connection.execute("""
        SELECT status_id
        FROM status
        WHERE LOWER(status_name) = %s AND status_id != %s;
        """, (status_name_lower, status_id))
        status_result = connection.fetchone()
        if status_result:
            flash("The status of "+status_name+" already exists.", 'error')
            return jsonify(success=False)
        else:
            connection.execute("UPDATE status SET status_name = %s WHERE status_id = %s;", (status_name, status_id))
            flash(status_name+" is updated successfully.", 'success')
            return jsonify(success=True)

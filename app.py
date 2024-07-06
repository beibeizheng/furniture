from flask import Flask,flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from datetime import date
from flask import jsonify
import calendar
import os
import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Defining custom filters
def days_diff(end_date, start_date):
    if end_date is None or start_date is None:
        return 'N/A' 
    return (end_date - start_date).days

# Register a custom filter
app.jinja_env.filters['days_diff'] = days_diff

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
      
        product_name = request.form['product_name']
        category_id = request.form['product_category']
        status_id = request.form['product_status']
        buy_date = request.form['buy_date']
        buy_price = request.form['buy_price']
        buy_platform_id = request.form['buy_platform']
        file = request.files['product_image']
        sell_date = request.form.get('sell_date') or None
        sell_price = request.form.get('sell_price') or None
        sell_platform_id = request.form.get('sell_platform') or None
        fees = request.form.get('fees') or None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product_image = os.path.join('images', filename)
            connection = getCursor()
            connection.execute("""INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id,sell_date,sell_price,sell_platform_id,fees,image_name)
            VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s);""",(product_name,category_id,status_id,buy_date,buy_price,buy_platform_id,sell_date,sell_price,sell_platform_id,fees,filename,))
            flash('A new product was successfully added!', 'success')
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
            connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.buy_date = %s;""", (today_date,))
        elif filter == 'this_week':
            today = datetime.today()
            start_of_week = today - timedelta(days=today.weekday())  # Get Monday's date
            end_of_week = start_of_week + timedelta(days=6)  # Get Sunday's date
            connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.buy_date BETWEEN %s AND %s;""", (start_of_week,end_of_week,))
        elif filter == 'this_month':
            start_of_month = datetime(datetime.now().year, datetime.now().month, 1).date()
            end_of_month = datetime(datetime.now().year, datetime.now().month + 1, 1).date() - timedelta(days=1)
            connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.buy_date BETWEEN %s AND %s;""", (start_of_month,end_of_month,))
        elif filter == 'this_year':
            start_of_year = datetime(datetime.now().year, 1, 1).date()
            end_of_year = datetime(datetime.now().year, 12, 31).date()
            connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.buy_date BETWEEN %s AND %s;""", (start_of_year,end_of_year,))
    else:
        search_query_like = f"%{search_query}%"
        connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
                p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
                FROM products p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN status s ON p.status_id = s.status_id
                LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
                LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.product_name LIKE %s;""", (search_query_like,))
                
    productList = connection.fetchall()
    
    active_page ="items"
    # print('filter',filter)
    return render_template("items.html", product_list = productList,active_page=active_page,filter=filter)

@app.route('/get_product', methods=['GET'])
def get_product():
    product_id = request.args.get('productId', type=int)
    cursor = getCursor()
    cursor.execute("""SELECT * FROM products WHERE product_id = %s""", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    if product:
        product_data = {
            'id': product[0],
            'name': product[1],
            'category': product[2],
            'status':product[3],
            'buy_date':product[4],
            'buy_price':product[5],
            'buy_platform':product[6],
            'sell_date':product[7],
            'sell_price':product[8],
            'sell_platform':product[9],
            'fees':product[10],
            'image_name':product[11]
        }
        print("product",product_data)
        return jsonify(product_data)
    else:
        return jsonify({'error': 'Product not found'}), 404


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
    sell_date = request.form.get('sell_date') or None
    sell_price = request.form.get('sell_price') or None
    sell_platform_id = request.form.get('sell_platform') or None
    fees = request.form.get('fees') or 0

    file = request.files['product_image']
    existing_image_name = request.form['existing_product_image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product_image = filename
    else:
        product_image = existing_image_name


    # Execute the SQL query
    connection = getCursor()
    connection.execute("""UPDATE products SET 
        product_name = %s,
        category_id = %s,
        status_id = %s,
        buy_date = %s,
        buy_price = %s,
        buy_platform_id = %s,
        sell_date = %s,
        sell_price = %s,
        sell_platform_id = %s,
        fees = %s,
        image_name =%s
        WHERE product_id = %s;""",(product_name, category_id, status_id, buy_date, buy_price,
        buy_platform_id, sell_date, sell_price, sell_platform_id, fees,product_image,product_id,))

    flash('The product was successfully updated!', 'success')
    print("www",product_id)
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
        FROM products WHERE sell_date IS NOT NULL AND YEAR(sell_date) = YEAR(CURDATE())
        GROUP BY MONTH(sell_date)
        ORDER BY Month;""")
        monthlylist = connection3.fetchall()
        month_list = [calendar.month_name[row[0]] for row in monthlylist]
        mIncome_list = [float(item[1]) for item in monthlylist] 

        return render_template("report.html",range_value=range_value,active_page=active_page,month_list=month_list,mIncome_list=mIncome_list,monthlylist=monthlylist )
    elif range_value=='month':
        connection3 = getCursor()
        connection3.execute("""SELECT DAY(sell_date) AS Day,
           SUM(CASE WHEN sell_price IS NOT NULL AND buy_price IS NOT NULL THEN sell_price - buy_price - fees
                    ELSE 0 END) AS daily_revenue
            FROM products 
            WHERE sell_date IS NOT NULL AND MONTH(sell_date) = MONTH(CURDATE()) AND YEAR(sell_date) = YEAR(CURDATE())
            GROUP BY DAY(sell_date)
            ORDER BY Day;""")
        daylist = connection3.fetchall()
        day_list = [row[0] for row in daylist]
        dIncome_list = [float(item[1]) for item in daylist]
        total_income = sum(dIncome_list)
        return render_template("report.html",range_value=range_value,active_page=active_page,day_list=day_list,dIncome_list=dIncome_list,daylist=daylist,total_income=total_income )
    else:
        connection1 = getCursor()
        connection1.execute("""SELECT c.category_name, sum(p.sell_price -p.buy_price-p.fees) as income FROM products p join category c on c.category_id=p.category_id
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
            ELSE 0 END) AS total_revenue FROM products
        WHERE  sell_date IS NOT NULL
        GROUP BY YEAR(sell_date)
        ORDER BY year;""")
        yearlylist = connection2.fetchall()
        year_list = [item[0] for item in yearlylist]
        yIncome_list = [float(item[1]) for item in yearlylist] 
        total_income = sum(yIncome_list)

        connection4 = getCursor()
        connection4.execute("""SELECT 
            (SELECT SUM(buy_price) FROM products WHERE status_id = (SELECT status_id FROM status WHERE status_name = 'selling')) AS total_buy_price_selling,
            SUM(buy_price) AS total_buy_price_all
            FROM products;""")
        paylist = connection4.fetchall()

        return render_template("report.html",range_value=range_value,active_page=active_page,incomelist=incomelist,category_list=category_list,income_list =income_list,yearlylist=yearlylist,year_list=year_list,yIncome_list=yIncome_list,total_income=total_income,paylist=paylist)
    # print('range_value ',range_value )
   


@app.route("/product", methods=['GET'])
def product():
    product_id = request.args.get("productId")
    connection = getCursor()
    connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
                p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
                FROM products p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN status s ON p.status_id = s.status_id
                LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
                LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id WHERE p.product_id= %s;""", (product_id,))
    productList = connection.fetchall()
    # print('productList',productList)
    connection1 = getCursor()
    connection1.execute("""SELECT category_id,category_name FROM category;""")
    categoryList = connection1.fetchall()
    connection2 = getCursor()
    connection2.execute("""SELECT status_id,status_name FROM status;""")
    statusList = connection2.fetchall()
    connection3 = getCursor()
    connection3.execute("""SELECT platform_id,platform_name FROM platform;""")
    platformList = connection3.fetchall()
    return render_template("product.html",productList=productList,categoryList=categoryList,statusList=statusList,platformList=platformList,product_id=product_id)



@app.route("/markSold", methods=['POST'])
def markSold():
    product_id = request.form['product_id']
    sell_date = request.form.get('sellDate') or None
    sell_price = request.form.get('sellPrice') or None
    sell_platform_id = request.form.get('sellPlatform') or None
    fees = request.form.get('fee') or None
    # Execute the SQL query
    connection = getCursor()
    connection.execute("""
        UPDATE products SET
            status_id = (SELECT status_id FROM status WHERE status_name = 'Sold'),
            sell_date = %s,
            sell_price = %s,
            sell_platform_id = %s,
            fees = %s
        WHERE product_id = %s;
        """, (sell_date, sell_price, sell_platform_id, fees, product_id))
    
    flash('The product was successfully updated!', 'success')
    return redirect(url_for('product', productId=product_id))


@app.route("/delete", methods=['GET'])
def delete():
    product_id = request.args.get("productId")
    connection = getCursor()
    connection.execute("""
        DELETE FROM products 
        WHERE product_id = %s;
        """, (product_id,))
    flash('The product was successfully deleted!', 'success')
    return redirect(url_for('items'))

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from flask import jsonify
import os
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

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
            print('file',filename)
            connection = getCursor()
            connection.execute("""INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id,sell_date,sell_price,sell_platform_id,fees,image_name)
            VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s);""",(product_name,category_id,status_id,buy_date,buy_price,buy_platform_id,sell_date,sell_price,sell_platform_id,fees,filename,))
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
        return render_template("index.html",categoryList=categoryList,statusList=statusList,platformList=platformList)



@app.route("/items")
def items():
    connection = getCursor()
    connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees,image_name,p.product_id
            FROM products p
            LEFT JOIN category c ON p.category_id = c.category_id
            LEFT JOIN status s ON p.status_id = s.status_id
            LEFT JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            LEFT JOIN platform spf ON p.sell_platform_id = spf.platform_id;""")
    productList = connection.fetchall()
    connection1 = getCursor()
    connection1.execute("""SELECT category_id,category_name FROM category;""")
    categoryList = connection1.fetchall()
    connection2 = getCursor()
    connection2.execute("""SELECT status_id,status_name FROM status;""")
    statusList = connection2.fetchall()
    connection3 = getCursor()
    connection3.execute("""SELECT platform_id,platform_name FROM platform;""")
    platformList = connection3.fetchall()
    return render_template("items.html", product_list = productList,categoryList=categoryList,statusList=statusList,platformList=platformList)

@app.route('/get_product', methods=['GET'])
def get_product():
    product_id = request.args.get('productId', type=int)
    cursor = getCursor()
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product_detail = cursor.fetchone()
    cursor.close()
    print("product_detail",product_detail)
    return render_template("items.html", product_detail = product_detail)
    

@app.route("/report")
def report():
    return render_template("report.html")


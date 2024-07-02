from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

# Defining custom filters
def days_diff(end_date, start_date):
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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/items")
def items():
    connection = getCursor()
    connection.execute("""SELECT p.product_name,c.category_name,s.status_name,p.buy_date,p.buy_price,bpf.platform_name AS buy_platform_name,
            p.sell_date,p.sell_price,spf.platform_name AS sell_platform_name,p.fees
            FROM products p
            JOIN category c ON p.category_id = c.category_id
            JOIN status s ON p.status_id = s.status_id
            JOIN platform bpf ON p.buy_platform_id = bpf.platform_id
            JOIN platform spf ON p.sell_platform_id = spf.platform_id;""")
    productList = connection.fetchall()
    print("productList",productList)
    return render_template("items.html", product_list = productList)

@app.route("/report")
def report():
    return render_template("report.html")


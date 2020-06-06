from flask import Flask, request, render_template
import mysql.connector as mysqlconn
import os
import random
import socket
import sys

app = Flask(__name__)

# Load configurations
app.config.from_pyfile('config_file.cfg')
button1 =       app.config['VOTE1VALUE']  
button2 =       app.config['VOTE2VALUE']
title =         app.config['TITLE']

# MySQL configurations
MYSQL_DATABASE_USER     = os.environ['MYSQL_USER'] 
MYSQL_DATABASE_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DATABASE_DB       = os.environ['MYSQL_DATABASE']
MYSQL_DATABASE_HOST     = os.environ['MYSQL_HOST']
MYSQL_DATABASE_SSL_CA = './BaltimoreCyberTrustRoot.crt.pem'

# Return MySQL Connection Object
def connect():
    return mysqlconn.connect(
        host = MYSQL_DATABASE_HOST,
        port = '3306',
        user = MYSQL_DATABASE_USER,
        password = MYSQL_DATABASE_PASSWORD,
        database = MYSQL_DATABASE_DB,
        ssl_ca = MYSQL_DATABASE_SSL_CA,
        ssl_verify_cert = True
    )

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    hostname = socket.gethostname()

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = None

    # MySQL Connection
    if connection == None or not connection.is_connected():
        connection = connect()
    cursor = connection.cursor()

    # Vote tracking
    vote1 = 0
    vote2 = 0

    if request.method == 'GET':

        # Get current values
        cursor.execute('''Select votevalue, count(votevalue) as count From azurevote.azurevote
        group by votevalue''')
        results = cursor.fetchall()

        # Parse results
        for i in results:
            if i[0] == app.config['VOTE1VALUE']:
                vote1 = i[1]
            elif i[0] == app.config['VOTE2VALUE']:
                vote2 = i[1]              

        # Return index with values
        return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title, hostname=hostname)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            
            # Empty table and return results
            cursor.execute('''Delete FROM azurevote''')
            connection.commit()
            return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title, hostname=hostname)
        else:

            # Insert vote result into DB
            vote = request.form['vote']
            cursor.execute('''INSERT INTO azurevote (votevalue) VALUES(%s)''', (vote,))
            connection.commit()
            
            # Get current values
            cursor.execute('''Select votevalue, count(votevalue) as count From azurevote.azurevote
            group by votevalue''')
            results = cursor.fetchall()

            # Parse results
            for i in results:
                if i[0] == app.config['VOTE1VALUE']:
                    vote1 = i[1]
                elif i[0] == app.config['VOTE2VALUE']:
                    vote2 = i[1]         
                
            # Return results
            return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title, hostname=hostname)

@app.route('/results')
def results():
    connection = None

    # MySQL Connection
    if connection == None or not connection.is_connected():
        connection = connect()
    cursor = connection.cursor()

    # Get current values
    cursor.execute('''Select * FROM azurevote''')
    rv = cursor.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
import os
from flask import Flask
#from flask.ext.mysql import MySQL
app = Flask(__name__)

#mysql=MySQL()

# MySql Confs
#app.config['MYSQL_DATABASE_USER']='db_user'
#app.config['MYSQL_DATABASE_PASSWORD']='vagrant'
#app.config['MYSQL_DATABASE_DB']='employeedb'
#app.config['MYSQL_DATABASE_HOST']='localhost'
#conn = mysql.connect()
#cursor = conn.cursor()


@app.route("/")
def main():
    return "Welcome!"

@app.route('/how are you')
def hello():
    return 'I am good, how about you?'

#@app.route('/read from database'
#def read():
#    cursor.execute('SELECT * FROM employees')
#   row = cursor.fetchone()
#    result = []
#    while row is not None:
#        result.append(row[0])
#        row = cursor.fetchone()
#    
#    return ",".join(result)


if __name__ == "__main__":
    app.run()

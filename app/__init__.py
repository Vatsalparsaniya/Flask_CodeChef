from flask_mysqldb import MySQL
from flask import Flask,render_template,url_for

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MYSQL_HOST= 'sql12.freesqldatabase.com',
    MYSQL_USER='sql12308164',
    MYSQL_PASSWORD='VPCkMech5s',
    MYSQL_PORT = 3306,
    MYSQL_DB='sql12308164'
)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # cur.execute("CREATE TABLE authorization(USER int(30),EMAIL varchar(35),PASSWORD varchar(30));")
    # cur.execute("INSERT INTO sql12308164.authorization VALUES (\"Darshit\",\"Darshit@gmail.com\",\"12345678\");")
    cur.execute("SELECT * FROM sql12308164.authorization;")
    rv = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('Index.html',DATA=rv)

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/signup')
def signup():
    return render_template('Signup.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)
    
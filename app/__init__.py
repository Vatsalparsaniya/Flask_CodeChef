from flask_mysqldb import MySQL
from flask import Flask,render_template,url_for,request,flash,redirect
from urllib.request import Request, urlopen
import urllib.request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MYSQL_HOST= 'sql12.freesqldatabase.com',
    MYSQL_USER='sql12308164',
    MYSQL_PASSWORD='VPCkMech5s',
    MYSQL_PORT = 3306,
    MYSQL_DB='sql12308164'
)
app.secret_key = 'vatsalparsaniya'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    # cur.execute("CREATE TABLE authorization(USER int(30),EMAIL varchar(35),PASSWORD varchar(30));")
    # cur.execute("INSERT INTO sql12308164.authorization VALUES (\"Darshit\",\"Darshit@gmail.com\",\"12345678\");")
    cur.execute("SELECT EMAIL FROM sql12308164.authorization;")
    rv = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('Index.html',DATA=rv)

@app.route('/login_page/')
def login():
    return render_template('Login.html')

@app.route('/signup_page/')
def signup():
    return render_template('Signup.html')

@app.route('/login_check/', methods=['POST'])
def login_check():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EMAIL,PASSWORD FROM sql12308164.authorization;")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if (email,password) in data:
            flash("Loged in Successfully")
            cur = mysql.connection.cursor()
            cur.execute("SELECT USER FROM sql12308164.authorization WHERE EMAIL=\'"+email+"\';")
            uname = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return render_template("Codechef_credentials.html",uname=uname[0][0])
        else:
            flash("Wrong!! Email or Password")
            return redirect(url_for("login"))

@app.route('/signup_check/', methods=['POST'])
def signup_check():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("SELECT EMAIL FROM sql12308164.authorization;")
        email_validate = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        uname = request.form['uname']
        email = request.form['email']
        password = request.form['psw']
        Rpassword = request.form['psw-repeat']
        try:
            if password == Rpassword:
                if email not in email_validate:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO sql12308164.authorization VALUES (\""+uname+"\",\""+email+"\",\""+password+"\");")
                    mysql.connection.commit()
                    cur.close()
                    flash("successfuly signup as {}".format(uname))
                    return redirect(url_for('login'))   
                else:
                    flash("sorry, emailid already signup")
                    return redirect(url_for('signup'))
            else:
                flash("Sorry, Password does not match")
                return redirect(url_for('signup'))
        except:
            flash("sorry, emailid already signup")
            return redirect(url_for('signup'))

@app.route('/Codechef_Credentials/')
def Codechef_Credentials():
    return render_template('Codechef_credentials.html')

@app.route('/check_contest_detail',methods=['POST'])
def check_details():
    if request.method == 'POST':
        uname = request.form['username']
        contest_name = request.form['content']
        User_profile_url  = "https://www.codechef.com/users/{}".format(uname)
        contest_url = "https://www.codechef.com/{}".format(contest_name)
        User_page = requests.get(User_profile_url)
        contest_page = request.get(contest_url)
        if str(User_page) == "<Response [404]>" and str(contest_page) == "<Response [404]>":
            flash("enter valid user name or contest code")
            return render_template("Codechef_credentials.html")
        else:
            flash("Successfully fatched data")
            return render_template("contest_details.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)
        
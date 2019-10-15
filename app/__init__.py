from flask_mysqldb import MySQL
from flask import Flask,render_template,url_for,request,flash,redirect
from urllib.request import Request, urlopen
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import time

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


def fetch_contest(contest_name,uname):
    Problem_code_URL = []
    Contest_URL = "https://www.codechef.com/{}/".format(contest_name)
    Contest_page = requests.get(Contest_URL)
    Contest_page_content = BeautifulSoup(Contest_page.content,'html.parser')
    data = [['Name','Code','Successful Submissions','Accuracy']]
    for row in Contest_page_content.findAll('tr',attrs={'class':'problemrow'}):
        row_data =[]
        problem_name = row.findAll('b')[0].text
        problem_code = row.findAll('td')[1].text
        problem_Successful_Submission = row.findAll('div')[2].text
        problem_Accuracy = row.findAll('a')[1].text
        row_data.append(problem_name)
        row_data.append(problem_code)
        row_data.append(problem_Successful_Submission)
        row_data.append(problem_Accuracy)
        Problem_code_URL.append(problem_code)
        data.append(row_data)
    return data

@app.route('/check_contest_detail/',methods=['POST','GET'])
def check_details():
        if request.method == 'POST':
            uname = request.form['username']
            contest_name = request.form['content']
            User_profile_url  = "https://www.codechef.com/users/{}".format(uname)
            contest_url = "https://www.codechef.com/{}".format(contest_name)
            User_page = requests.get(User_profile_url)
            contest_page = requests.get(contest_url)
            if str(User_page) == "<Response [404]>" and str(contest_page) == "<Response [404]>":
                flash("enter valid user name or contest code , {} or {} is not valid".format(uname,contest_name))
                return render_template("Codechef_credentials.html")
            else:
                flash("Successfully fatched data for contest {} and user name {}".format(contest_name,uname))
                return render_template("contest_details.html",Data = fetch_contest(contest_name,uname),uname=uname,contest_name=contest_name)
    
def Problem_S(contest,User_name,code):
    problem_page_url = "https://www.codechef.com/"+str(contest)+"/problems/"+str(code)+"/"
    page = requests.get(problem_page_url)
    page_contest = BeautifulSoup(page.content,'html.parser')
    statement = page_contest.findAll('div',attrs={'class':'content'})
    a = statement[1].text
    b = re.sub('[$]', '', a)
    # Can't fatch All Special character so replacing them by replace function
    b = b.replace("\le","<").replace("\ldots","...").replace("\in","∈").replace("\oplus","⊕").replace("\{","{")
    b =b.replace("\}","}").replace("\sum_{i=1}^{N-1}","i=1∑N−1").replace("**","").replace("`","").replace("\neq","≠")
    b =b.replace("*","").replace("\rightarrow","->").replace("\ge",">").replace(" \cdot ","*").replace("\neq","≠")
    problem_statment = b
    return problem_statment


@app.route('/Code_details/<contest>/<uname>/',methods=['POST'])
def Code_details(uname,contest):
    if request.method == 'POST':
        CODE = request.form['code']
        flash(" Uname " + str(uname) + " Code " + CODE + " Contest " + contest)
        return render_template('problem_statment.html',problem_statment = Problem_S(contest,uname,CODE),uname=uname,contest_name=contest,code=CODE)

def solution_table_function(contest_name,uname,code):
    Sloution_Status_url = "https://www.codechef.com/"+contest_name+"/status/"+code+","+uname
    page_content = requests.get(Sloution_Status_url)
    time.sleep(2)
    page = BeautifulSoup(page_content.content,'html.parser')
    ID = page.findAll('td',attrs={'width':'60'})
    SID = []
    for subid in ID:
        SID.append(subid.text)
    return SID

@app.route('/solution_table/<contest_name>/<uname>/<code>/',methods=['POST'])
def solution_table(contest_name,uname,code):
    if request.method == 'POST':
        return render_template("solutiontable.html",ID = solution_table_function(contest_name,uname,code),uname=uname)

def get_viewsol(subid):
    solution_view_url = "https://www.codechef.com/viewplaintext/" + subid
    req = Request(solution_view_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage = BeautifulSoup(webpage,'html.parser')
    z = webpage.find('pre').text
    return z

@app.route('/viewsolution/<uname>/<subid>/',methods=['POST'])
def viewsol(uname,subid):
    if request.method == 'POST':
        return render_template("viewsolution.html",uname=uname,solution = get_viewsol(subid))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)
        
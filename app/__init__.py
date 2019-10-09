from flask_mysqldb import MySQL
from flask import Flask,render_template,url_for

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MYSQL_HOST='127.0.0.1',
    MYSQL_USER='root',
    MYSQL_PASSWORD='12345678',
    MYSQL_DB='Flask_CRUD'
)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('Index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1234)
    
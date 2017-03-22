from flask import Flask, g, render_template, request
from conf import config
import os
import sqlite3 as sql
app = Flask(__name__)

def main():
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)

def connect_db():
    return sql.connect(config.DATABASE_NAME)


@app.before_request
def before_request():
    g.db = connect_db()
    
@app.route('/submit',methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('form/form.html')
    elif request.method == 'POST':
        kwargs = {
            'name': request.form['name'],
            'key': request.form['key'],
        }
        
        return render_template(
            'form/process.html', **kwargs)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main()
    
    
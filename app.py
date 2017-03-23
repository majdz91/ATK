#!/usr/bin/env python
# this script is the flask interface for the ATK 
from flask import Flask, g, render_template, request
from conf import config , DB
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
    pass
    
    
@app.route('/submit',methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('form/form.html')
    elif request.method == 'POST':
        DBl = DB.DBL(config.l_s_i)
        kwargs = {
            'name': request.form['name'],
            'key': request.form['key'],
        }
        List = DBl.Hash_List()
        for i in range (config.STU_NUM):
            if kwargs['key'] == List[i] :
                print('yep')
                List[i] = List[i].replace(kwargs['key'],'*######*')
                DBl.Update_Hashes(List)
                return render_template(
                'form/process.html', **kwargs)
        return render_template(
                'form/hash_error.html', **kwargs)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main()
    
    
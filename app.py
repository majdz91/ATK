#!/usr/bin/env python
# this script is the flask interface for the ATK 
from flask import Flask, g, render_template, request
from flask_basicauth import BasicAuth
from conf import  DBase as DB
from conf import config
import os, datetime
import generator as gen
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///conf/pdb.db'
basic_auth = BasicAuth(app)
DB.db.init_app(app)


def main():
    
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
    


@app.before_request
def before_request():
    pass

@app.route('/Manage',methods=['POST','GET']) 
@basic_auth.required
def Manage():
    if request.method == 'GET':
        return render_template('form/start.html') 
    elif request.method == 'POST':
        now = datetime.datetime.now()
        Hash = gen.generate()
        print(Hash)
        sess = DB.Sessions(now)
        DB.db.session.add(sess)
        DB.db.session.commit()
        
        
    
    

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
    
    
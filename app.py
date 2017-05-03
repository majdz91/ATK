#!/usr/bin/env python
# this script is the flask interface for the ATK 
from flask import Flask, g, render_template, request , abort
from flask_basicauth import BasicAuth
from conf import  DBase as DB
from conf import config
import os, datetime ,re 
import generator as gen
from flask_sqlalchemy import SQLAlchemy 


# initilaizing Flask App With SQLAlchemy Object Mapper 
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///conf/pdb.db'
basic_auth = BasicAuth(app)
DB.db.init_app(app)


def main():
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
        return render_template('form/Start.html') 
    elif request.method == 'POST':
        now = datetime.date.today()
        Hash = gen.generate()
        rv = DB.Sessions.query.all()
        for r in rv : 
            if r.SDate.strftime("%Y-%m-%d") == now.strftime("%Y-%m-%d") :
                  return render_template('form/error.html', name = "Session is already registered")
        
        sess = DB.Sessions(now)
        hsh = DB.Hashes(str(Hash))
        DB.db.session.add(sess)
        DB.db.session.add(hsh)
        DB.db.session.commit()
        DB.db.session.flush()
        return render_template('form/Done.html', h = Hash )
        
        
          
        
@app.route('/submit',methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('form/form.html')
    elif request.method == 'POST':
        student_id = DB.Students.query.filter_by(Name=str(request.form['name'])).first()
        if student_id is None : 
            return render_template('form/error.html',name=str(request.form['name']))
        elif student_id is not None : 
            now = datetime.date.today()
            sid = DB.Sessions.query.all()
            for s in sid :
                if s.SDate.strftime("%Y-%m-%d") == now.strftime("%Y-%m-%d") :
                    si = s.ID 
            if si is not None :
                hashe = DB.Hashes.query.filter_by(ID=si).first()
                kwargs = {
                    'name': request.form['name'],
                    'key': request.form['key'],
                        }
                List = DB.Get_Hashes()
                mylist = str(List).split(',')
                
                for word in mylist :
                    ed = word[2:-1]
                    if kwargs['key'] == ed :
                        return render_template('form/process.html', **kwargs)
                    
                return render_template('form/error.html', **kwargs)
       
        
    #    print(li)
     #   for l in li:
      #     if kwargs['key'] == l :
       #        print('yep')
              
               
        
        
        #return render_template(
         #       'form/hash_error.html', **kwargs)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main()
    
    
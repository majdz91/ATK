from conf import config 
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask , g 




app = Flask(__name__)    
db = SQLAlchemy()


class Students(db.Model):
    __tablename__ = 'Students'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))
#    Notes = db.Column(db.String(500))
    rel_att = db.relationship('Attendance',backref='stu_id',lazy='dynamic')


    def __init__(self, Name, notes, pub_date=None):
        self.Name = Name
        self.Notes = notes
        
    def __repr__(self):
        return '<Student Name :  %r>' % self.Name
        
class Sessions(db.Model):
    __tablename__ = 'Sessions'
    ID = db.Column(db.Integer , autoincrement=True , primary_key=True)
    SDate = db.Column(db.Date)
    #rel_hash = db.relationship('Hashes',backef='sess_hash',lazy='dynamic')
    rel_att = db.relationship('Attendance',backref='sess_id',lazy='dynamic')
    db.__table_args__ = (db.UniqueConstraint('SDate', name='udate'))
    def __init__(self,SDate):
        
        self.SDate = SDate
        
    def __repr__(self):
        return '%r' % self.SDate
        
class Hashes(db.Model):
    __tablename__ = 'Hashes'
    ID = db.Column(db.Integer , primary_key = True)
    Hashes = db.Column(db.String(255))
    #Sessions = db.relationship('Sessions', backref=db.backref('ID', lazy='dynamic'))

    
    def __init__(self,Hashes):
        
        self.Hashes = Hashes
        
    
    def __repr__(self):
        return '<Hashes are : %r>' % self.Hashes
    
ass_tab = db.Table()
    
    
        
class Attendance(db.Model):
    __tablename__ = 'Attendance'
    ID = db.Column(db.Integer,primary_key=True)
    ST_ID = db.Column(db.Integer , db.ForeignKey('Students.ID'))
    S_ID = db.Column(db.Integer ,  db.ForeignKey('Sessions.ID'))
    Attend = db.Column(db.Integer)

    def __init__(self,ST_ID,S_ID,Attend):
        self.ST_ID = ST_ID 
        self.S_ID = S_ID
        self.Attend = Attend
        
#MetaData.create_all()

def Get_Hashes():
    h = [] 
    rv = Hashes.query.get(1)
    return rv
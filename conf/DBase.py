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
    rel2 = db.relationship('Attendance',backref='rel_students',lazy='dynamic')

    def __init__(self, Name, notes, pub_date=None):
        self.Name = Name
        self.Notes = notes
        
    def __repr__(self):
        return '<Student Name :  %r>' % self.Name
        
class Sessions(db.Model):
    __tablename__ = 'Sessions'
    ID = db.Column(db.Integer , autoincrement=True , primary_key=True)
    SDate = db.Column(db.Date)
    #rel_att = db.relationship('Hashes',backef='sess_hash',lazy='dynamic')
    rel1 = db.relationship('Attendance',backref='rel_session',lazy='dynamic')
    db.__table_args__ = (db.UniqueConstraint('SDate', name='udate'))

    def __init__(self,SDate):
        self.SDate = SDate
        
    def __repr__(self):
        return '%r' % self.SDate
        
class Hashes(db.Model):
    __tablename__ = 'Hashes'
    ID = db.Column(db.Integer , primary_key = True)
    Hashes = db.Column(db.String(500))
    
    def __init__(self,Hashes):
        self.Hashes = Hashes
        
    def __repr__(self):
        return ' %r' % self.Hashes
    
#ass_tab = db.Table()
    
class Attendance(db.Model):
    __tablename__ = 'Attendance'
    ID = db.Column(db.Integer,primary_key=True)
    ST_ID = db.Column(db.Integer , db.ForeignKey('Students.ID'))
    S_ID = db.Column(db.Integer ,  db.ForeignKey('Sessions.ID'))
    Attend = db.Column(db.Boolean)
    rel_to_session = db.relationship("Sessions", back_populates="rel1")
    rel_to_students = db.relationship("Students", back_populates="rel2")
    
    def __init__(self,ST_ID,S_ID,Attend):
        self.ST_ID = ST_ID 
        self.S_ID = S_ID
        self.Attend = Attend
        
    def __repr__(self):
        return '{}-{}-{}'.format(self.ID,self.S_ID,self.Attend)


def Get_Hashes(SI):
    rv = Hashes.query.get(SI)
    return rv
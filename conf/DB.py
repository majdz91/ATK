# class Modle for DB CURD 

import sqlite3 as sql 
from conf import config

class DBL():
    def __init__(self,sessionid):
        self.SID = sessionid
        self.CON = sql.connect('conf/pdb.db')
        self.CUR = self.CON.cursor()
    def Get_Session_Hashes(self):
        self.result = self.CUR.execute('SELECT Hashes FROM Hashes WHERE S_ID = ?',(self.SID,)).fetchone()[0]
    def Hash_List(self):
        self.Get_Session_Hashes()
        self.List = self.result.split(',')
        for i in range (config.STU_NUM) :
            self.List[i] = self.List[i][2:10]
        return self.List
    
        
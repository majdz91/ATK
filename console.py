#!/usr/bin/env python

import sqlite3 as sql 
import sys,os,datetime,time,uuid
import generator as genr
from optparse import OptionParser


def Create_Session(dateobj):
    print('Creating Session Haseshes')
    toolbar_width = 25
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) 

    for i in range(toolbar_width):
        time.sleep(0.1)
        # do real work here
        hashes= Create_Hashes()
   
        file = open("hashes.txt","w")
        for hashe in hashes :
            file.write(hashe)
            file.write("\n")
        file.close()
         # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()
    sys.stdout.write("\n")
    # Done Visulaizing the bar progress 
    print('submit session')
    time.sleep(0.1)
    submit(hashes,dateobj)
    
    return hashes

def Create_Hashes():
    i=0
    hashs =[]
    for i in range (25):
        hashs.append(genr.get_ran_str())
    return hashs
    
def submit(hashs,dateobj):
    db = sql.connect('conf/pdb.db')
    cur = db.cursor()
    try: 
        cursor = cur.execute('SELECT max(ID) FROM Sessions')
        _id = cursor.fetchone()[0] 
        max_id = _id + 1
        bind_date = dateobj.strftime('%Y-%m-%d')
        cur.execute('INSERT INTO Sessions(ID,SDate) VALUES(?,?)',(max_id,bind_date))
        db.commit()
        try:
            hash_sub = cur.execute('INSERT INTO Hashes VALUES(?,?)',(_id,str(hashs)))
            db.commit()
        except sql.Error as e:
            db.rollback()
            print('[-]Error :', e.args[0])
        print('[+] Session registered')
    except sql.Error as e:
        db.rollback()
        print('[-] Error : ', e.args[0])
        

def main():
    usage = """usage: /path/to/console.py --create-session YYYY-MM-DD after commiting session 
    /path/to/console.py --put-online on|off to start or stop ATK web service"""
    parser = OptionParser(usage=usage)
    parser.add_option( "--create-session", type="string", dest="date",action="store", help="Start new R{c} session by --create-session 2017-04-12")
    parser.add_option( "--put-online", dest="online",action="store_true",default=False, help="Start|Stop ATK web service with --put-online ")
    (options, args) = parser.parse_args()
    if options.date!=None:
        dateobj = datetime.datetime.strptime(options.date,"%Y-%m-%d")
        Create_Session(dateobj)
    if options.online:
        import app
        app.main()
        
        

if __name__ == "__main__":
    main()
   
    
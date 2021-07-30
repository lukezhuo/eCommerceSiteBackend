# coding: utf-8
import sqlite3
def connect():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DROP TABLE if EXISTS sellers")
    cur.execute("CREATE TABLE IF NOT EXISTS sellers (email text PRIMARY KEY, password text not null)")
    conn.commit()
    conn.close()

def insertUser(email,password,security_ans,status):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if status=="sellers":
        cur.execute("INSERT INTO sellers VALUES(?,?,?,0.0)", (email,password,security_ans))
    elif status == "buyers":
        cur.execute("INSERT INTO buyers VALUES(?,?,?,0.0)", (email,password,security_ans))
    conn.commit()
    conn.close()

def retrieveUser(email,status):
    print(email)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if status=="sellers":
        cur.execute("SELECT * FROM sellers WHERE email=?",[email])
    elif status == "buyers":
        cur.execute("SELECT * FROM buyers WHERE email=?",[email])
    user = cur.fetchall()
    conn.close()
    return user

def getSellerList(email):
    print(email)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE seller=?",[email])
    rows = cur.fetchall()
    conn.close()
    return rows

def addBalance(email, balance, status):
    print(email)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if status == "sellers":
        cur.execute("UPDATE sellers SET balance=? WHERE email=?",[balance,email])
    if status == "buyers":
        cur.execute("UPDATE buyers SET balance=? WHERE email=?",[balance,email]) 
    conn.commit()
    conn.close()
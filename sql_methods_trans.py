import sqlite3

def get_all_trans(email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE buyer_email=?",[email])
    rows=cur.fetchall()
    conn.close()
    return rows

def insert_review(item_id, buyer_email, notes, buyername, date, stars):
    #inserts reviews
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO reviews VALUES (?,?,?,?,?,?)",(item_id, buyer_email, notes, buyername, date, stars))
    conn.commit()
    conn.close()
    return

def insert_item_to_trans(trans_id, date, buyer_email, seller_email, item_id, item_cost, quantity):
    #inserts reviews
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?)",(trans_id, date, buyer_email, seller_email, item_id, item_cost, quantity))
    conn.commit()
    conn.close()
    return 

def get_current_trans_id():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT COUNT (*) FROM transactions")
    rows=cur.fetchall()
    conn.close()
    return rows


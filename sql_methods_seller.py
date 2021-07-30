import sqlite3

def get_selling_items(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT item_id, item_name, item_price, quantity, description, category, seller FROM items WHERE seller=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

def seller_balance(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT balance FROM buyers WHERE email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    print(rows)
    return rows

def get_sold_hist(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT trans_id, date, buyer_email, seller_email, item_id, item_cost, quantity FROM transactions WHERE seller_email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

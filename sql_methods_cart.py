# coding: utf-8
import sqlite3
def connect():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DROP TABLE if EXISTS cart")
    cur.execute("CREATE TABLE IF NOT EXISTS cart (PRIMARY KEY(email, item_id), qty int)")
    conn.commit()
    conn.close()

def insert_cart_item(b_email, item_id, quantity):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO cart VALUES (?,?,?)",(b_email, item_id, quantity))
    conn.commit()
    conn.close()

def get_cart_item(b_email, iid):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM cart WHERE email=? AND item_id=?", [b_email, iid])
    rows=cur.fetchall()
    conn.close()
    return rows

def get_cart(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT cart.email, cart.item_id, items.item_name, items.item_price, cart.quantity, items.seller FROM cart, items WHERE cart.item_id = items.item_id AND email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

def get_item_ids(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT item_id, quantity FROM cart WHERE email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

def cost(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT SUM(item_price) FROM cart, items WHERE cart.item_id = items.item_id AND email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

def delete_cart_item(buyer_email, item_id):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM cart WHERE email=? AND item_id=?",[buyer_email, item_id])
    conn.commit()
    conn.close()

def clear_cart(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM cart WHERE ​email=?",[b_email])
    conn.commit()
    conn.close()

def balance(b_email):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT balance FROM buyers WHERE email=?", [b_email])
    rows=cur.fetchall()
    conn.close()
    return rows

def deduct_bal(b_email, amt):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT balance FROM buyers WHERE email=?", [b_email])
    rows=cur.fetchall()
    new = rows[0][0] - amt
    print(new, b_email)
    cur.execute("UPDATE buyers SET balance = ? WHERE email=?", [new, b_email])
    conn.commit()
    conn.close()
    return rows

def remove_from_inv(iid, quanty):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT quantity FROM items WHERE item_id=?", [iid])
    rows=cur.fetchall()
    new = rows[0][0] - quanty
    print(new, iid)
    cur.execute("UPDATE items SET quantity = ? WHERE item_id=?", [new, iid])
    conn.commit()
    conn.close()
    return rows

def adjust_cart_amt(email, iid, quanty):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT quantity FROM cart WHERE email = ? AND item_id=?", [email, iid])
    rows=cur.fetchall()
    new = rows[0][0] + quanty
    print(new, iid)
    cur.execute("UPDATE cart SET quantity = ? WHERE email = ? AND item_id=?", [new, email, iid])
    conn.close()
    return rows

def cart_amt(email, iid):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT quantity FROM cart WHERE email = ? AND item_id=?", [email, iid])
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

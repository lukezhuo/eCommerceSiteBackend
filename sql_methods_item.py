# coding: utf-8
import sqlite3
def connect():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DROP TABLE if EXISTS items")
    cur.execute("CREATE TABLE IF NOT EXISTS items (item_id text PRIMARY KEY, item_name text, item_price float, quantity int, description text, photo text)")
    conn.commit()
    conn.close()

def insert_item(item_name, item_price, quantity, description, category,seller):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO items VALUES (NULL,?,?,?,?,?,?)",(item_name, item_price, quantity, description, category,seller))
    conn.commit()
    conn.close()

""" def search(item_name):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_name LIKE ('%' || ? || '%')", [item_name])
    rows=cur.fetchall()
    conn.close()
    return rows """

def search(item_name, item_category, item_description, min_price, max_price,seller):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE ((?1 IS NULL OR item_name LIKE ('%' || ?1 || '%')) AND (?2 IS NULL OR category = ?2) AND (?3 IS NULL OR description LIKE ('%' || ?3|| '%')) AND (?5 IS NULL OR item_price >= ?4 AND item_price <= ?5) AND (?6 IS NULL OR seller LIKE ('%' || ?6|| '%')))", [item_name, item_category, item_description, min_price, max_price,seller])
    rows=cur.fetchall()
    conn.close()
    return rows

def get_recommendation(email):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE category IN (SELECT DISTINCT I.category FROM items I, transactions T WHERE T.buyer_email = ?1 AND T.item_id = I.item_id) AND item_id NOT IN (SELECT item_id FROM transactions WHERE buyer_email = ?1) LIMIT 9", [email])
    rows = cur.fetchall()
    conn.close()
    return rows

def get_seller(item_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT seller FROM items WHERE item_id=?", [item_id])
    rows = cur.fetchall()
    conn.close()
    return rows

def get_cost(item_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT item_price FROM items WHERE item_id=?", [item_id])
    rows = cur.fetchall()
    conn.close()
    return rows

def find_item(item_id):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_id=?", [item_id])
    rows=cur.fetchall()
    conn.close()
    return rows

def search_category(category):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE category = ?", [category])
    rows = cur.fetchall()
    conn.close()
    return rows

def in_price_range(low_price, high_price):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items WHERE item_price>=? and item_price<=?", (low_price, high_price))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete_item(item_id):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM items WHERE ​item_id​=?",(item_id))
    conn.commit()
    conn.close()

def update_price(item_id, item_price):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("UPDATE items SET item_price=? WHERE ​item_id​=?",(item_price, item_id))
    conn.commit()
    conn.close()

def update_name(item_id, item_name):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("UPDATE items SET item_name=? WHERE ​item_id​=?",(item_name, item_id))
    conn.commit()
    conn.close()

def update_desc(item_id, description):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("UPDATE items SET description=? WHERE ​item_id​=?",(description, item_id))
    conn.commit()
    conn.close()

def update_qty(item_id, quantity):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("UPDATE items SET item_quantity=? WHERE ​item_id​=?",(quantity, item_id))
    conn.commit()
    conn.close()

def update_seller(item_id, seller):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("UPDATE items SET seller=? WHERE ​item_id​=?",(seller, item_id))
    conn.commit()
    conn.close()

def avg_price():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT avg(item_price) FROM items")
    rows=cur.fetchall()
    conn.close()
    return rows

def count_different_items():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT count(item_id) FROM items")
    rows=cur.fetchall()
    conn.close()
    return rows

def get_all_items():
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items LIMIT 20;")
    rows=cur.fetchall()
    conn.close()
    return rows

def get_n_items(n):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM items LIMIT 20 offset ?",(n))
    rows=cur.fetchall()
    conn.close()
    return rows

def get_all_reviews(item_id):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE item_id=?",[item_id])
    rows=cur.fetchall()
    conn.close()
    return rows

def get_names_from_id(rows):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    data = []
    for row in rows:
        id = row[4]
        cur.execute("SELECT item_name FROM items WHERE item_id=?",[id])
        ret = cur.fetchall()
        data.append(ret[0][0])
    conn.close()
    return data

def get_rating(item_id):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    cur.execute("SELECT AVG(stars) FROM reviews WHERE item_id=?",[item_id])
    rows=cur.fetchall()
    conn.close()
    return rows

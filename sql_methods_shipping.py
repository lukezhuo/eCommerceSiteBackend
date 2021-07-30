import sqlite3

def get_all_shipping(email):
  conn=sqlite3.connect("database.db")
  cur=conn.cursor()
  cur.execute("SELECT * FROM shipping WHERE seller_email=?",[email])
  rows=cur.fetchall()
  conn.close()
  return rows

def insert_shipping(buyer_email, seller_email, item_id, date_shipped, provider, eta):
  conn=sqlite3.connect("database.db")
  cur=conn.cursor()
  print(buyer_email)
  cur.execute("INSERT INTO shipping VALUES (?,?,?,?,?,?)", (buyer_email,seller_email, item_id, date_shipped, provider, eta))
  conn.commit()
  conn.close()
  return 

def get_item_id(rows):
    conn=sqlite3.connect("database.db")
    cur=conn.cursor()
    data = []
    for row in rows:
        id = row[2]
        cur.execute("SELECT item_id FROM shipping WHERE item_id=?",[id])
        ret = cur.fetchall()
        data.append(ret[0][0])
    conn.close()
    return data
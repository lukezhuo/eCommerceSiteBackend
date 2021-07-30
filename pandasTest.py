import pandas as pd
import sqlite3, csv
import uuid

pd.set_option('max_colwidth', 800)

df = pd.read_csv('amazon_co-ecommerce_sample.csv', dtype={'price': str, 'number_available_in_stock}': str})

df = df[df['customer_reviews'].notna()]

df['price'] = df['price'].str.replace('£','')
df['price'].fillna('100.00', inplace = True)

df['number_available_in_stock'].fillna('10', inplace = True)
df['number_available_in_stock'] = df['number_available_in_stock'].str.split().str[0] + '0'

df['average_review_rating'] = df['average_review_rating'].str.split().str[0]

df['amazon_category_and_sub_category'] = df['amazon_category_and_sub_category'].str.split(' > ').str[0]
df['amazon_category_and_sub_category'].fillna('Other', inplace = True)

df['sellers'] = df['sellers'].str.split('"Seller_price_1"').str[0]
df['sellers'] = df['sellers'].str.split('=>').str[2]
df['sellers'] = df['sellers'].str.strip('"')
df['sellers'] = df['sellers'].str.split('"').str[0]
df['sellers'].fillna('Amazon.co.uk', inplace = True)
df['sellers'] = df['sellers'].str.replace(" ","")
df['sellers'] = df['sellers'] + '@gmail.com'

df.to_csv('modified.csv')

conn=sqlite3.connect("database.db")
cur=conn.cursor()
cur.execute("DROP TABLE if EXISTS items")
cur.execute("DROP TABLE if EXISTS temp")
cur.execute("DROP TABLE if EXISTS sellers")
cur.execute("CREATE TABLE IF NOT EXISTS temp (id text, name text, manufact text, price text, quantity text, numreviews text, numansweredq text, avgrating text, category text, customer_also_bought text, description text, info text, prod_desc text, bought_after_viewing text, qanda text, reviews text, seller text)")

with open('modified.csv', 'r',encoding='utf-8') as file:
	dr = csv.DictReader(file)
	to_db = [(i['uniq_id'], i['product_name'], i['manufacturer'], i['price'], i['number_available_in_stock'], i['number_of_reviews'], i['number_of_answered_questions'], i['average_review_rating'], i['amazon_category_and_sub_category'], i['customers_who_bought_this_item_also_bought'], i['description'], i['product_information'], i['product_description'], i['items_customers_buy_after_viewing_this_item'], i['customer_questions_and_answers'], i['customer_reviews'], i['sellers']) for i in dr]

cur.executemany("INSERT INTO temp (id, name, manufact, price, quantity, numreviews, numansweredq, avgrating, category, customer_also_bought, description, info, prod_desc, bought_after_viewing, qanda, reviews, seller) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)

# create items table and insert values from temp table
cur.execute("CREATE TABLE IF NOT EXISTS items (item_id INTEGER PRIMARY KEY, item_name text NOT NULL, item_price REAL NOT NULL CHECK (item_price > 0), quantity int NOT NULL CHECK (quantity > 0), description text, category TEXT NOT NULL, seller TEXT NOT NULL REFERENCES sellers(email), UNIQUE(item_id, seller))")
cur.execute("SELECT name, price, quantity, description, category, seller FROM temp")
rows = cur.fetchall()
cur.executemany("INSERT INTO items VALUES (NULL,?,?,?,?,?,?);", rows)

# init sellers table
cur.execute("CREATE TABLE IF NOT EXISTS sellers (email TEXT PRIMARY KEY, password TEXT NOT NULL, security_ans TEXT NOT NULL, balance REAL NOT NULL CHECK (balance >= 0))")
cur.execute("SELECT DISTINCT seller FROM temp")
rows = cur.fetchall()
cur.executemany("INSERT INTO sellers VALUES (?, 'testpw', 'testans', 0);", rows)

# init buyers table
cur.execute("DROP TABLE IF EXISTS buyers")
cur.execute("CREATE TABLE IF NOT EXISTS buyers (email TEXT PRIMARY KEY, password TEXT NOT NULL, security_ans TEXT NOT NULL, balance REAL NOT NULL CHECK (balance >= 0))")
cur.execute("SELECT reviews FROM temp")
rows = cur.fetchall()

x = []
for row in rows:
	if "\n" in row[0]:
		separated = row[0].splitlines()
		abuyer = separated[2].strip().replace(" ","")
		if abuyer not in x and len(abuyer) > 1:
			cur.execute("INSERT INTO buyers VALUES (?, 'testpw', 'testans', 5000);", (abuyer + '@gmail.com',))
			x.append(abuyer)

# init reviews table
cur.execute("DROP TABLE IF EXISTS reviews")
cur.execute("CREATE TABLE IF NOT EXISTS reviews (item_id INTEGER REFERENCES items(item_id), buyer_email TEXT REFERENCES buyers(email), notes TEXT NOT NULL, buyername TEXT NOT NULL, date TEXT NOT NULL, stars REAl NOT NULL CHECK (stars >= 0 and stars <= 5.0), UNIQUE(item_id, buyer_email))")

cur.execute("SELECT item_id, reviews FROM temp, items WHERE temp.name = items.item_name")
rows = cur.fetchall()

for row in rows:
	separated = row[1].split("|")
	for onerev in separated:
		revar = onerev.split('//')
		if len(revar)>4:
			buyerstring = revar[3].splitlines()
			if len(buyerstring) < 3: continue
			buyer = buyerstring[2].strip().replace(" ","")
			if not buyer.isalnum(): continue
			note = revar[4]
			date = revar[2]
			rating = revar[1]
		cur.execute("INSERT OR IGNORE INTO reviews VALUES (?, ?, ?, ?, ?, ?);", (row[0], buyer + '@gmail.com', note, buyer, date, rating))

# init cart table
cur.execute("DROP TABLE IF EXISTS cart")
cur.execute("CREATE TABLE IF NOT EXISTS cart (email TEXT NOT NULL REFERENCES buyers(email), item_id INTEGER NOT NULL REFERENCES items(item_id), quantity INTEGER NOT NULL CHECK (quantity >= 0), UNIQUE(email, item_id))")
cur.execute("SELECT I.item_id FROM buyers B, items I LIMIT 10")
rows = cur.fetchall()
cur.executemany("INSERT INTO cart VALUES ('Copnovelist@gmail.com', ?, 1);", rows)

# init transactions table
cur.execute("DROP TABLE IF EXISTS transactions")
cur.execute("CREATE TABLE IF NOT EXISTS transactions (trans_id INTEGER PRIMARY KEY, date TEXT NOT NULL, buyer_email TEXT NOT NULL REFERENCES buyers(email), seller_email TEXT NOT NULL REFERENCES sellers(email), item_id INTEGER NOT NULL REFERENCES items(item_id), item_cost REAL NOT NULL CHECK (item_cost > 0), quantity INTEGER NOT NULL, UNIQUE(trans_id, buyer_email, seller_email, item_id))")
cur.execute("SELECT seller, item_id, item_price FROM items LIMIT 10")
rows = cur.fetchall()
cur.executemany("INSERT INTO transactions VALUES (NULL, '10/4/2014', 'Copnovelist@gmail.com', ?, ?, ?, 1);", rows)
cur.execute("SELECT B.email, I.seller, I.item_id, I.item_price, I.quantity FROM items I, buyers B, reviews R WHERE I.item_id = R.item_id AND B.email = R.buyer_email LIMIT 100")
rows = cur.fetchall()
cur.executemany("INSERT INTO transactions VALUES (NULL, '10/4/2014', ?, ?, ?, ?, ?);", rows)

#put some transactions and orderhistory for Copnovelist
cur.execute("INSERT INTO transactions VALUES (NULL, '10/4/2014','Jen@gmail.com', 'Copnovelist@gmail.com', '100', '36.35', '1');")
cur.execute("INSERT INTO items VALUES (NULL, 'Database Manual', '15.00', '3', 'Manual to help you study for CS316', 'Fancy Dress', 'Copnovelist@gmail.com');")


# init recommendations (do we even need this table??)
cur.execute("DROP TABLE IF EXISTS recommendations")
cur.execute("CREATE TABLE IF NOT EXISTS recommendations (email TEXT NOT NULL REFERENCES buyers(email), item_id INTEGER NOT NULL REFERENCES items(item_id))")

# init shipping
cur.execute("DROP TABLE IF EXISTS shipping")
cur.execute("CREATE TABLE IF NOT EXISTS shipping (buyer_email TEXT NOT NULL REFERENCES buyers(email), seller_email TEXT NOT NULL REFERENCES sellers(email), item_id INTEGER NOT NULL REFERENCES items(item_id), date_shipped TEXT NOT NULL, provider TEXT NOT NULL, ETA TEXT NOT NULL, UNIQUE(buyer_email, seller_email, item_id))")

conn.commit()
conn.close()

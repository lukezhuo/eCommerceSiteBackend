from flask import Flask, jsonify, render_template, url_for, redirect, request, session
from markupsafe import escape
from flask_cors import CORS
import sql_methods_item as sqlm
import sql_methods_user as sqlu
import sql_methods_cart as sqlc
import sql_methods_trans as sqlt
import sql_methods_shipping as sqls
import sql_methods_seller as sqlms
import sqltojson
from datetime import datetime
from datetime import date

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#insert some temp values COMMENT THIS OUT AFTER first time
""" sqlm.insert_item("1", "FantasticPhone", 500.00, 2, "super duper phone", "photolink1")
sqlm.insert_item("2", "FP2", 500.20, 4, "super duper sfsdf", "photolink2")
sqlm.insert_item("3", "FP3", 510.00, 5, "super crappy phone", "photolink3")
sqlm.insert_item("4", "FP3", 510.00, 5, "super crappy phone", "photolink3")
sqlm.insert_item("5", "F2P3", 510.00, 5, "super crappy p", "photolink13")
sqlm.insert_item("6", "FP23", 510.00, 5, "super crappy thing", "photo1link3") """

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

ITEMS = [
    {
        'uid': 1,
        'name': 'iPhone',
        'quantity': 5,
        'price': 799.99,
        'description': 'Brand new',
    },
    {
        'uid': 2,
        'name':'MacBook Pro',
        'quantity': 2,
        'price': 1299.99,
        'description': 'Slightly used',
    },
    {
        'uid': 3,
        'name': 'Apple Watch',
        'quantity': 10,
        'price': 499.99,
        'description': 'Brand new',
    }
]

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/items', methods=['GET','POST'])
def items():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # if(not bool(sqlu.retrieveUser(post_data.get('seller_text'),'sellers'))):
        #     return jsonify({'status': 'failure'})
        sqlm.insert_item(
            post_data.get('name'),
            post_data.get('price'),
            post_data.get('quantity'),
            post_data.get('description'),
            post_data.get('category_text'),
            post_data.get('seller_text'))
        response_object['message'] = 'Item added!'
    else:
        rows = sqlm.get_all_items()
        response_object['items'] = (sqltojson.make_dicts_item(rows[0:50], None))
        print(response_object)
    return jsonify(response_object)

@app.route('/balance',methods=['GET','POST'])
def balance():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        total = 0
        post_data = request.get_json()
        email = post_data.get('email')
        pw = post_data.get('password')
        amount = post_data.get('money')
        s = sqlu.retrieveUser(email,'sellers')
        b = sqlu.retrieveUser(email,'buyers')
        if(not bool(s) and not bool(b)):
            print('account doesnt exist')
            return jsonify({'status': 'failure'})
        if(bool(s) and s[0][1]==pw):
            total = s[0][3] +int(amount)
            total = str(total)
            sqlu.addBalance(email, total, 'sellers')
            print(total)
        if(bool(b) and b[0][1]==pw):
            total = b[0][3]+ int(amount)
            total = str(total)
            sqlu.addBalance(email, total, 'buyers')
            print(total)
        else:
            print('incorrect pw')
            return jsonify({'status': 'failure'})
    else:
        print(response_object)
    return jsonify(response_object)



@app.route('/search', methods=['GET'])
def search_items():
    name = request.args.get('name')
    category = request.args.get('category')
    description = request.args.get('description')
    minprice = request.args.get('minprice')
    maxprice = request.args.get('maxprice')
    seller = request.args.get('seller')
    params = [name, category, description,minprice, maxprice, seller]
    conv = lambda i : i or None
    nullparams = [conv(i) for i in params]
    response_object = {'status': 'success'}
    rows = sqlm.search(nullparams[0], nullparams[1], nullparams[2], nullparams[3], nullparams[4],nullparams[5])
    response_object['items'] = (sqltojson.make_dicts_search(rows, None))
    return jsonify(response_object)


@app.route('/recom', methods=['GET'])
def get_recommendation():
    email = request.args.get('email')
    rows = sqlm.get_recommendation(email)
    response_object = {'status': 'success'}
    response_object['items'] = (sqltojson.make_dicts_item(rows, None))
    return jsonify(response_object)


""" @app.route('/searchid/<uid>', methods=['GET'])
def search_items_id(uid):
    print(type(uid))
    response_object = {'status': 'success'}
    rows = sqlm.find_item(uid)
    print(rows)
    response_object['items'] = (sqltojson.make_dicts_search(rows, None))
    return jsonify(response_object) """


@app.route('/getitem/<id>', methods=['GET'])
def one_item(id):
    print(type(id))
    print("getting one item ID: "+id)
    rows = sqlm.find_item(id)
    revs = sqlm.get_all_reviews(id)
    avgrating = sqlm.get_rating(id)
    print(sqltojson.make_dicts_item(rows, avgrating))
    print(sqltojson.make_dicts_review(revs))
    return jsonify({
    'status':'success',
    'items': (sqltojson.make_dicts_item(rows, avgrating)),
    'reviews': (sqltojson.make_dicts_review(revs))
    })

@app.route('/cart<buyer_email>', methods=['GET'])
def get_cart(buyer_email):
    response_object = {'status': 'success'}
    stuff = sqlc.get_cart(buyer_email)
    response_object['trans'] = sqltojson.make_dicts_cart(stuff)
    return jsonify(response_object)

@app.route('/selling<email>', methods=['GET'])
def get_selling(email):
    stuff = sqlms.get_selling_items(email)
    bal = sqlms.seller_balance(email)
    return jsonify({
    'status':'success',
    'selling': (sqltojson.make_dicts_selling(stuff)),
    'balance': (sqltojson.make_dicts_sellbal(bal))
    })

@app.route('/sellinghistory<email>', methods=['GET'])
def get_sellinghist(email):
    stuff = sqlms.get_sold_hist(email)
    return jsonify({
    'status':'success',
    'transactions': (sqltojson.make_dicts_sold(stuff))
    })

@app.route('/checkout', methods=['POST'])
def checkout():
    post_data = request.get_json()
    b_email = post_data.get('buyer_email')
    print("wtf")
    if sqlc.cost(b_email)[0][0] > sqlc.balance(b_email)[0][0]:
        print(sqlc.cost(b_email)[0][0])
        print(sqlc.balance(b_email)[0][0])
        return jsonify({
            'status':'failure'
        })
    else:
        print("wtf is going on")
        exp = sqlc.cost(b_email)[0][0]
        sqlc.deduct_bal(b_email, exp)
        # print(exp)
        for iid in sqlc.get_item_ids(b_email):
            sqlc.remove_from_inv(iid[0], iid[1])
        new_id = sqlt.get_current_trans_id()[0][0] + 1
        for ii in sqlc.get_item_ids(b_email):
            ii = ii[0]
            #now = datetime.now()
            today = datetime.today()
            d1 = today.strftime("%d/%m/%Y")
            #d1 = now.strftime("%d/%m/%Y %H:%M:%S")
            #print(ii)
            seller = sqlm.get_seller(ii)[0][0]
            #print(seller)
            price = sqlm.get_cost(ii)[0][0]
            amt = sqlc.cart_amt(b_email, ii)[0][0]
            sqlt.insert_item_to_trans(new_id, d1, b_email, seller, ii, price, amt)
            print(new_id, d1, b_email, seller, ii, price, amt)
            new_id = new_id + 1
        #print(sqlc.balance(b_email)[0][0])
        for i in sqlc.get_item_ids(b_email):
            i = i[0]
            sqlc.delete_cart_item(b_email, i)
        #print(sqlc.clear_cart(b_email))
        return jsonify({
            'status':'success'
        })
#@app.route('/addtocart/<item_id>/<buyer_email>', methods=['POST'])
@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data.get('item_id'))
        sqlc.insert_cart_item(
            post_data.get('buyer_email'),
            post_data.get('item_id'),
            #item_id,
            post_data.get('quantity'))
        response_object['message'] = 'Item added to cart!'
        return jsonify(response_object)
    else:
        stuff = sqlc.get_cart(buyer_email)
        response_object['cart'] = (sqltojson.make_dicts_cart(stuff))
        return jsonify(response_object)

#@app.route('/removefromcart/<item_id>/<buyer_email>', methods=['DELETE'])
@app.route('/removefromcart', methods=['POST'])
def remove_from_cart():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        #print(buyer_email, item_id)
        sqlc.delete_cart_item(
            post_data.get('buyer_email'),
            post_data.get('item_id'))
        response_object['message'] = 'Item deleted from cart!'
        return jsonify(response_object)
    else:
        response_object = {'status': 'failure'}
        stuff = sqlc.get_cart(buyer_email)
        response_object['cart'] = (sqltojson.make_dicts_cart(stuff))
        return jsonify(response_object)

@app.route('/')
def index():
    if 'email' in session:
        return 'Logged in as %s' % escape(session['email'])
    return 'You are not logged in'

@app.route('/signup<email>+<password>+<security>/<status>')
def signup(email,password,security,status):
    if(not bool(sqlu.retrieveUser(email,"buyers")) and not bool(sqlu.retrieveUser(email,"sellers"))):
        print(status)
        if status == "sellers" or status == "buyers" :
            sqlu.insertUser(email,password,security,status)
            return jsonify({
            'status':'success'
            })
        else:
            print("status should be sellers or buyers")
            return jsonify({
            'status':'failure'
        })
    else:
        print("email already has a linked account")
        return jsonify({
            'status':'failure'
        })

@app.route('/seller/<email>')
def sellerList(email):
    user = sqlu.retrieveUser(email,"sellers")
    items = sqlu.getSellerList(email)
    return jsonify({
    'seller': (sqltojson.make_dicts_user(user)),
    'items': (sqltojson.make_dicts_sellerItem(items))
    })

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/account')
def account():
    email = request.args.get('email')
    print(email)
    response_object = {'status': 'success'}
    rows = sqlt.get_all_trans(email)
    itemnames = sqlm.get_names_from_id(rows)
    cursell = sqlms.get_selling_items(email)
    cursellbal = sqlu.retrieveUser(email,'buyers')[0][3]
    sold = sqlms.get_sold_hist(email)
    solditems = sqlm.get_names_from_id(sold)
    response_object['trans'] = (sqltojson.make_dicts_trans(rows, itemnames))
    response_object['selling'] = (sqltojson.make_dicts_selling(cursell))
    response_object['balance'] = cursellbal
    response_object['sold'] = sqltojson.make_dicts_sold(sold, solditems)
    return jsonify(response_object)

@app.route('/publishreview', methods=['GET', 'POST'])
def publishreview():
    print("publish review made")
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        sqlt.insert_review(
            post_data.get('item_id'),
            post_data.get('buyer_email'),
            post_data.get('notes'),
            post_data.get('buyername'),
            datetime.now().strftime("%d %B, %Y"),
            post_data.get('stars'))
        response_object['message'] = 'Item added!'
    return jsonify(response_object)

@app.route('/login', methods=['GET', 'POST'])
def login():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        formemail = post_data.get('email')
        formpass = post_data.get('password')
        row = sqlu.retrieveUser(formemail,'buyers')
        realpass = row[0][1]
        if formpass == realpass: response_object['loginstat']='success'
        else: response_object['loginstat']='incorrect password'
        print(row)
        print(jsonify(response_object))
    return jsonify(response_object)


@app.route('/ship', methods=['GET', 'POST'])
def shipment():
    seller_email="Copnovelist@gmail.com"
    response_object = {'status': 'success'}#, 'seller_email': seller_email}
    if request.method == 'POST':
        post_data = request.get_json()
        sqls.insert_shipping(
            post_data.get('buyerEmail'),
            post_data.get('sellerEmail'),
            post_data.get('itemID'),
            post_data.get('dateShipped'),
            post_data.get('provider'),
            post_data.get('eta'))
        print(post_data.get('buyerEmail'))
        response_object['message']= 'Shipment added!'
    else:
        rows = sqls.get_all_shipping(seller_email)
        response_object['ship'] = (sqltojson.make_dicts_ship(rows))
        print(response_object)
    return jsonify(response_object)


if __name__ == "__main__":
    app.run(debug=False)

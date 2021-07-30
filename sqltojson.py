def make_dicts_item(rowsi, avgrating):
    fields = ["item_id", "item_name","item_price", "quantity", "description", "category", "seller"]
    data = []
    for row in rowsi:
        tempdic = {}
        for i in range(7):
            tempdic[fields[i]] = row[i]
        if avgrating:
            tempdic['avgrating'] = avgrating[0][0]
            if tempdic['avgrating'] == None: tempdic['avgrating'] = 0
        data.append(tempdic)
    return data

def make_dicts_sellerItem(rowsi):
    fields = ["item_id", "item_name","item_price", "quantity", "description", "category"]
    data = []
    for row in rowsi:
        tempdic = {}
        for i in range(6):
            tempdic[fields[i]] = row[i]
        data.append(tempdic)
    return data

def make_dicts_review(reviews):
    fields = ["item_id", 'buyer_email', 'notes', 'buyername', 'date', 'stars']
    data = []
    for row in reviews:
        tempdic = {}
        for i in range(6):
            tempdic[fields[i]] = row[i]
        data.append(tempdic)
    if len(reviews)==0:
        print('no reviews')
        data.append({"item_id":"0", "buyer_email":"0", "notes":"na", "buyername": "na", "date":'na', "stars":"0"})
    return data

def make_dicts_user(users):
    fields = ["email", "password","security_ans","balance"]
    data = []
    for user in users:
        tempdic = {}
        for i in range(4):
            tempdic[fields[i]] = user[i]
        data.append(tempdic)
    return data

def make_dicts_search(rowsi, avgrating):
    fields = ["item_id", "item_name","item_price", "quantity", "description", "category", "seller"]
    data = []
    for row in rowsi:
        tempdic = {}
        for i in range(7):
            tempdic[fields[i]] = row[i]
        if avgrating: tempdic['avgrating'] = avgrating[0][0]
        data.append(tempdic)
    return data

def make_dicts_cart(cart_contents):
    fields = ["email", "item_id", "item_name", "item_price", "quantity", "seller"]
    data = []
    for cart_c in cart_contents:
        tempdic = {}
        for i in range(6):
            tempdic[fields[i]] = cart_c[i]
        data.append(tempdic)
    return data

def make_dicts_selling(selling_contents):
    fields = ["item_id", "item_name", "item_price", "quantity", "description", "category", "seller"]
    data = []
    for selling_c in selling_contents:
        tempdic = {}
        for i in range(7):
            tempdic[fields[i]] = selling_c[i]
        data.append(tempdic)
    return data

def make_dicts_sellbal(balance):
    fields = ["balance"]
    data = []
    for bal in balance:
        tempdic = {}
        for i in range(1):
            tempdic[fields[i]] = bal[i]
        data.append(tempdic)
    return data

def make_dicts_sold(transaction_contents, itemnames):
    fields = ["trans_id", "date", "buyer_email", "seller_email", "item_id", "item_cost", "quantity"]
    data = []
    for j, transaction_c in enumerate(transaction_contents):
        tempdic = {}
        for i in range(7):
            tempdic[fields[i]] = transaction_c[i]
        tempdic['item_name'] = itemnames[j]
        data.append(tempdic)
    return data

def make_dicts_cost(cost_cont):
    fields = ["cost"]
    data = []
    for cost_c in cost_cont:
        tempdic = {}
        for i in range(1):
            tempdic[fields[i]] = cost_c[i]
        data.append(tempdic)
    return data

def make_dicts_trans(trans, itemnames):
    fields = ["trans_id", "date","buyer_email", "seller_email", "item_id", "item_cost", "quantity"]
    data = []
    for j, row in enumerate(trans):
        tempdic = {}
        for i in range(len(fields)):
            tempdic[fields[i]] = row[i]
        tempdic['item_name'] = itemnames[j]
        data.append(tempdic)
    return data

def make_dicts_ship(ship):
    fields = ["buyer_email", "seller_email", "item_id", "date_shipped", "provider", "ETA"]
    data = []
    for j, row in enumerate(ship):
        tempdic = {}
        for i in range(len(fields)):
            tempdic[fields[i]]=row[i]
        data.append(tempdic)
    return data

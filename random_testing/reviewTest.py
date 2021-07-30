import pandas as pd

pd.set_option('max_colwidth', 800)
df = pd.read_csv('../modified.csv')
#print(df['customer_reviews'][2])
teststring = df['customer_reviews'][2]
alltestrevs = teststring.split("|")
onerevar = alltestrevs[0].split("//")
print(onerevar[3].splitlines())

row = df['customer_reviews'][2]
separated = row.split("|")
for onerev in separated:
    revar = onerev.split('//')
    if len(revar)>4:
        buyerstring = revar[3].splitlines()
        print(buyerstring)
        buyer = buyerstring[2].strip().replace(" ","")
        print(buyer)
        if not buyer.isalnum(): continue
        note = revar[4]
        date = revar[2]
        rating = revar[1]

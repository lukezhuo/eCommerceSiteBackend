from google_images_search import GoogleImagesSearch
import os
import re
gis = GoogleImagesSearch('AIzaSyDg_wjdnL2VEQQMvOCU73lTKt6OuPHXKd0', '50d8c3f39e94e4ba1')


categories = [('Hobbies',), ('Characters & Brands',), ('Other',), ('Fancy Dress',), ('Bags',), ('Arts & Crafts',), ('Handbags & Shoulder Bags',), ('Games',), ('Figures & Playsets',), ('Home Accessories',), ('Sweets, Chocolate & Gum',), ('Sports Toys & Outdoor',), ('Die-Cast & Toy Vehicles',), ('Baby & Toddler Toys',), ('Storage, Cleaning & Ring Sizers',), ('Bedding & Linens',), ('Office Supplies',), ('Party Supplies',), ('Camping & Hiking',), ('Pretend Play',), ('Women',), ('Electronic Toys',), ('Car Parts',), ('Dolls & Accessories',), ('Indoor Lighting',), ('Educational Toys',), ('Laundry, Storage & Organisation',), ("Supporters' Gear",), ('Jams, Honey & Spreads',), ('Novelty & Special Use',), ('Musical Toy Instruments',), ('Men',), ('Sex & Sensuality',), ('Cooking & Dining',), ('Medication & Remedies',), ('Puppets & Puppet Theatres',), ('Jigsaws & Puzzles',), ('Dogs',), ('Medical Supplies & Equipment',), ('Pens, Pencils & Writing Supplies',), ('Worlds Apart',), ('Gardening',), ('Lab & Scientific Products',), ('Novelty Jewellery',)]

foldernames = []

for cattup in categories:
    catname = cattup[0]
    cncondense = "".join(catname.split(" "))
    print(cncondense)
    path = "/Users/ahanasen/Documents/316twopart/316-mini-amazon-client/src/assets/images/"
    # try:
    #     os.mkdir(path+cncondense)
    # except FileExistsError:
    #     print('Directory not created.')
    # foldernames.append(cncondense)



# for i, cattup in enumerate(categories):
#     cat = cattup[0]
#     _search_params = {
#     'q':cat+" toy",
#     'num':1,
#     'fileType': 'jpg',
#     'imgSize':'ICON'
#     }
#     foldername = foldernames[i]
#     print(cat)
#     print(foldername)
#     path = "/Users/ahanasen/Documents/316twopart/316-mini-amazon-client/src/assets/images/"
#     gis.search(search_params=_search_params, path_to_dir=path+foldername)

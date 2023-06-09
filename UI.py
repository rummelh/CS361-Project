# Import module
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import mysql.connector
import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

cnx = mysql.connector.connect(user = 'cs340_rummelh', password = '3496', host = 'classmysql.engr.oregonstate.edu',
database = 'cs340_rummelh')

cursor = cnx.cursor()



root = Tk()


root.geometry("600x600")

inventory_management = Label(root, text= "Inventory Management", font=("Times", 24))
inventory_management.pack()



#passed to button click to pass parameters to create product window
def get_product_info():
    product = clicked.get()
    query = ("SELECT * FROM Products WHERE product_name = %s")
    cursor.execute(query, (product,))
    results = cursor.fetchall()
    stock = results[0][2]
    source = results[0][3]
    link = results[0][4]
    lead_time = results[0][5]
    cost = results[0][6]
    create_product_window(product,stock,source,link,lead_time,cost)

def get_category_info():
    category = click.get()
    query = ("SELECT category_ID FROM Categories WHERE category_name = %s")
    cursor.execute(query,(category,))
    results = cursor.fetchall()
    results = results[0]
    query2 = ("SELECT * FROM Products WHERE category_id = %s")
    cursor.execute(query2,results)
    result = cursor.fetchall()
    product_name = result[0][1]
    stock = result[0][2]
    time = result[0][8]
    create_category_window(category, product_name, stock, time)

def add_inventory():
    #adds one to product inventory
    product = clicked.get()
    query = ("SELECT inventory_level FROM Products WHERE product_name = %s")
    cursor.execute(query,(product,))
    result = cursor.fetchall()
    add = result[0][0]
    add +=1
    update_query = ("UPDATE Products SET inventory_level = %s")
    cursor.execute(update_query, (add,))





def subtract_inventory():
    #subtracts one from inventory
    product = clicked.get()
    query = ("SELECT inventory_level FROM Products WHERE product_name = %s")
    cursor.execute(query, (product,))
    result = cursor.fetchall()
    sub = result[0][0]
    sub -= 1
    update_query = ("UPDATE Products SET inventory_level = %s")
    cursor.execute(update_query, (sub,))

#Creates pop-up window for given product
def create_product_window(name1, inventory1, source1, link1, lead_time1,cost1):
    window = tk.Toplevel(root)
    window.geometry("300x300")
    product_name = Label(window, text = name1, font = ("Times", 24))
    product_name.pack()

    inventory_level = Label(window, text = "Inventory Level - " + str(inventory1), font = ("Times", 12))
    button_frame = Frame(window)
    button_frame.pack()
    button1 = Button(button_frame, text="SUBTRACT 1 FROM INVENTORY", command= subtract_inventory)
    button1.grid(row=0, column=0)

    button2 = Button(button_frame, text="ADD 1 TO INVENTORY", command= add_inventory)
    button2.grid(row=0, column=1)
    source = Label(window, text = "Source - " + source1, font = ("Times", 12))
    link = Label(window, text="Link - " + link1, font = ("Times", 12))
    lead_time = Label(window, text="Lead Time - " + lead_time1, font = ("Times", 12))
    cost = Label(window, text="Cost - " + cost1, font = ("Times", 12))
    inventory_level.pack()
    source.pack()
    link.pack()
    lead_time.pack()
    cost.pack()
    def close():
        window.destroy()
    Button(window, text = "Exit",  command = close).pack()

def create_category_window(category1, name1, stock1, time1):
    window = tk.Toplevel(root)
    window.geometry("500x300")
    product_name = Label(window, text = category1, font = ("Times", 24))
    product_name.pack()
    info = Label(window, text = "Product              Stock", font = ("Times", 12))
    info.pack()
    products = Label(window, text =name1+"             "+ str(stock1), font = ("Times", 12))
    products.pack()
    def close():
        window.destroy()
    Button(window, text = "Exit",  command = close).pack()

def low_stock_report():
    query = ("SELECT product_name, inventory_level FROM Products")

    cursor.execute(query)

    json_dict = {}

    for product_name, inventory_level in cursor:
        json_dict[product_name] = inventory_level

    json_file = json.dumps(json_dict)

    socket.send_json(json_file)

    message = socket.recv_json()
    json_dict = json.loads(message)
    print(f"received reply [ {message}]")
    boxed = tk.Label(box, text= json_dict)
    boxed.pack()



product_search = Label(root, text= "Product Search", font=("Times", 16))
product_search.pack()


query1 = ("SELECT product_name FROM Products")

cursor.execute(query1)

results = cursor.fetchall()

display_names = []

# Dropdown menu options
options = ['']

for names in results:
    options.append(names[0])

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Product")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create button, it will change label text
button = Button(root, text="Enter Selection", command=get_product_info).pack()


# Create Label
label = Label(root, text="")
label.pack()


category_search = Label(root, text= "Category Search", font=("Times", 16))
category_search.pack()
# Dropdown menu options
query2 = ("SELECT category_name FROM Categories")

cursor.execute(query2)

results = cursor.fetchall()

display_categories = []

# Dropdown menu options
options = ['']

for names in results:
    options.append(names[0])



click = StringVar()

click.set("Category")

drop = OptionMenu(root, click, *options)
drop.pack()

select_category = Label(root, text="")
select_category.pack()


button_click = Button(root, text="Enter Selection", command=get_category_info).pack()



run_report = tk.Button(root, text = 'Run Low Inventory Report', command = low_stock_report).pack()

box = tk.LabelFrame(root, text="Low Stock!", pady=20)
box.pack()




root.mainloop()


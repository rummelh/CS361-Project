# Import module
from tkinter import *
from tkinter.ttk import *
import tkinter as tk

# Create object
root = Tk()

# Adjust size
root.geometry("600x600")

inventory_management = Label(root, text= "Inventory Management", font=("Times", 24))
inventory_management.pack()


#Creates pop-up window for given product
def create_product_window():
    window = tk.Toplevel(root)
    window.geometry("300x300")
    product_name = Label(window, text = "Product name", font = ("Times", 24))
    product_name.pack()
    info = Label(window, text = "Inventory Level - \n Source - \n Link - \n Lead Time - \n Cost - \n Acceptable Stock "
    "Level - ", font = ("Times", 12))
    info.pack()
    def close():
        window.destroy()
    Button(window, text = "Exit",  command = close).pack()

def create_category_window():
    window = tk.Toplevel(root)
    window.geometry("500x300")
    product_name = Label(window, text = "Category name", font = ("Times", 24))
    product_name.pack()
    info = Label(window, text = "Product              Stock              Last update date/time", font = ("Times", 12))
    info.pack()
    products = Label(window, text = "Apples              10              3/8/23 4:00pm", font = ("Times", 12))
    products.pack()
    def close():
        window.destroy()
    Button(window, text = "Exit",  command = close).pack()

product_search = Label(root, text= "Product Search", font=("Times", 16))
product_search.pack()

# Dropdown menu options
options = [
    "Apple",
    "Bananas",
    "Beef",
    "Bread",
    "Broccoli",
    "Celery",
    "Cereal",
    "Chicken",
    "Cupcakes",
    "Grapes",
    "Ice Cream",
    "Pancake Mix",
    "Pears",
    "Peppers",
    "Pork",
    "Sour Cream",
    "Syrup",
    "Tortillas",
    "Turkey",
    "Yogurt",
]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Product")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create button, it will change label text
button = Button(root, text="Enter Selection", command=create_product_window).pack()

# Create Label
label = Label(root, text="")
label.pack()


category_search = Label(root, text= "Category Search", font=("Times", 16))
category_search.pack()
# Dropdown menu options
options = [
    "Fruits",
    "Vegetables",
    "Meat",
    "Breakfast Foods",
    "Dairy",
    "Baked Goods"
]


click = StringVar()

click.set("Category")

drop = OptionMenu(root, click, *options)
drop.pack()

select_category = Label(root, text="")
select_category.pack()


button_click = Button(root, text="Enter Selection", command=create_category_window).pack()

box = tk.LabelFrame(root, text = "Low Stock!", pady = 20)
box.pack()
boxed = tk.Label(box, text="- Cupcakes \n - Ice Cream")
boxed.pack()

root.mainloop()


import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3

# Initialize or connect to the SQLite database
conn = sqlite3.connect('pos_system.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY,name TEXT,price REAL,stock INTEGER)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY,product_id INTEGER,quantity INTEGER,total REAL)")
# Create the main application window
app = tk.Tk()
app.geometry("1280x720")
app.title("Point of Sale System")

# Create a treeview to display products
product_tree = ttk.Treeview(app, columns=("ID", "Name", "Price", "Stock"), show="headings")
product_tree.heading("ID", text="ID")
product_tree.heading("Name", text="Name")
product_tree.heading("Price", text="Price")
product_tree.heading("Stock", text="Stock")


# Function to populate the product tree
def populate_product_tree():
    product_tree.delete(*product_tree.get_children())
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        product_tree.insert("", "end", values=row)


populate_product_tree()

# Create labels and entry fields for product details
product_name_label = tk.Label(app, text="Product Name:")
product_name_entry = tk.Entry(app)

product_price_label = tk.Label(app, text="Price:")
product_price_entry = tk.Entry(app)

product_stock_label = tk.Label(app, text="Stock:")
product_stock_entry = tk.Entry(app)


# Function to add a product to the database and update the product tree
def add_product():
    name = product_name_entry.get()
    price = float(product_price_entry.get())
    stock = int(product_stock_entry.get())
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    populate_product_tree()
    product_name_entry.delete(0, "end")
    product_price_entry.delete(0, "end")
    product_stock_entry.delete(0, "end")


# Function to delete a product from the database
def delete_product():
    selected_item = product_tree.selection()
    if selected_item:
        product_id = product_tree.item(selected_item, 'values')[0]
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        populate_product_tree()


# Create buttons for adding and deleting products
add_product_button = tk.Button(app, text="Add Product", command=add_product)
delete_product_button = tk.Button(app, text="Delete Product", command=delete_product)
delete_product_button.place(relx=1, x=-250, y=230, anchor=NE)
# Create a label for the sales section
sales_label = tk.Label(app, text="Sales")

# Create a treeview to display sales
sales_tree = ttk.Treeview(app, columns=("ID", "Product ID", "Quantity", "Total"), show="headings")
sales_tree.heading("ID", text="ID")
sales_tree.heading("Product ID", text="Product ID")
sales_tree.heading("Quantity", text="Quantity")
sales_tree.heading("Total", text="Total")


# Function to make a sale and update the sales tree
def make_sale():
    product_id = product_id_entry.get()
    quantity = int(quantity_entry.get())
    cursor.execute("SELECT name, price, stock FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    if product and product[2] >= quantity:
        total = product[1] * quantity
        cursor.execute("INSERT INTO sales (product_id, quantity, total) VALUES (?, ?, ?)",
                       (product_id, quantity, total))
        cursor.execute("UPDATE products SET stock=? WHERE id=?", (product[2] - quantity, product_id))
        conn.commit()
        populate_product_tree()
        populate_sales_tree()
        product_id_entry.delete(0, "end")
        quantity_entry.delete(0, "end")


# Function to populate the sales tree
def populate_sales_tree():
    sales_tree.delete(*sales_tree.get_children())
    cursor.execute("SELECT * FROM sales")
    for row in cursor.fetchall():
        sales_tree.insert("", "end", values=row)


# Create labels and entry fields for sales details
product_id_label = tk.Label(app, text="Product ID:")
product_id_entry = tk.Entry(app)

quantity_label = tk.Label(app, text="Quantity:")
quantity_entry = tk.Entry(app)

# Create a button to make a sale
make_sale_button = tk.Button(app, text="Make Sale", command=make_sale)

# Pack the widgets
product_tree.pack()
product_name_label.pack()
product_name_entry.pack()
product_price_label.pack()
product_price_entry.pack()
product_stock_label.pack()
product_stock_entry.pack()
add_product_button.pack()
sales_label.pack()
sales_tree.pack()
product_id_label.pack()
product_id_entry.pack()
quantity_label.pack()
quantity_entry.pack()
make_sale_button.pack()


# Close the database connection when the application is closed
def on_closing():
    conn.close()
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

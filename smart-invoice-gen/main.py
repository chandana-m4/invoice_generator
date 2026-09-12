import tkinter as tk
from tkinter import messagebox, ttk
import os
import re

from pdf_generator import create_invoice


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()
window.title("Chandu Technologies - Smart Invoice")
window.state("zoomed")
window.resizable(True, True)
window.configure(bg="#f5f3ff")


# =========================================================
# SCROLLABLE AREA
# =========================================================

main_canvas = tk.Canvas(
    window,
    bg="#f5f3ff",
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    window,
    orient="vertical",
    command=main_canvas.yview
)

scrollable_frame = tk.Frame(
    main_canvas,
    bg="#f5f3ff"
)

canvas_window = main_canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="n"
)


def update_scroll_region(event=None):
    main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )


def resize_content(event):
    main_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


scrollable_frame.bind(
    "<Configure>",
    update_scroll_region
)

main_canvas.bind(
    "<Configure>",
    resize_content
)

main_canvas.configure(
    yscrollcommand=scrollbar.set
)

main_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# =========================================================
# MOUSE SCROLL
# =========================================================

def mouse_scroll(event):

    if event.delta:
        main_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


window.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# =========================================================
# MAIN CONTENT
# =========================================================

content = tk.Frame(
    scrollable_frame,
    bg="#f5f3ff"
)

content.pack(
    fill="x",
    padx=70,
    pady=20
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    content,
    text="CHANDU TECHNOLOGIES",
    font=("Arial", 28, "bold"),
    bg="#f5f3ff",
    fg="#5b21b6"
)

title.pack(
    pady=(5, 2)
)


subtitle = tk.Label(
    content,
    text="SMART INVOICE GENERATOR",
    font=("Arial", 12, "bold"),
    bg="#f5f3ff",
    fg="#666666"
)

subtitle.pack(
    pady=(0, 20)
)


# =========================================================
# CUSTOMER DETAILS
# =========================================================

customer_frame = tk.LabelFrame(
    content,
    text="  Customer Details  ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#5b21b6",
    padx=25,
    pady=12
)

customer_frame.pack(
    fill="x",
    pady=8
)

customer_frame.columnconfigure(
    1,
    weight=1
)


def create_label(parent, text, row):

    tk.Label(
        parent,
        text=text,
        bg="white",
        font=("Arial", 10)
    ).grid(
        row=row,
        column=0,
        sticky="w",
        pady=7
    )


create_label(
    customer_frame,
    "Company Name",
    0
)

company_entry = tk.Entry(
    customer_frame,
    font=("Arial", 10)
)

company_entry.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


create_label(
    customer_frame,
    "Customer Name",
    1
)

customer_entry = tk.Entry(
    customer_frame,
    font=("Arial", 10)
)

customer_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


create_label(
    customer_frame,
    "Phone Number",
    2
)

phone_entry = tk.Entry(
    customer_frame,
    font=("Arial", 10)
)

phone_entry.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


create_label(
    customer_frame,
    "Email Address",
    3
)

email_entry = tk.Entry(
    customer_frame,
    font=("Arial", 10)
)

email_entry.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)

email_entry.insert(
    0,
    "chandusc253@gmail.com"
)


# =========================================================
# PRODUCT DETAILS
# =========================================================

product_frame = tk.LabelFrame(
    content,
    text="  Add / Edit Product  ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#5b21b6",
    padx=25,
    pady=12
)

product_frame.pack(
    fill="x",
    pady=10
)

product_frame.columnconfigure(
    1,
    weight=1
)


create_label(
    product_frame,
    "Product Name",
    0
)

product_entry = tk.Entry(
    product_frame,
    font=("Arial", 10)
)

product_entry.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


create_label(
    product_frame,
    "Quantity",
    1
)

quantity_entry = tk.Entry(
    product_frame,
    font=("Arial", 10)
)

quantity_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


create_label(
    product_frame,
    "Price",
    2
)

price_entry = tk.Entry(
    product_frame,
    font=("Arial", 10)
)

price_entry.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=20,
    pady=7
)


products = []
editing_index = None


# =========================================================
# PRODUCT TABLE
# =========================================================

table_frame = tk.LabelFrame(
    content,
    text="  Products  ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#5b21b6",
    padx=15,
    pady=12
)

table_frame.pack(
    fill="x",
    pady=8
)


columns = (
    "product",
    "quantity",
    "price",
    "total"
)


product_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=7
)


product_table.heading(
    "product",
    text="PRODUCT"
)

product_table.heading(
    "quantity",
    text="QTY"
)

product_table.heading(
    "price",
    text="PRICE"
)

product_table.heading(
    "total",
    text="TOTAL"
)


product_table.column(
    "product",
    width=500,
    anchor="w"
)

product_table.column(
    "quantity",
    width=120,
    anchor="center"
)

product_table.column(
    "price",
    width=180,
    anchor="e"
)

product_table.column(
    "total",
    width=180,
    anchor="e"
)


product_table.pack(
    fill="x"
)


style = ttk.Style()

style.configure(
    "Treeview",
    rowheight=32,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)


# =========================================================
# TOTAL SUMMARY
# =========================================================

total_frame = tk.LabelFrame(
    content,
    text="  Invoice Summary  ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#5b21b6",
    padx=25,
    pady=12
)

total_frame.pack(
    fill="x",
    pady=8
)


subtotal_label = tk.Label(
    total_frame,
    text="Subtotal: Rs. 0.00",
    font=("Arial", 11, "bold"),
    bg="white"
)

subtotal_label.pack(
    anchor="e",
    pady=3
)


discount_label = tk.Label(
    total_frame,
    text="Discount: Rs. 0.00",
    font=("Arial", 11, "bold"),
    bg="white"
)

discount_label.pack(
    anchor="e",
    pady=3
)


gst_label = tk.Label(
    total_frame,
    text="GST: Rs. 0.00",
    font=("Arial", 11, "bold"),
    bg="white"
)

gst_label.pack(
    anchor="e",
    pady=3
)


grand_total_label = tk.Label(
    total_frame,
    text="Grand Total: Rs. 0.00",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#5b21b6"
)

grand_total_label.pack(
    anchor="e",
    pady=6
)


# =========================================================
# GST / DISCOUNT
# =========================================================

tax_frame = tk.Frame(
    content,
    bg="#f5f3ff"
)

tax_frame.pack(
    pady=10
)


tk.Label(
    tax_frame,
    text="GST (%)",
    bg="#f5f3ff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=8
)


gst_entry = tk.Entry(
    tax_frame,
    width=15,
    font=("Arial", 10)
)

gst_entry.grid(
    row=0,
    column=1,
    padx=8
)


tk.Label(
    tax_frame,
    text="Discount (%)",
    bg="#f5f3ff",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=2,
    padx=8
)


discount_entry = tk.Entry(
    tax_frame,
    width=15,
    font=("Arial", 10)
)

discount_entry.grid(
    row=0,
    column=3,
    padx=8
)


# =========================================================
# PAYMENT DETAILS
# =========================================================

payment_frame = tk.LabelFrame(
    content,
    text="  Payment Details  ",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#5b21b6",
    padx=25,
    pady=12
)

payment_frame.pack(
    fill="x",
    pady=8
)


tk.Label(
    payment_frame,
    text="Payment Method",
    bg="white",
    font=("Arial", 10)
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=7
)


payment_method = ttk.Combobox(
    payment_frame,
    values=[
        "Cash",
        "UPI",
        "Card",
        "Bank Transfer"
    ],
    state="readonly",
    width=35
)

payment_method.grid(
    row=0,
    column=1,
    padx=20,
    pady=7
)

payment_method.set("Cash")


tk.Label(
    payment_frame,
    text="Payment Status",
    bg="white",
    font=("Arial", 10)
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=7
)


payment_status = ttk.Combobox(
    payment_frame,
    values=[
        "Paid",
        "Pending"
    ],
    state="readonly",
    width=35
)

payment_status.grid(
    row=1,
    column=1,
    padx=20,
    pady=7
)

payment_status.set("Paid")


# =========================================================
# CALCULATE TOTAL
# =========================================================

def calculate_total():

    subtotal = 0

    for item in products:

        subtotal += (
            item["quantity"] *
            item["price"]
        )

    try:
        gst = float(
            gst_entry.get()
        )
    except ValueError:
        gst = 0

    try:
        discount = float(
            discount_entry.get()
        )
    except ValueError:
        discount = 0

    discount_amount = (
        subtotal * discount / 100
    )

    amount_after_discount = (
        subtotal - discount_amount
    )

    gst_amount = (
        amount_after_discount *
        gst / 100
    )

    grand_total = (
        amount_after_discount +
        gst_amount
    )

    subtotal_label.config(
        text=f"Subtotal: Rs. {subtotal:.2f}"
    )

    discount_label.config(
        text=f"Discount: Rs. {discount_amount:.2f}"
    )

    gst_label.config(
        text=f"GST: Rs. {gst_amount:.2f}"
    )

    grand_total_label.config(
        text=f"Grand Total: Rs. {grand_total:.2f}"
    )


# =========================================================
# AUTO CALCULATE WHEN GST / DISCOUNT CHANGES
# =========================================================

gst_entry.bind(
    "<KeyRelease>",
    lambda event: calculate_total()
)

discount_entry.bind(
    "<KeyRelease>",
    lambda event: calculate_total()
)


# =========================================================
# ADD PRODUCT
# =========================================================

def add_product():

    product = product_entry.get().strip()

    try:

        quantity = int(
            quantity_entry.get()
        )

        price = float(
            price_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Quantity must be a whole number and Price must be a number."
        )

        return

    if product == "":

        messagebox.showwarning(
            "Missing Product",
            "Please enter product name."
        )

        return

    if quantity <= 0:

        messagebox.showwarning(
            "Invalid Quantity",
            "Quantity must be greater than 0."
        )

        return

    if price < 0:

        messagebox.showwarning(
            "Invalid Price",
            "Price cannot be negative."
        )

        return

    item_total = quantity * price

    products.append({
        "product": product,
        "quantity": quantity,
        "price": price
    })

    product_table.insert(
        "",
        tk.END,
        values=(
            product,
            quantity,
            f"Rs. {price:.2f}",
            f"Rs. {item_total:.2f}"
        )
    )

    product_entry.delete(
        0,
        tk.END
    )

    quantity_entry.delete(
        0,
        tk.END
    )

    price_entry.delete(
        0,
        tk.END
    )

    calculate_total()


# =========================================================
# EDIT PRODUCT
# =========================================================

def edit_product():

    global editing_index

    selected = product_table.selection()

    if not selected:

        messagebox.showwarning(
            "Select Product",
            "Please select a product from the table."
        )

        return

    selected_item = selected[0]

    editing_index = product_table.index(
        selected_item
    )

    item = products[editing_index]

    product_entry.delete(
        0,
        tk.END
    )

    product_entry.insert(
        0,
        item["product"]
    )

    quantity_entry.delete(
        0,
        tk.END
    )

    quantity_entry.insert(
        0,
        item["quantity"]
    )

    price_entry.delete(
        0,
        tk.END
    )

    price_entry.insert(
        0,
        item["price"]
    )

    update_button.config(
        state="normal"
    )

    add_button.config(
        state="disabled"
    )


# =========================================================
# UPDATE PRODUCT
# =========================================================

def update_product():

    global editing_index

    if editing_index is None:
        return

    product = product_entry.get().strip()

    try:

        quantity = int(
            quantity_entry.get()
        )

        price = float(
            price_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Quantity must be a whole number and Price must be a number."
        )

        return

    if product == "":

        messagebox.showwarning(
            "Missing Product",
            "Please enter product name."
        )

        return

    if quantity <= 0:

        messagebox.showwarning(
            "Invalid Quantity",
            "Quantity must be greater than 0."
        )

        return

    if price < 0:

        messagebox.showwarning(
            "Invalid Price",
            "Price cannot be negative."
        )

        return

    products[editing_index] = {
        "product": product,
        "quantity": quantity,
        "price": price
    }

    selected_item = (
        product_table.get_children()
        [editing_index]
    )

    item_total = (
        quantity * price
    )

    product_table.item(
        selected_item,
        values=(
            product,
            quantity,
            f"Rs. {price:.2f}",
            f"Rs. {item_total:.2f}"
        )
    )

    product_entry.delete(
        0,
        tk.END
    )

    quantity_entry.delete(
        0,
        tk.END
    )

    price_entry.delete(
        0,
        tk.END
    )

    editing_index = None

    update_button.config(
        state="disabled"
    )

    add_button.config(
        state="normal"
    )

    calculate_total()

    messagebox.showinfo(
        "Updated",
        "Product updated successfully!"
    )


# =========================================================
# REMOVE PRODUCT
# =========================================================

def remove_product():

    global editing_index

    selected = product_table.selection()

    if not selected:

        messagebox.showwarning(
            "Select Product",
            "Please select a product first."
        )

        return

    selected_item = selected[0]

    index = product_table.index(
        selected_item
    )

    products.pop(index)

    product_table.delete(
        selected_item
    )

    editing_index = None

    update_button.config(
        state="disabled"
    )

    add_button.config(
        state="normal"
    )

    product_entry.delete(
        0,
        tk.END
    )

    quantity_entry.delete(
        0,
        tk.END
    )

    price_entry.delete(
        0,
        tk.END
    )

    calculate_total()


# =========================================================
# PRODUCT BUTTONS
# =========================================================

button_frame = tk.Frame(
    content,
    bg="#f5f3ff"
)

button_frame.pack(
    pady=10
)


add_button = tk.Button(
    button_frame,
    text="+  ADD PRODUCT",
    command=add_product,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=25,
    pady=9,
    relief="flat"
)

add_button.grid(
    row=0,
    column=0,
    padx=5
)


edit_button = tk.Button(
    button_frame,
    text="EDIT SELECTED",
    command=edit_product,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=25,
    pady=9,
    relief="flat"
)

edit_button.grid(
    row=0,
    column=1,
    padx=5
)


update_button = tk.Button(
    button_frame,
    text="UPDATE PRODUCT",
    command=update_product,
    bg="#5b21b6",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=25,
    pady=9,
    relief="flat",
    state="disabled"
)

update_button.grid(
    row=0,
    column=2,
    padx=5
)


remove_button = tk.Button(
    button_frame,
    text="REMOVE SELECTED",
    command=remove_product,
    bg="#eeeeee",
    fg="#333333",
    font=("Arial", 10, "bold"),
    padx=25,
    pady=9,
    relief="flat"
)

remove_button.grid(
    row=0,
    column=3,
    padx=5
)


# =========================================================
# VALIDATION
# =========================================================

def valid_email(email):

    pattern = (
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    return re.match(
        pattern,
        email
    ) is not None


def valid_phone(phone):

    digits = re.sub(
        r"\D",
        "",
        phone
    )

    return (
        len(digits) >= 10 and
        len(digits) <= 15
    )


# =========================================================
# GENERATE INVOICE
# =========================================================

def generate_invoice():

    company = company_entry.get().strip()
    customer = customer_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if company == "":

        messagebox.showwarning(
            "Missing Details",
            "Please enter company name."
        )

        return

    if customer == "":

        messagebox.showwarning(
            "Missing Details",
            "Please enter customer name."
        )

        return

    if phone == "":

        messagebox.showwarning(
            "Missing Details",
            "Please enter phone number."
        )

        return

    if not valid_phone(phone):

        messagebox.showwarning(
            "Invalid Phone",
            "Please enter a valid phone number."
        )

        return

    if email == "":

        messagebox.showwarning(
            "Missing Details",
            "Please enter email address."
        )

        return

    if not valid_email(email):

        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )

        return

    if len(products) == 0:

        messagebox.showwarning(
            "No Products",
            "Please add at least one product."
        )

        return

    try:

        gst = float(
            gst_entry.get()
            if gst_entry.get().strip()
            else 0
        )

        discount = float(
            discount_entry.get()
            if discount_entry.get().strip()
            else 0
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "GST and Discount must be numbers."
        )

        return

    if gst < 0 or gst > 100:

        messagebox.showwarning(
            "Invalid GST",
            "GST must be between 0 and 100."
        )

        return

    if discount < 0 or discount > 100:

        messagebox.showwarning(
            "Invalid Discount",
            "Discount must be between 0 and 100."
        )

        return

    selected_payment_method = (
        payment_method.get()
    )

    selected_payment_status = (
        payment_status.get()
    )

    try:

        pdf_path = create_invoice(
            company,
            customer,
            phone,
            email,
            products,
            gst,
            discount,
            selected_payment_method,
            selected_payment_status
        )

        os.startfile(
            os.path.abspath(pdf_path)
        )

        messagebox.showinfo(
            "Success",
            "Invoice generated successfully!\n\n"
            "PDF opened automatically."
        )

    except Exception as e:

        messagebox.showerror(
            "Invoice Error",
            "Something went wrong:\n\n"
            + str(e)
        )


# =========================================================
# MAIN BUTTONS
# =========================================================

generate_button = tk.Button(
    content,
    text="GENERATE INVOICE",
    command=generate_invoice,
    bg="#5b21b6",
    fg="white",
    font=("Arial", 13, "bold"),
    padx=50,
    pady=13,
    relief="flat"
)

generate_button.pack(
    pady=10
)


def open_invoices_folder():

    folder_path = os.path.abspath(
        "invoices"
    )

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)

    os.startfile(
        folder_path
    )


open_folder_button = tk.Button(
    content,
    text="OPEN INVOICES FOLDER",
    command=open_invoices_folder,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=25,
    pady=9,
    relief="flat"
)

open_folder_button.pack(
    pady=5
)


# =========================================================
# CLEAR FORM
# =========================================================

def clear_form():

    global editing_index

    company_entry.delete(
        0,
        tk.END
    )

    customer_entry.delete(
        0,
        tk.END
    )

    phone_entry.delete(
        0,
        tk.END
    )

    email_entry.delete(
        0,
        tk.END
    )

    email_entry.insert(
        0,
        "chandusc253@gmail.com"
    )

    product_entry.delete(
        0,
        tk.END
    )

    quantity_entry.delete(
        0,
        tk.END
    )

    price_entry.delete(
        0,
        tk.END
    )

    gst_entry.delete(
        0,
        tk.END
    )

    discount_entry.delete(
        0,
        tk.END
    )

    payment_method.set(
        "Cash"
    )

    payment_status.set(
        "Paid"
    )

    products.clear()

    for item in product_table.get_children():

        product_table.delete(
            item
        )

    subtotal_label.config(
        text="Subtotal: Rs. 0.00"
    )

    discount_label.config(
        text="Discount: Rs. 0.00"
    )

    gst_label.config(
        text="GST: Rs. 0.00"
    )

    grand_total_label.config(
        text="Grand Total: Rs. 0.00"
    )

    editing_index = None

    update_button.config(
        state="disabled"
    )

    add_button.config(
        state="normal"
    )

    main_canvas.yview_moveto(0)


# =========================================================
# CLEAR BUTTON
# =========================================================

clear_button = tk.Button(
    content,
    text="CLEAR FORM",
    command=clear_form,
    bg="#eeeeee",
    fg="#333333",
    font=("Arial", 10, "bold"),
    padx=30,
    pady=9,
    relief="flat"
)

clear_button.pack(
    pady=(5, 30)
)


# =========================================================
# START APPLICATION
# =========================================================

window.mainloop()
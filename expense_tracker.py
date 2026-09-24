import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date, datetime
import csv


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL
)
""")

# Add transaction_type to old database if required
cursor.execute("PRAGMA table_info(expenses)")
columns = [row[1] for row in cursor.fetchall()]

if "transaction_type" not in columns:
    cursor.execute("""
        ALTER TABLE expenses
        ADD COLUMN transaction_type TEXT DEFAULT 'Expense'
    """)

conn.commit()


# =========================================================
# WINDOW
# =========================================================

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1050x750")
root.configure(bg="#F3F4F6")


# =========================================================
# COLORS
# =========================================================

BG = "#F3F4F6"
WHITE = "#FFFFFF"
DARK = "#111827"
GRAY = "#6B7280"
GREEN = "#15803D"
RED = "#DC2626"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
BORDER = "#E5E7EB"


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=20, pady=(15, 5))

tk.Label(
    header,
    text="Personal Finance Dashboard",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w")

tk.Label(
    header,
    text="Manage your income and expenses easily",
    font=("Arial", 10),
    bg=BG,
    fg=GRAY
).pack(anchor="w", pady=(3, 0))


# =========================================================
# DASHBOARD
# =========================================================

dashboard = tk.Frame(root, bg=BG)
dashboard.pack(fill="x", padx=20, pady=15)


def make_card(parent, title, value, value_color):

    frame = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        frame,
        text=title,
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=GRAY
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 2)
    )

    label = tk.Label(
        frame,
        text=value,
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=value_color
    )

    label.pack(
        anchor="w",
        padx=15,
        pady=(0, 12)
    )

    return frame, label


total_card, total_label = make_card(
    dashboard,
    "TOTAL TRANSACTIONS",
    "₹0.00",
    PURPLE
)

total_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4
)


income_card, income_label = make_card(
    dashboard,
    "TOTAL INCOME",
    "₹0.00",
    GREEN
)

income_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4
)


expense_card, expense_label = make_card(
    dashboard,
    "TOTAL EXPENSE",
    "₹0.00",
    RED
)

expense_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4
)


balance_card, balance_label = make_card(
    dashboard,
    "CURRENT BALANCE",
    "₹0.00",
    BLUE
)

balance_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=4
)


# =========================================================
# SUMMARY
# =========================================================

summary = tk.Frame(root, bg=BG)
summary.pack(fill="x", padx=25)

summary_label = tk.Label(
    summary,
    text="Transactions: 0     |     This Month: ₹0.00     |     Top Category: None",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=GRAY
)

summary_label.pack(anchor="w")


# =========================================================
# MAIN AREA
# =========================================================

main_area = tk.Frame(root, bg=BG)
main_area.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


# =========================================================
# FORM
# =========================================================

form = tk.Frame(
    main_area,
    bg=WHITE,
    width=320,
    highlightbackground=BORDER,
    highlightthickness=1
)

form.pack(
    side="left",
    fill="y",
    padx=(0, 10)
)

form.pack_propagate(False)


tk.Label(
    form,
    text="Add Transaction",
    font=("Arial", 16, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=18,
    pady=(15, 12)
)


def label(text):

    tk.Label(
        form,
        text=text,
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=GRAY
    ).pack(
        anchor="w",
        padx=18,
        pady=(5, 3)
    )


label("DATE")

date_entry = tk.Entry(
    form,
    font=("Arial", 10)
)

date_entry.pack(
    fill="x",
    padx=18
)

date_entry.insert(
    0,
    str(date.today())
)


label("TYPE")

type_entry = ttk.Combobox(
    form,
    values=["Expense", "Income"],
    state="readonly",
    font=("Arial", 10)
)

type_entry.pack(
    fill="x",
    padx=18
)

type_entry.set("Expense")


label("CATEGORY")

categories = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Education",
    "Entertainment",
    "Medical",
    "Other"
]

category_entry = ttk.Combobox(
    form,
    values=categories,
    state="readonly",
    font=("Arial", 10)
)

category_entry.pack(
    fill="x",
    padx=18
)

category_entry.set("Food")


label("DESCRIPTION")

description_entry = tk.Entry(
    form,
    font=("Arial", 10)
)

description_entry.pack(
    fill="x",
    padx=18
)


label("AMOUNT")

amount_entry = tk.Entry(
    form,
    font=("Arial", 10)
)

amount_entry.pack(
    fill="x",
    padx=18
)


# =========================================================
# FUNCTIONS
# =========================================================

def update_dashboard():

    # Income
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE transaction_type = 'Income'
    """)

    income = cursor.fetchone()[0]

    # Expense
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE transaction_type = 'Expense'
    """)

    expense = cursor.fetchone()[0]

    # Balance
    balance = income - expense

    # Total money involved
    total = income + expense

    # Transaction count
    cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
    """)

    count = cursor.fetchone()[0]

    # Current month expenses
    month = datetime.now().strftime("%Y-%m")

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE transaction_type = 'Expense'
        AND expense_date LIKE ?
    """, (month + "%",))

    month_expense = cursor.fetchone()[0]

    # Top category
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE transaction_type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
    """)

    top = cursor.fetchone()

    if top:
        top_text = f"{top[0]} (₹{top[1]:.2f})"
    else:
        top_text = "None"

    # Update cards
    total_label.config(
        text=f"₹{total:.2f}"
    )

    income_label.config(
        text=f"₹{income:.2f}"
    )

    expense_label.config(
        text=f"₹{expense:.2f}"
    )

    balance_label.config(
        text=f"₹{balance:.2f}"
    )

    summary_label.config(
        text=(
            f"Transactions: {count}     |     "
            f"This Month: ₹{month_expense:.2f}     |     "
            f"Top Category: {top_text}"
        )
    )


def load_data():

    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("""
        SELECT
            id,
            expense_date,
            transaction_type,
            category,
            description,
            amount
        FROM expenses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:

        tree.insert(
            "",
            "end",
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                f"₹{row[5]:.2f}"
            )
        )


def clear_fields():

    date_entry.delete(0, tk.END)
    date_entry.insert(0, str(date.today()))

    type_entry.set("Expense")
    category_entry.set("Food")

    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


def add_transaction():

    d = date_entry.get().strip()
    t = type_entry.get().strip()
    c = category_entry.get().strip()
    desc = description_entry.get().strip()
    amount = amount_entry.get().strip()

    if not d:
        messagebox.showerror("Error", "Enter date")
        return

    if not desc:
        messagebox.showerror("Error", "Enter description")
        return

    if not amount:
        messagebox.showerror("Error", "Enter amount")
        return

    try:
        amount_value = float(amount)

        if amount_value <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid amount"
        )
        return

    cursor.execute("""
        INSERT INTO expenses
        (
            expense_date,
            category,
            description,
            amount,
            transaction_type
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        d,
        c,
        desc,
        amount_value,
        t
    ))

    conn.commit()

    clear_fields()
    load_data()
    update_dashboard()

    messagebox.showinfo(
        "Success",
        "Transaction added successfully!"
    )


def select_transaction(event):

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(
        selected[0]
    )["values"]

    date_entry.delete(0, tk.END)
    date_entry.insert(0, values[1])

    type_entry.set(values[2])

    category_entry.set(values[3])

    description_entry.delete(0, tk.END)
    description_entry.insert(0, values[4])

    amount_entry.delete(0, tk.END)

    amount_text = str(values[5]).replace("₹", "")

    amount_entry.insert(
        0,
        amount_text
    )


def edit_transaction():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a transaction first"
        )
        return

    values = tree.item(
        selected[0]
    )["values"]

    transaction_id = values[0]

    try:
        amount_value = float(
            amount_entry.get().strip()
        )

        if amount_value <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter a valid amount"
        )
        return

    cursor.execute("""
        UPDATE expenses
        SET
            expense_date = ?,
            transaction_type = ?,
            category = ?,
            description = ?,
            amount = ?
        WHERE id = ?
    """, (
        date_entry.get().strip(),
        type_entry.get().strip(),
        category_entry.get().strip(),
        description_entry.get().strip(),
        amount_value,
        transaction_id
    ))

    conn.commit()

    clear_fields()
    load_data()
    update_dashboard()

    messagebox.showinfo(
        "Success",
        "Transaction updated successfully!"
    )


def delete_transaction():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a transaction first"
        )
        return

    values = tree.item(
        selected[0]
    )["values"]

    transaction_id = values[0]

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Delete this transaction?"
    )

    if answer:

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (transaction_id,)
        )

        conn.commit()

        clear_fields()
        load_data()
        update_dashboard()


def search_transaction():

    text = search_entry.get().strip()

    for item in tree.get_children():
        tree.delete(item)

    if not text:

        load_data()
        return

    cursor.execute("""
        SELECT
            id,
            expense_date,
            transaction_type,
            category,
            description,
            amount
        FROM expenses
        WHERE category LIKE ?
        OR description LIKE ?
        OR transaction_type LIKE ?
        ORDER BY id DESC
    """, (
        "%" + text + "%",
        "%" + text + "%",
        "%" + text + "%"
    ))

    rows = cursor.fetchall()

    for row in rows:

        tree.insert(
            "",
            "end",
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                f"₹{row[5]:.2f}"
            )
        )


def export_csv():

    cursor.execute("""
        SELECT
            id,
            expense_date,
            transaction_type,
            category,
            description,
            amount
        FROM expenses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    with open(
        "expenses_report.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Date",
            "Type",
            "Category",
            "Description",
            "Amount"
        ])

        writer.writerows(rows)

    messagebox.showinfo(
        "Export Complete",
        "expenses_report.csv created!"
    )


# =========================================================
# FORM BUTTONS
# =========================================================

button_area = tk.Frame(
    form,
    bg=WHITE
)

button_area.pack(
    fill="x",
    padx=18,
    pady=15
)


tk.Button(
    button_area,
    text="ADD TRANSACTION",
    command=add_transaction,
    bg=BLUE,
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    pady=8
).pack(
    fill="x",
    pady=3
)


tk.Button(
    button_area,
    text="EDIT SELECTED",
    command=edit_transaction,
    font=("Arial", 10, "bold"),
    relief="flat",
    pady=7
).pack(
    fill="x",
    pady=3
)


tk.Button(
    button_area,
    text="DELETE SELECTED",
    command=delete_transaction,
    fg=RED,
    font=("Arial", 10, "bold"),
    relief="flat",
    pady=7
).pack(
    fill="x",
    pady=3
)


tk.Button(
    button_area,
    text="CLEAR",
    command=clear_fields,
    font=("Arial", 10),
    relief="flat",
    pady=7
).pack(
    fill="x",
    pady=3
)


tk.Button(
    button_area,
    text="EXPORT CSV",
    command=export_csv,
    font=("Arial", 10),
    relief="flat",
    pady=7
).pack(
    fill="x",
    pady=3
)


# =========================================================
# TRANSACTIONS
# =========================================================

transactions = tk.Frame(
    main_area,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)

transactions.pack(
    side="right",
    fill="both",
    expand=True
)


tk.Label(
    transactions,
    text="Recent Transactions",
    font=("Arial", 16, "bold"),
    bg=WHITE,
    fg=DARK
).pack(
    anchor="w",
    padx=15,
    pady=(15, 8)
)


# Search bar

search_area = tk.Frame(
    transactions,
    bg=WHITE
)

search_area.pack(
    fill="x",
    padx=15,
    pady=(0, 8)
)


search_entry = tk.Entry(
    search_area,
    font=("Arial", 10)
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)


tk.Button(
    search_area,
    text="Search",
    command=search_transaction
).pack(side="left")


# =========================================================
# TABLE
# =========================================================

table_area = tk.Frame(
    transactions,
    bg=WHITE
)

table_area.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


columns = (
    "ID",
    "Date",
    "Type",
    "Category",
    "Description",
    "Amount"
)

tree = ttk.Treeview(
    table_area,
    columns=columns,
    show="headings"
)


for col in columns:

    tree.heading(
        col,
        text=col
    )


tree.column(
    "ID",
    width=45
)

tree.column(
    "Date",
    width=90
)

tree.column(
    "Type",
    width=75
)

tree.column(
    "Category",
    width=90
)

tree.column(
    "Description",
    width=150
)

tree.column(
    "Amount",
    width=90
)


tree.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = ttk.Scrollbar(
    table_area,
    orient="vertical",
    command=tree.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

tree.configure(
    yscrollcommand=scrollbar.set
)


tree.bind(
    "<<TreeviewSelect>>",
    select_transaction
)


# =========================================================
# START APP
# =========================================================

load_data()
update_dashboard()

root.mainloop()

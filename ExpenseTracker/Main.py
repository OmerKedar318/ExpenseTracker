from Database import *
from Classes import *
import tkinter as tk
from tkinter import ttk, messagebox


def alert(budgets):
    sum_categories = sum_categories_exp()
    for key in budgets:
        if sum_categories[key] > budgets[key]:
            messagebox.showerror("Error", "Went out of budget in " + key)
        elif sum_categories[key] > 0.9 * budgets[key]:
            messagebox.showinfo("Pay Attention!", "Nearing the budget limit in " + key)


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)


root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Amount").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Label(root, text="Category").pack()
entry_category = tk.Entry(root)
entry_category.pack()

tk.Label(root, text="Date (DD.MM.YYYY)").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Label(root, text="Description").pack()
entry_desc = tk.Entry(root)
entry_desc.pack()

tk.Button(root, text="Add Expense", command=lambda: insert_exp(Expense(entry_amount.get(), entry_category.get(), entry_date.get(), entry_desc.get()))).pack()
tk.Button(root, text="Delete Selected", command=lambda: remove_exp(Expense(entry_amount.get(), entry_category.get(), entry_date.get(), entry_desc.get()))).pack()

tree = ttk.Treeview(root, columns=("Amount", "Category", "Date", "Description"), show="headings")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Date", text="Date")
tree.heading("Description", text="Description")
tree.pack()

load_expenses()

root.mainloop()

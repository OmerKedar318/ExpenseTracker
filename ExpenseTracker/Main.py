from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, TableStyle, Table
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
            messagebox.showwarning("Warning", "Nearing the budget limit in " + key)


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)


def add_expense():
    try:
        amount = float(entry_amount.get())
        category = entry_category.get()
        date = entry_date.get()
        description = entry_desc.get()
        if not category or not date or not amount:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        exp = Expense(amount, category, date, description)
        insert_exp(exp)
        load_expenses()
        messagebox.showinfo("Success", "Expense added successfully.")
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")


def delete_selected():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an expense to delete.")
        return
    values = tree.item(selected_item, 'values')
    if values:
        amount, category, date, description = values
        exp = Expense(amount, category, date, description)
        remove_exp(exp)
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Expense deleted successfully.")


def fetch_expenses():
    c.execute("SELECT * FROM expenses")
    data = c.fetchall()
    return data


def export_table_to_pdf(filename, data):
    if not data:
        messagebox.showerror("No data to export!")
        return
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    table_data = [["Amount", "Category", "Date", "Description"]]
    table_data.extend(data)
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    pdf.build([table])
    messagebox.showinfo(f"PDF exported successfully as {filename}")


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

tk.Button(root, text="Add Expense", command=add_expense).pack()
tk.Button(root, text="Delete Selected", command=delete_selected).pack()
tk.Button(root, text="Export to PDF", command=lambda: export_table_to_pdf("expenses.pdf", fetch_expenses())).pack()

tree = ttk.Treeview(root, columns=("Amount", "Category", "Date", "Description"), show="headings")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Date", text="Date")
tree.heading("Description", text="Description")
tree.pack()

load_expenses()

root.mainloop()

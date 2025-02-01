import sqlite3

conn = sqlite3.connect("expenses.db")
c = conn.cursor()

conn2 = sqlite3.connect("revenues.db")
c2 = conn2.cursor()


def insert_exp(exp):
    with conn:
        c.execute("INSERT INTO expenses VALUES (:amount, :category, :date, :description)",
                  {'amount': exp.amount, 'category': exp.category, 'date': exp.date, 'description': exp.description})


def remove_exp(exp):
    with conn:
        c.execute("DELETE from expenses WHERE date = :date AND description = :description",
                  {'date': exp.date, 'description': exp.description})


def update_amount_exp(exp, amount):
    with conn:
        c.execute("""UPDATE expenses SET amount = :amount
                    WHERE date = :date AND description = :description""",
                  {'amount': amount, 'category': exp.category, 'date': exp.date, 'description': exp.description})


def insert_rev(rev):
    with conn2:
        c2.execute("INSERT INTO revenues VALUES (:amount, :category, :date, :description)",
                  {'amount': rev.amount, 'category': rev.category, 'date': rev.date, 'description': rev.description})


def remove_rev(rev):
    with conn2:
        c2.execute("DELETE from revenues WHERE date = :date AND description = :description",
                  {'date': rev.date, 'description': rev.description})


def update_amount_rev(rev, amount):
    with conn2:
        c2.execute("""UPDATE revenues SET amount = :amount
                    WHERE date = :date AND description = :description""",
                  {'amount': amount, 'category': rev.category, 'date': rev.date, 'description': rev.description})


def sum_all_exp():
    sum = 0
    with conn:
        c.execute("SELECT * FROM expenses")
        l = c.fetchall()
        for i in l:
            sum += i[0]
    return sum


def sum_all_rev():
    sum = 0
    with conn2:
        c2.execute("SELECT * FROM revenues")
        l = c2.fetchall()
        for i in l:
            sum += i[0]
    return sum


def sum_category_exp(category):
    sum = 0
    with conn:
        c.execute("SELECT * FROM expenses WHERE category = :category", {'category': category})
        l = c.fetchall()
        for i in l:
            sum += i[0]
    return sum


def sum_category_rev(category):
    sum = 0
    with conn2:
        c2.execute("SELECT * FROM revenues WHERE category = :category", {'category': category})
        l = c2.fetchall()
        for i in l:
            sum += i[0]
    return sum


def sum_categories_exp():
    categories = []
    dic = {}
    with conn:
        c.execute("SELECT * FROM expenses")
        l = c.fetchall()
        for i in l:
            if i[1] not in categories:
                categories.append(i[1])
        for i in categories:
            dic[i] = sum_category_exp(i)
    return dic


def sum_categories_rev():
    categories = []
    dic = {}
    with conn2:
        c2.execute("SELECT * FROM revenues")
        l = c2.fetchall()
        for i in l:
            if i[1] not in categories:
                categories.append(i[1])
        for i in categories:
            dic[i] = sum_category_rev(i)
    return dic


def set_categories_budgets():
    categories = []
    budgets = {}
    with conn:
        c.execute("SELECT * FROM expenses")
        l = c.fetchall()
        for i in l:
            if i[1] not in categories:
                categories.append(i[1])
        for i in categories:
            budgets[i] = int(input("Enter budget... "))
    return budgets

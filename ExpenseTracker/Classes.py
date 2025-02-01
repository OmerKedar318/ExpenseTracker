class Expense:
    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self):
        return "Expense({}, '{}', '{}', '{}')".format(self.amount, self.category, self.date, self.description)


class Revenue:
    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self):
        return "Revenue({}, '{}', '{}', '{}')".format(self.amount, self.category, self.date, self.description)

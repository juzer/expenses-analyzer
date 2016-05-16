class Expense(object):
    def __init__(self, date, amount, title):
        self.date = date
        self.amount = amount
        self.title = title

    def __repr__(self):
        return "Date=%s, amount=%s, title='%s'" % (str(self.date), str(self.amount), self.title)
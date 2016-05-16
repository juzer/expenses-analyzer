from datetime import datetime
from decimal import *
from analyzer.model import Expense

class AbstractConverter(object):
    def convert_row(self, row):
        '''Parses row of data (taken as a list) and returns a Expense object'''
        raise NotImplementedError('This method is abstract')


class SabadellConverter(AbstractConverter):
    def convert_row(self, row):
        date = datetime.strptime(row[0], '%d/%m/%Y')
        amount = Decimal(row[3])
        title = row[1]
        return Expense(date, amount, title)
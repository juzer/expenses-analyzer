from analyzer.converters import SabadellConverter
import csv

class AbstractParser(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        '''Parses given file and returns a collection of Expense objects'''
        raise NotImplementedError('This method is abstract')


class SabadellParser(AbstractParser):
    def __init__(self, file_path):
        super(SabadellParser, self).__init__(file_path)
        self.converter = SabadellConverter()

    def parse(self):
        result = []
        for row in csv.reader(open(self.file_path, 'rb'), delimiter='|'):
            if not row[0].startswith("#"):
                result.append(self.converter.convert_row(row))
        return result
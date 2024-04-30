from pprint import pprint


class Cell:
    def __init__(self, row=None, column=None, value=None, fixed=None):
        self.column = column
        self.row = row
        self.value = value
        self.fixed = fixed

    def as_dict(self):
        return {
            'col': self.column,
            'row': self.row,
            'value': self.value,
            'fixed': self.fixed,
        }

    def __str__(self):
        return str(self.as_dict())


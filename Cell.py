
class Cell:
    def __init__(self, row=None, column=None, value=None, solved=None):
        self.column = column
        self.row = row
        self.value = value
        self.solved = solved
        self.posibilities = []

    def as_dict(self):
        return {
            'row': self.row,
            'col': self.column,
            'value': self.value,
            'posibilities': self.posibilities
        }

    def __str__(self):
        return str(self.as_dict())
    
    


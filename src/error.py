class MissingHeaderException(Exception): pass
class WrongHeaderException(Exception):
    def __init__(self, col_missing):
        self.col_missing = col_missing
class CoordinateNotANumber(Exception):
    def __init__(self, line_number, col, value):
        self.line_number = line_number
        self.col = col
        self.value = value

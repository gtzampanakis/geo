class MissingHeaderException(Exception):

    def __init__(self, filename):
        Exception.__init__(self, filename)
        self.filename = filename

    def __str__(self):
        return 'File "%s" has no header' % self.filename

class WrongHeaderException(Exception):

    def __init__(self, filename, col_missing):
        Exception.__init__(self, filename, col_missing)
        self.filename = filename
        self.col_missing = col_missing

    def __str__(self):
        return 'In file "%s": Header is missing column "%s"' % (
            self.filename,
            self.col_missing
        )

class CoordinateNotANumber(Exception):

    def __init__(self, filename, line_number, col, value):
        Exception.__init__(self, filename, line_number, col, value)
        self.filename = filename
        self.line_number = line_number
        self.col = col
        self.value = value

    def __str__(self):
        return ('In file "%s", line %s, column "%s", '
               'value is not a number: "%s"' % (
            self.filename, self.line_number, self.col, self.value
        ))

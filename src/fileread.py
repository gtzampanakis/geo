import csv

import geotypes as gt
import error

def get_csv_reader(path):
# Check the header. If it doesn't DictReader will not be able to return
# meaningful data.

    with open(path, 'rb') as infile:
        reader = csv.reader(infile)
        try:
            row = reader.next()
        except StopIteration as e:
            raise error.MissingHeaderException
        header_names = [col.strip() for col in row]
        for required_name in ['Latitude', 'Longitude']:
            if required_name not in header_names:
                raise error.WrongHeaderException(required_name)

    with open(path, 'rb') as infile:
        reader = csv.DictReader(infile)
        for rowi, row in enumerate(reader, 1):
            row['__line_number'] = rowi
            try:
                p = float(row['Latitude'])
            except ValueError as e:
                raise error.CoordinateNotANumber(
                    rowi, 'Latitude', row['Latitude'])
            try:
                l = float(row['Longitude'])
            except ValueError as e:
                raise error.CoordinateNotANumber(
                    rowi, 'Longitude', row['Longitude'])
            row['__coords'] = gt.Coords(
                float(row['Latitude']),
                float(row['Longitude'])
            )
            yield row

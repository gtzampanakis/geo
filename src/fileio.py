import collections
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

        for rowi, row in enumerate(reader, 1):
            data = collections.OrderedDict()
            for i in xrange(len(header_names)):
                if i < len(row):
                    data[header_names[i]] = row[i]

            data['__line_number'] = rowi
            try:
                p = float(data['Latitude'])
            except ValueError as e:
                raise error.CoordinateNotANumber(
                    rowi, 'Latitude', data['Latitude'])
            try:
                l = float(data['Longitude'])
            except ValueError as e:
                raise error.CoordinateNotANumber(
                    rowi, 'Longitude', data['Longitude'])
            yield data

def get_csv_writer_to_fobj(fobj, dicts):
    for dicti, d in enumerate(dicts):
        if dicti == 0:
            writer = csv.DictWriter(fobj, fieldnames = d.keys())
            writer.writeheader()
        writer.writerow(d)

def get_csv_writer(path, dicts):
    with open(path, 'wb') as outfile:
        return get_csv_writer_to_fobj(outfile, dicts)

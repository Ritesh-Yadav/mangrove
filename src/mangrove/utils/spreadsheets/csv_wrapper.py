# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import csv
import codecs


class CsvReader(object):
    def __init__(self, path):
        self.open(path)

    def open(self, path):
        self._file = codecs.open(path, encoding='utf-8')
        # http://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python/904085#904085
        self._csv_reader = csv.reader(self._file)

    def close(self):
        self._file.close()

    def __iter__(self):
        return self

    def next(self):
        """
        A CsvReader object is iterable (since we have defined __iter__
        and next methods. Each iteration of this object returns a row
        of data.
        """
        row = self._csv_reader.next()
        return [unicode(cell, 'utf-8') for cell in row]

    def _set_headers(self):
        self._headers = self.next()

    def iter_dicts(self):
        self._set_headers()
        for row in self:
            yield dict(zip(self._headers, row))
        self.close()

"""
csv_reader_util.py

DESCRIPTION:
    A wrapper and some logic around python's csv
    library to load and preprocess csv files.

TO USE:
    FILL THIS IN ~~~~

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/3/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""
import csv

class csv_reader_util(object):
    """
    A reader util for csvs built around Python's
    builtin csv library.

    SIG: Bool -> Object

    ARGS:
    --------------------------------
     - verbose_mode: toggle to echo extra output
                     while parsing csvs.
    """
    def __init__(self, verbose_mode=True):
        self.file_content = None
        self.verbose = verbose_mode

    def _get_csv_header(self):
        """
        PRIVATE_METHOD:
        Gets header of loaded CSV in an unchecked manner.

        SIG: None -> None
        """
        return self.file_content[0]

    def get_csv_header(self):
        """
        Gets header of loaded CSV.

        SIG: None -> None
        """
        if self.file_content != None:
            return self._get_csv_header()
        elif self.verbose:
            print("[ERROR]: No CSV has been loaded! Returning None Type...")
        return None

    def _get_csv_body(self):
        """
        Gets body of loaded CSV in an unchecked manner.

        SIG: None -> None
        """
        return self.file_content[1::]

    def get_csv_body(self):
        """
        Gets body of loaded CSV.

        SIG: None -> None
        """
        print("[STATUS]: retrieving CSV body...") if self.verbose else None
        if self.file_content != None:
            return self._get_csv_body()
        elif self.verbose:
            print("[ERROR]: No CSV has been loaded! Returning None Type...")
        return None

    def load_csv(self, filename):
        """
        Loads a csv into self.file_content

        SIG: String -> None

        ARGS:
        ---------------------------
         - filename: the direct path to the file you
                     want to load.
        """
        try:
            unprocessed_csv = open(filename, "r", encoding='utf-8', errors='ignore')
            self.file_content = list(list(row) for row in csv.reader(unprocessed_csv, delimiter=","))
            unprocessed_csv.close()
        except FileNotFoundError:
            print("[ERROR]: Could not find specified file. Did you pass a correct path?")

    def get_column_indexes(self, column_headers):
        """
        Returns a list of index of the string
        specified in column_headers from self.file_content.

        SIG: String -> List[Int]

        ARGS:
        --------------------------
         - column_headers: the header values of the columns
                           you want the index of.
        """
        indexes = []
        for tag in column_headers:
            try:
                indexes.append(self.file_content[0].index(tag))
            except ValueError:
                print("[ERROR]: column tag {} is not in loaded CSV.".format(tag))
        return indexes

    def get_specific_columns(self, column_headers):
        """
        Filters the CSV and returns only the columns specified
        in column_headers (in the oreder they appear in that passed
        list).

        SIG: String -> List[List[String]]

        ARGS:
        --------------------------
         - column_headers: the header values of the columns
                           you want returned.
        """
        indexes = self.get_column_indexes(column_headers)
        print("indexes are {}".format(indexes))
        filtered_csv = []
        for full_row in self.file_content:
            filter_row = []
            for index in indexes:
                filter_row.append(full_row[index])
            filtered_csv.append(filter_row)
        return filtered_csv

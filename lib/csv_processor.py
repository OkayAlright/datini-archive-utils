"""
csv_writer_util.py

DESCRIPTION:
    A set of utility functions to operate on csvs-as-lists.

TO USE:
    FILL THIS IN ~~~~

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/3/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""

def filter_by_exact_value(csv, column, value_to_find):
    """
    Filters a given CSV by an exact value match in an exact
    column.

    SIG: (List[List[Any]], Any, Any) -> List[List[Any]] V None

    ARG:
    --------------------------
     - csv: the CSV you want to filter
     - column: the value of the header you want to search under
     - value_to_find: the value which will be used to make EXACT matches
    """
    try:
        index = csv[0].index(column)
    except ValueError:
        print("[ERROR]: Column value {} does not exists".format(column))
        return None
    return list(filter((lambda x: x[index] == value_to_find), csv[1::]))

def filter_by_contained_value(csv, column, value_to_find):
    """
    Filters a given CSV by an contained value match in an exact
    column.

    SIG: (List[List[Any]], Any, Any) -> List[List[Any]] V None

    ARG:
    --------------------------
     - csv: the CSV you want to filter
     - column: the value of the header you want to search under
     - value_to_find: the value which will be used to make CONTAINED matches
    """
    try:
        index = csv[0].index(column)
    except ValueError:
        print("[ERROR]: Column value {} does not exists".format(column))
        return None
    return list(filter((lambda x: value_to_find in x[index]), csv[1::]))

def count_contained_occurence(csv, column, value_to_find):
    """
    Finds the amount of occerunces of a given value in a
    given column.

    SIG: (List[List[Any]], Any, Any) -> List[List[Any]] V None

    ARG:
    --------------------------
     - csv: the CSV you want to count from
     - column: the value of the header you want to search under
     - value_to_find: the value which will be used to make
                      CONTAINED matches when counting
    """
    return len(filter_by_contained_value(csv, column, value_to_find))

def count_exact_occurence(csv, column, value_to_find):
    """
    Finds the amount of occerunces of a given value in a
    given column.

    SIG: (List[List[Any]], Any, Any) -> List[List[Any]] V None

    ARG:
    --------------------------
     - csv: the CSV you want to count from
     - column: the value of the header you want to search under
     - value_to_find: the value which will be used to make
                      EXACT matches when counting
    """
    return len(filter_by_exact_value(csv, column, value_to_find))

def batch_filter_by_exact_value(csv, column_value_tuple):
    """
    Filters and combines multiple EXACT filters of a single
    CSV.

    SIG (List[List[Any]], List[Tuple(Any, Any)] ) -> List[List[Any]]

    ARGS:
    ---------------------------
     - csv: the csv to search from.
     - column_value_tuple: a list of tuples with the fist item being a
                           value for the column to search under and the
                           second being the value to search for
    """
    aggregate = []
    for tup in column_value_tuple:
        part = filter_by_exact_value(csv, tup[0], tup[1])
        aggregate = aggregate + part
    return aggregate

def batch_filter_by_contained_value(csv, column_value_tuple):
    """
    Filters and combines multiple CONTAINED filters of a single
    CSV.

    SIG (List[List[Any]], List[Tuple(Any, Any)] ) -> List[List[Any]]

    ARGS:
    ---------------------------
     - csv: the csv to search from.
     - column_value_tuple: a list of tuples with the fist item being a
                           value for the column to search under and the
                           second being the value to search for
    """
    aggregate = []
    for tup in column_value_tuple:
        part = filter_by_contained_value(csv, tup[0], tup[1])
        aggregate = aggregate + part
    return aggregate

def filter_by_predicate_function(csv, function):
    """
    Filters a CSV based on a pass predicate function
    pointer.

    ARGS:
    -----------------------------
     - csv: the CSV you want to search
     - function: a function to use to filter
                 the CSV. The function must return
                 either True of False in any given
                 execution.
    """
    return list(filter(function, csv))

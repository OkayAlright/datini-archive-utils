"""
csv_writer_util.py

DESCRIPTION:
    A wrapper and some logic around python's csv
    library to write out csv files in various formats.

TO USE:
    FILL THIS IN ~~~~

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/3/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""
import csv

class csv_writer_util(object):
    """
    A container objec that wraps some useful functions
    to write a csv files to disk.
    """

    def csv_write_out(self, outputname, content):
        """
        Writes a file to disk as csv.

        SIG:(String,List[List[String]]) -> None

        ARGS:
        -----------------------------
         - outputname: the name the written csv will be given
         - content: the csv file to write
        """
        output_file = open(outputname, "w")
        writer = csv.writer(output_file)
        writer.writerows(content)
        output_file.close()

    def writeout_as_json_organized_by_id(self, output_name, content):
        """
        Writes a csv to disk as a JSON file.
        Each entry is hashed by it's ID column as
        formatted in the Datini archive csv.

        SIG:(String,List[List[String]]) -> None

        ARGS:
        -----------------------------
         - output_name: the name the written csv will be given
         - content: the csv file to write

         TODO:
           - make a better method for getting the id column
           - make more flexible to hash by any column ID
        """
        json_output = "{\n"
        header = content[0]
        body = content[1::]
        for row in content:
            json_output = json_output + "\t'" + row[0] + "': { \n"
            for i in range(1, len(row)):
                json_output = json_output + "\t\t'" + header[i] + "': '"+row[i] + "',\n"
            json_output = json_output[:-2:] + "},\n"
        json_output = json_output + "}"

        output_file = open(output_name, "w")
        output_file.write(json_output)
        output_file.close()




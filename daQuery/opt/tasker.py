"""
tasker.py

DESCRIPTION:
    A task handler to deal with the distributed job
    system used by daQuery.

    Do not directly use this file.

TO USE:
    DO NOT USE THIS DIRECTLY.

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/13/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""
import json
import argparse
import lib.csv_processor as processor
import lib.csv_reader_util as reader 
import lib.csv_writer_util as writer 

class tasker(object):
    """
    The task handler with an isolated language environment.
    """

    def __init__(self):
        self.writer = writer.csv_writer_util()
        self.reader = reader.csv_reader_util()
        self.parser = argparse.ArgumentParser(
            description="Tasker agent. Please don't attempt to directly use this.")
        self.parser.add_argument('--job', help='The content of the job to do.')

        self.job = json.loads(self.parser.parse_args().job)

        self.env = {
            "get-header": self.get_header,
            "get-body": self.get_body,
            "load": self.load_csv,
            "get-specific-column-by-header": self.get_specific_column,
            "write-out": self.write_out_as_csv,
            "write-out-as-json": self.write_json,
            "exact-filter": self.filter_exact,
            "contained-filter": self.filter_contained,
            "count-exact": self.count_exact,
            "count-contained": self.count_contained,
            "batch-filter-exact": self.batch_filter_exact,
            "batch-filter-contained": self.batch_filter_contained,
            "quit": self.quit_prompt
        }

        self.read_job() # do the job
        

    def eval_statement(self, line):
        """
        Evaluates a single statement. 

        SIG: List[String] -> None

        ARGS:
        ----------------------------
         - line a single line of daQuery code.
        """
        if line[0] in self.env:
            self.env[line[0]](line[1::])
        elif line[1] == "=":
            self.assign_to_env(line)
        else:
            print("ERROR: Undefined function {}".format(line[0]))
            quit()

    def eval_sub_statement(self, line):
        """
        Evaluates a single statement and 
        returns the result. This is used for
        assignments. 

        SIG: List[String] -> Any

        ARGS:
        ----------------------------
         - line a single line of daQuery code.
        """
        if line[0] in self.env:
            return self.env[line[0]](line[1::])
        else:
            print("ERROR: Undefined function {}".format(line[0]))
            quit()


    def assign_to_env(self, line):
        """
        Evaluates a single assignment statement.

        SIG: List[String] -> None

        ARGS:
        ----------------------------
         - line a single line of daQuery code.
        """
        tag = line[0]
        value = line[2::]
        self.env[tag] = self.eval_sub_statement(value)

    def get_var(self, tag):
        """
        Gets a variable value from self.env.

        Sig: String -> Any

        ARGS:
        -----------------------------
         - tag: a string that corresponds to some env variable.
        """
        if not tag in self.env:
            print("ERROR: value {} is not defined yet".format(tag))
        elif callable(self.env[tag]):
            print("ERROR: tried to access callable {} was a value".format(tag))
        else:
            return self.env[tag]

    def read_job(self):
        """
        Reads though a loaded job.
        """
        for jobname in self.job:
            for line in self.job[jobname]:
                self.eval_statement(line)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~FUNCTION WRAPPERS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    """
    ~~~ NOTE ~~~
    So all following definitions are the same kind of wrapper for 
    lib function calls. pointers to these are in self.env 

    Most just check arity, but some format arguements.

    The only arguements is "args" which is the arguement section
    of a statement.
    """

    def quit_prompt(self, args):
        quit()

    def batch_filter_exact(self, args):
        tuples = []
        if len(args[1::])%2 != 0:
            print("ERROR: passed key:value list to batch filter is odd, therefore pairs cannot be constructed")
            quit()
        for i in range(0, len(args[1::]), 2):
            tuples.append(args[i+1], args[i+2])
        return processor.batch_filter_by_exact_value(self.get_var(args[0]), tuples)

    def batch_filter_contained(self, args):
        tuples = []
        if len(args[1::])%2 != 0:
            print("ERROR: passed key:value list to batch filter is odd, therefore pairs cannot be constructed")
            quit()
        for i in range(0, len(args[1::]), 2):
            tuples.append(args[i+1], args[i+2])
        return processor.batch_filter_by_contained_value(self.get_var(args[0]), tuples)

    def count_contained(self, args):
        if len(args) == 3:
            return processor.count_contained_occurence(self.get_var(args[0]), args[1], args[2])
        else:
            print("ERROR: count-contained takes three arguements.")
            quit()

    def count_exact(self, args):
        if len(args) == 3:
            return processor.count_exact_occurence(self.get_var(args[0]), args[1], args[2])
        else:
            print("ERROR: count-exact takes three arguements.")
            quit()

    def write_json(self, args):
        if len(args) == 2:
            self.writer.writeout_as_json_organized_by_id(args[0], self.get_var(args[1]))
        else:
            print("ERROR: write-csv-as-json takes two arguements.")
            quit()

    def get_header(self, args):
        if len(args) == 0:
            return self.reader.get_csv_header()
        else:
            print("ERROR: get_header takes no args")
            quit()

    def get_body(self, args):
        if len(args) == 0:
            return self.reader.get_csv_body()
        else:
            print("ERROR: get_body takes no args")
            quit()

    def load_csv(self, args):
        if len(args) == 1:
            self.reader.load_csv(args[0])
            return self.reader.file_content
        else:
            print("ERROR: load takes one arguement.")
            quit()

    def get_specific_column(self, args):
        return self.reader.get_specific_columns(args)

    def write_out_as_csv(self, args):
        if len(args) == 2:
            self.writer.csv_write_out(args[0], self.get_var(args[1]))
        else:
            print("ERROR: write-out takes two arguements.")
            quit()

    def filter_exact(self, args):
        if len(args) == 3:
            return processor.filter_by_exact_value(self.get_var(args[0]), \
                                                   args[1], \
                                                   args[2])
        else:
            print("ERROR: filter-exact takes three arguements.")
            quit()

    def filter_contained(self, args):
        if len(args) == 3:
            return processor.filter_by_contained_value(self.get_var(args[0]), \
                                                       args[1], \
                                                       args[2])
        else:
            print("ERROR: filter-contained takes three arguements.")
            quit()

t = tasker()
print("Job {} is done".format(list(t.job.keys())[0]))


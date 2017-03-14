"""
master_controller.py 

DESCRIPTION:
    Deals with parsing, constructing, and cordinating
    taskers and their jobs.

TO USE:
    Instance with some mode tag and a job file
    to read from.

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/13/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""
import subprocess
import json

class master_controller(object):
    """
    The master controller of taskers. 

    ARGS:
    -----------------------------
     - mode: either "i" or "e" for interactive or execute respectively.
     - source_file: the job file to read in.
    """
    def __init__(self, mode, source_file):
        self.mode = mode
        self.source_file = source_file
        self.job_que = []
        self.parser_lexer = lex_and_parse()

    def spawn_agent(self, tokens):
        """
        Spawns off a tasker to run a job.

        Sig: List[String] -> None

        ARGS:
        ---------------------------------
         - tokens: a job's ast/token stream
        """
        command = "{\""+tokens[0][0].replace("{","")+"\":"+str(tokens[2::]).replace("'","\"")+"}"
        return subprocess.Popen(["python", "opt/tasker.py", "--job",command])

    def run(self):
        """
        Runs the qued jobs.
        Only call after self.set_que
        """
        for stage in self.job_que:
            procs = list(map(self.spawn_agent, stage))
            while True:
                if len(list(map((lambda x: x.poll == 0), procs))) == len(stage):
                    break
                if sum(procs) != 0:
                    print("ERROR: some tasker finished with a non zero exit-code.")
                    break

    def distribute_jobs(self):
        """
        Handles staging and wraps tasker spawning
        """
        for stage in self.job_que:
            for job in stage:
                map(self.run, job)

    def set_que(self):
        """
        Seperates job token streams into
        ranked stages.
        """
        self.parser_lexer.tokenize_and_parse(self.source_file)
        raw_que = self.parser_lexer.ast
        max_stage = self.find_last_stage(raw_que)
        for i in range(1, max_stage+1):
            self.job_que.append(list(filter((lambda x: int(x[1][1]) == i), raw_que)))

    def find_last_stage(self, que):
        """
        Finds the latest stage in a job file token stream. 

        Sig: List[List[String]] -> Int

        ARGS:
        -----------------------------------
        Que: an unstructed job token stream.
        """
        max_stage = 0
        for job in que:
            if int(job[1][1]) > max_stage:
                max_stage = int(job[1][1])
        return max_stage


class lex_and_parse(object):
    """
    lexes and parses a jobs file into a 
    token stream.
    """
    def __init__(self):
        self.ast = []

    def break_up_job(self, source):
        """
        Seperates jobs.

        Sig: String -> List[String]

        ARGS:
        -------------------------------
         - source: the job file to parse as a string
        """
        return source.split("}")

    def break_up_statements(self, source):
        """
        Seperates each job's statements. 

        Sig: String -> List[List[String]]

        ARGS:
        -------------------------------
         - source: the job file to parse as a string
        """
        jobs = self.break_up_job(source)
        tmp_results = []
        final_results = []
        for job in jobs:
            tmp_results.append(list(filter((lambda x: x != ''), job.split("\n"))))
            final_results.append([])
            for line in tmp_results[-1]:
                final_results[-1].append(list(filter((lambda x: x != ''), line.split())))

        return list(filter((lambda x: x != []), final_results))

    def tokenize_and_parse(self, source_file):
        """
        Opens a file and parses it. Assigns it to self.ast

        Sig: String -> None

        ARGS:
        -------------------------------
         - source_file: a relative path to the file you
                        want to parse
        """
        source_code = open(source_file, "r")
        source_code_as_string = source_code.read()
        self.ast = self.break_up_statements(source_code_as_string)




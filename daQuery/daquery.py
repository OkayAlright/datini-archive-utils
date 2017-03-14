"""
daquery.py 

DESCRIPTION:
    runs a daquery jobs file

TO USE:
    Pass some --mode flag (either "i" or "e") and
    the path to some job file (--job some-example).

CREDITS:
   - Logan Davis <ldavis@marlboro.edu>

Init date: 3/13/17 | Version: Python 3.6 | DevOS: MacOS 10.11 & <add here>
"""
import argparse
import opt.master_controller as daController

parser = argparse.ArgumentParser(description="The DaQuery DSL executer.")
parser.add_argument('--file', help='A path the the job you want to run')
parser.add_argument('--mode', help='either "i" for interactive or "e" for execute (Note: this option is currently ignored).')

controller = daController.master_controller(parser.parse_args().mode, parser.parse_args().file)
controller.set_que()
controller.run()
print("STATUS: Finished.")

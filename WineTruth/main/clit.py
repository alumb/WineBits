"""
Command-Line Interactive Tool

"""

from optparse import OptionParser
from subprocess import call

parser = OptionParser()
parser.add_option("-s", "--start", action="store_true", dest="start",
                  help="Thrusters engage!")
parser.add_option("-t", "--test", action="store_true", dest="test",
                  help="Test everything!")
parser.add_option("-p", "--pep", action="store_true", dest="pep",
                  help="PIP8 everything!")

(options, args) = parser.parse_args()

if options.start:
    call("~/google_appengine/dev_appserver.py . --host=0.0.0.0 " +
         "", shell=True)
elif options.test:
    call("python `which nosetests`", shell=True)
elif options.pep:
    call("pep8", shell=True)
else:
    parser.print_help()

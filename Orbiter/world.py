import os
import sys

sys.path.append (os.path.abspath ('../..')) # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable

from SimPyLC import *
from orbiter import *
from timing import *


World (orbiter ()) #, Timing ())

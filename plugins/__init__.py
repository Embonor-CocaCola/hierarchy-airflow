import os
import sys

# insert vendor directory into syspath
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../include/expos_pdv/db/vendor'))

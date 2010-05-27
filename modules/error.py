import os
import sys
from stdout import red

def fail(s):
    """
    failure call

    @arg s      string

    @return     exit
    """
    print red('ERR')+': ' + s
    sys.exit(2)

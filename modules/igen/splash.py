import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class splash:

    def __init__(self):
        """
        init class variable
        """
        pass

    def build(self):
        """
        splash build sequence

        @return     bool
        """
        pass

    def fail(self, step):
        """
        @arg step   string

        @return     exit
        """
        print red('error')+': initramfs.luks.'+step+'() failed'
        sys.exit(2)


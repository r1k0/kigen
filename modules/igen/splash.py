import os
import sys
from stdout import green, turquoise, white, red, yellow
import utils

class splash:

    def __init__(self,  \
                master_config,  \
                theme,          \
                sres,           \
                sinitrd,        \
                temp,           \
                verbose):
        """
        init class variable
        """

        self.master_config  = master_config
        self.theme          = theme
        self.sres           = sres
        self.sinitrd        = sinitrd
        self.temp           = temp
        self.verbose        = verbose

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
        print red('error')+': initramfs.splash.'+step+'() failed'
        sys.exit(2)


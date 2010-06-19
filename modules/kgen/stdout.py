import os
import sys
color = os.getenv("KGEN_STDOUT")
if color == '0':
    from portage.output import green, turquoise, white, red, yellow
else:
    from nocolor import green, turquoise, white, red, yellow

import os
import sys
color = os.getenv("GENKI_STD_COLOR")
if color == '0':
	from portage.output import green, turquoise, white, red, yellow
else:
	from nocolor import green, turquoise, white, red, yellow


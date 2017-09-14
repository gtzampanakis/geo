import os
import sys

BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, 'lib')

sys.path.insert(0, LIB_DIR)

import gui

gui.main()

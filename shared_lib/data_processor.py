import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSOR_LIB_DIR = os.path.join(BASE_DIR, 'data_processor')

sys.path.append(DATA_PROCESSOR_LIB_DIR)

import lib

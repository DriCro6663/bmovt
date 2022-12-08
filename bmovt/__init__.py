import sys
from pathlib import Path
current_dir = str(Path().resolve())
parent_dir = str(Path().resolve().parent)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from libs import *
from .libs import *
from bmovt.bmovt import *

__version__ = "0.0.1"
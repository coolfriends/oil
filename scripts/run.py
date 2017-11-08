import sys
import os
import inspect
import json

try:
    from oil import Oil
except ImportError: # If module not installed with pip
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    from oil import Oil

oil = Oil()
print(json.dumps(oil.scan(), indent=4))

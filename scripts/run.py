import sys
import os
import json

from pathlib import Path

try:
    from oil import Oil
except ImportError: # If module not installed with pip
    oil_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, oil_path)
    from oil import Oil

oil = Oil()
print(json.dumps(oil.scan(), indent=2))

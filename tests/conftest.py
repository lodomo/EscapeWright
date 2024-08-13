# tests/conftest.py
import sys
from pathlib import Path

# Set the path to the root of the project so that 'escapewright' can be found
sys.path.append(str(Path(__file__).parent.parent))

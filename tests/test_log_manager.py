# Add escapewright to path
import sys

import pytest

from escapewright import LogManager

# Add 'escapewright' to path back one folder.
sys.path.append("..")


def test_creation():
    log_manager = LogManager()
    assert log_manager is not None


if __name__ == "__main__":
    pytest.main(["-v", __file__])

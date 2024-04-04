# Add escapewright to path
import os
import sys

import pytest

from escapewright import LogManager

# Add 'escapewright' to path back one folder.
sys.path.append("..")


def test_creation():
    log_manager = LogManager(auto_refresh=False)
    assert log_manager is not None
    # Assert there's a file at the path ~/EWLogs/YYYY/YYYY-MM-DD.log
    assert os.path.exists(log_manager.log_file_path)

    log_manager.override_log_file("test.log")
    assert os.path.exists(log_manager.log_file_path)

    log_manager.override_log_file("test2.log")
    assert os.path.exists(log_manager.log_file_path)


if __name__ == "__main__":
    pytest.main(["-v", __file__])

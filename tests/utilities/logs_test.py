"""Test to check if log file is correctly initialized."""

import os
import pathlib
import shutil
from sources.utilities import logs


def test_init_logger():
    """Test init_file function."""
    assert logs.init_logger()
    logs_dir = pathlib.Path(os.path.abspath(os.getenv("LOGS_DIR", "logs")))
    assert os.path.exists(logs_dir)
    assert logs_dir.is_dir()


def test_init_logger_with_path_no_dir_create_dir():
    """Test init_file function."""
    assert logs.init_logger("logs/test-dir")
    logs_dir = pathlib.Path("logs/test-dir")
    assert os.path.exists(logs_dir)
    assert logs_dir.is_dir()
    shutil.rmtree(logs_dir)


def test_get_logger():
    """Test get_logger function."""
    assert logs.get_logger()

"""
Test to check if log file is correctly initialized
"""
import os
import pathlib
from utilities import logs

def test_init_logger():
    """Test init_file function"""
    assert logs.init_logger()
    logs_dir = pathlib.Path(os.path.abspath(os.getenv("LOGS_DIR", "logs")))
    assert os.path.exists(logs_dir)
    assert logs_dir.is_dir()

def test_get_logger():
    """Test get_logger function"""
    assert logs.get_logger()
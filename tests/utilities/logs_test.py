"""
Test to check if log file is correctly initialized
"""
from utilities import logs

def test_init_logger():
    """Test init_file function"""
    assert logs.init_logger()

def test_get_logger():
    """Test get_logger function"""
    assert logs.get_logger()
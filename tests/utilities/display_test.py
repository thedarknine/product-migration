"""
Test to check display utilities
"""
from utilities import display
from datetime import datetime

def test_colors():
    """Test colors"""
    assert display.colors('green')
    assert display.colors('white')
    assert display.colors('red')
    assert display.colors('cyan')
    assert display.colors('grey')
    assert display.colors('yellow')
    assert display.colors('')

def test_info():
    """Test info"""
    display.info("Test info")

def test_alert():
    """Test alert"""
    display.alert("Test alert")

def test_title():
    """Test title"""
    display.title("Test title")

def test_clear_screen():
    """Test clear screen"""
    display.clear_screen()

def test_start_info():
    """Test start info"""
    display.start_info(datetime.now(), "Test start info")

def test_end_info():
    """Test end info"""
    display.end_info(datetime.now())

def test_deinit():
    """Test deinit"""
    display.deinit()
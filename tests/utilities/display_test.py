"""
Test to check display utilities
"""

import arrow
from sources.utilities import display


def test_info():
    """Test info"""
    display.info("Test info")


def test_alert():
    """Test alert"""
    display.alert("Test alert")


def test_title():
    """Test title"""
    display.title("Test title")


def test_items_list():
    """Test items list"""
    display.items_list(["Test item 1", "Test item 2", "Test item 3"])
    display.items_list([])
    display.items_list(None)
    display.items_list("")
    display.items_list(1)


def test_clear_screen():
    """Test clear screen"""
    display.clear_screen()


def test_start_info():
    """Test start info"""
    display.start_info(arrow.now(), "Test start info")


def test_end_info():
    """Test end info"""
    display.end_info(arrow.now())

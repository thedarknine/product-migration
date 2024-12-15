"""
Test to check files utility
"""

from sources.utilities import files


def test_get_content():
    """Test the get_content method"""
    assert files.get_content("openproject_projects.json", "tests/samples")


def test_get_content_file_not_found_return_none():
    """Test the get_content method"""
    assert not files.get_content("not_found.json", "tests/samples")

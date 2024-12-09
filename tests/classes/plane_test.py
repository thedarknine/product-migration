"""
Tests for the plane module
"""
import os
import logging
from classes import plane

def test__init__():
    """Test the __init__ method"""
    client = plane.Client()
    assert client.base_url == os.getenv("PLANE_URL")
    assert client.path == ""
    assert client.headers == { 'X-API-Key': os.getenv("PLANE_API_KEY") }
    assert client.get_endpoint() == os.getenv("PLANE_URL")

def test_get_endpoint():
    """Test the get_endpoint method"""
    client = plane.Client()
    assert client.get_endpoint() == os.getenv("PLANE_URL")

def test_get_projects_return_list(httpx_mock):
    """Test the get_projects method"""
    httpx_mock.add_response(200, json={"results": []})
    client = plane.Client()
    result = client.get_projects()
    assert result == []
    assert isinstance(result, list)

def test_get_projects_write_logging(httpx_mock, caplog):
    """Test the get_projects method"""
    httpx_mock.add_response(200, json={"results": []})
    client = plane.Client()
    with caplog.at_level(logging.INFO):
        client.get_projects()
        assert "Attempting to get projects from Plane" in caplog.text

def test_get_users_return_list(httpx_mock):
    """Test the get_users method"""
    httpx_mock.add_response(200, json={"results": []})
    client = plane.Client()
    result = client.get_users()
    assert not result # result == []
    assert isinstance(result, list)

def test_get_users_write_logging(httpx_mock, caplog):
    """Test the get_users method"""
    httpx_mock.add_response(200, json={"results": []})
    client = plane.Client()
    with caplog.at_level(logging.INFO):
        client.get_users()
        assert "Attempting to get users from Plane" in caplog.text

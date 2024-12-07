"""
Tests for the api module
"""
from classes import api

def test__init__():
    """Test the __init__ method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    assert client.base_url == "https://api.example.com"
    assert client.path == "path"
    assert client.headers == {"X-API-Key": "secret"}
    assert client.get_endpoint() == "https://api.example.com/path"

def test_get_endpoint():
    """Test the get_endpoint method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    assert client.get_endpoint() == "https://api.example.com/path"

    client.set_endpoint("path2")
    assert client.get_endpoint() == "https://api.example.com/path2"

    client.set_endpoint("")
    assert client.get_endpoint() == "https://api.example.com"

    client.set_endpoint(None)
    assert client.get_endpoint() == "https://api.example.com"

def test_set_endpoint():
    """Test the set_endpoint method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    client.set_endpoint("path2")
    assert client.get_endpoint() == "https://api.example.com/path2"

    client.set_endpoint("")
    assert client.get_endpoint() == "https://api.example.com"

    client.set_endpoint(None)
    assert client.get_endpoint() == "https://api.example.com"

    client.set_endpoint("path3")
    assert client.get_endpoint() == "https://api.example.com/path3"

def test_get():
    """Test the get method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    assert client.get() is None
    assert client.get({"param": "value"}) is None

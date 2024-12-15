"""
Tests for the api module
"""

import os
import pytest
from sources.classes import api
from sources.utilities import logs

logger = logs.get_logger()


def test__init__():
    """Test the __init__ method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    assert client.base_url == "https://api.example.com"
    assert client.path == "path"
    assert client.headers == {"X-API-Key": "secret"}
    assert client.get_endpoint() == "https://api.example.com/path"

    with pytest.raises(ValueError):
        api.Client(None, "path", {"X-API-Key": "secret"})

    with pytest.raises(ValueError):
        api.Client(None)


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


def test_get(caplog):
    """Test the get method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    assert client.get() is None
    assert client.get({"param": "value"}) is None
    assert (
        caplog.records[0].message
        == "An error occurred: [Errno -2] Name or service not known"
    )


def test_get_success(httpx_mock):
    """Test the get method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    httpx_mock.add_response(
        method="GET",
        url=client.get_endpoint(),
        match_headers=client.headers,
        status_code=200,
        json=[],
    )
    result = client.get()
    assert result == []


def test_get_error(httpx_mock, caplog):
    """Test the get method"""
    client = api.Client("https://api.example.com", "path")

    httpx_mock.add_response(401, json={"error": "Unauthorized"})
    assert client.get() is None
    error_message = (
        "Client error '401 Unauthorized' for url 'https://api.example.com/path'"
    )
    assert error_message in caplog.records[0].message

    httpx_mock.add_response(403, json={"error": "Forbidden"})
    assert client.get() is None

    httpx_mock.add_response(404, json={"error": "Not Found"})
    assert client.get() is None

    httpx_mock.add_response(500, json={"error": "Internal Server Error"})
    assert client.get() is None


def test_get_all_projects(httpx_mock):
    """Test the get_all method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    response = client.get_all(os.getenv("OPENPROJECT_PATH_PROJECTS"))
    assert isinstance(response, dict)
    assert len(response) == 1


def test_get_all_users(httpx_mock):
    """Test the get_all method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    response = client.get_all(os.getenv("OPENPROJECT_PATH_USERS"))
    assert isinstance(response, dict)
    assert len(response) == 1


def test_get_all_projects_with_replace(httpx_mock):
    """Test the get_all method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    response = client.get_all(
        os.getenv("OPENPROJECT_PATH_PROJECTS"), "{PROJECT_ID}", "1"
    )
    assert isinstance(response, dict)
    assert len(response) == 1


def test_get_all_tasks_with_replace(httpx_mock):
    """Test the get_all method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    response = client.get_all(os.getenv("OPENPROJECT_PATH_TASKS"), "{PROJECT_ID}", "1")
    assert isinstance(response, dict)
    assert len(response) == 1


def test_get_all_no_endpoint_returns_empty_list():
    """Test the get_all method"""
    client = api.Client("https://api.example.com", "path", {"X-API-Key": "secret"})
    response = client.get_all(None)
    assert response is None

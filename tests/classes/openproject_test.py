"""
Tests for the openproject module
"""

import os
import logging
from classes import openproject


def test__init__():
    """Test the __init__ method"""
    client = openproject.Client()
    assert client.base_url == os.getenv("OPENPROJECT_URL")
    assert client.path == ""
    assert client.headers == {"Authorization": os.getenv("OPENPROJECT_API_AUTH")}
    assert client.get_endpoint() == os.getenv("OPENPROJECT_URL")


def test_get_endpoint():
    """Test the get_endpoint method"""
    client = openproject.Client()
    assert client.get_endpoint() == os.getenv("OPENPROJECT_URL")


def test_get_projects_return_list(httpx_mock):
    """Test the get_projects method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    response = client.get_projects()
    assert response == []
    assert isinstance(response, list)


def test_get_two_projects_return_two_elements():
    """Test the get_projects method"""
    client = openproject.Client()
    response = client.get_projects()
    # Return only result into elements subarray
    assert "_embedded" not in response
    assert "elements" not in response
    assert isinstance(response, list)
    assert len(response) == 2


def test_get_projects_write_logging(httpx_mock, caplog):
    """Test the get_projects method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    with caplog.at_level(logging.INFO):
        client.get_projects()
        assert "Attempting to get projects from OpenProject" in caplog.text


def test_get_users_return_list(httpx_mock):
    """Test the get_users method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    response = client.get_users()
    assert not response
    assert isinstance(response, list)


def test_get_two_users_return_two_elements():
    """Test the get_users method"""
    client = openproject.Client()
    response = client.get_users()
    # Return only result into elements subarray
    assert "_embedded" not in response
    assert "elements" not in response
    assert isinstance(response, list)
    assert len(response) == 2


def test_get_users_write_logging(httpx_mock, caplog):
    """Test the get_users method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    with caplog.at_level(logging.INFO):
        client.get_users()
        assert "Attempting to get users from OpenProject" in caplog.text


def test_get_tasks_return_list(httpx_mock):
    """Test the get_tasks method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    response = client.get_tasks()
    assert not response
    assert isinstance(response, list)


def test_get_four_tasks_return_four_elements():
    """Test the get_tasks method"""
    client = openproject.Client()
    response = client.get_tasks()
    # Return only result into elements subarray
    assert "_embedded" not in response
    assert "elements" not in response
    assert isinstance(response, list)
    assert len(response) == 4


def test_get_tasks_write_logging(httpx_mock, caplog):
    """Test the get_tasks method"""
    httpx_mock.add_response(200, json={"_embedded": {"elements": []}})
    client = openproject.Client()
    with caplog.at_level(logging.INFO):
        client.get_tasks()
        assert "Attempting to get tasks from OpenProject" in caplog.text

"""Tests for the openproject module."""

import os
import logging
import json
from sources.classes import openproject
from sources.utilities import files

# Get JSON results
json_projects_data = json.loads(
    files.get_content("openproject_projects.json", "tests/samples")
)
json_users_data = json.loads(
    files.get_content("openproject_users.json", "tests/samples")
)
json_tasks_data = json.loads(
    files.get_content("openproject_workpackages.json", "tests/samples")
)


def test__init__():
    """Test the __init__ method."""
    client = openproject.Client()
    assert client.base_url == os.getenv("OPENPROJECT_URL")
    assert client.path == ""
    assert client.headers == {"Authorization": os.getenv("OPENPROJECT_API_AUTH")}
    assert client.get_endpoint() == os.getenv("OPENPROJECT_URL")


def test_get_endpoint():
    """Test the get_endpoint method."""
    client = openproject.Client()
    assert client.get_endpoint() == os.getenv("OPENPROJECT_URL")


def test_get_total():
    """Test the get_total method."""
    client = openproject.Client()
    assert client.get_total(json_projects_data) == 2


def test_get_all_projects(httpx_mock):
    """Test the get_all_projects method.

    Args:
        httpx_mock: pytest fixture to mock httpx
    """
    httpx_mock.add_response(200, json=json_projects_data)
    client = openproject.Client()
    response = client.get_all_projects()
    assert isinstance(response, list)
    assert len(response) == 2


def test_compute_projects_return_list():
    """Test the compute_projects method."""
    client = openproject.Client()
    result = client.compute_projects(json_projects_data)
    assert "_embedded" not in result
    assert "elements" not in result
    assert result == json_projects_data["_embedded"]["elements"]
    assert isinstance(result, list)


def test_compute_projects_write_logging(caplog):
    """Test the compute_projects method.

    Args:
        caplog: pytest fixture to capture logs
    """
    client = openproject.Client()
    with caplog.at_level(logging.INFO):
        client.compute_projects(json_projects_data)
        assert "Compute projects from OpenProject" in caplog.text


def test_compute_projects_two_elements_return_two():
    """Test the compute_projects method."""
    client = openproject.Client()
    result = client.compute_projects(json_projects_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert len(result) == len(json_projects_data["_embedded"]["elements"])


def test_get_all_users(httpx_mock):
    """Test the get_all_users method.

    Args:
        httpx_mock: pytest fixture to mock httpx
    """
    httpx_mock.add_response(200, json=json_users_data)
    client = openproject.Client()
    response = client.get_all_users()
    assert isinstance(response, list)
    assert len(response) == 2


def test_compute_users_return_list():
    """Test the compute_users method."""
    client = openproject.Client()
    result = client.compute_users(json_users_data)
    assert "_embedded" not in result
    assert "elements" not in result
    assert result == json_users_data["_embedded"]["elements"]
    assert isinstance(result, list)


def test_compute_users_write_logging(caplog):
    """Test the compute_users method.

    Args:
        caplog: pytest fixture to capture logs
    """
    client = openproject.Client()
    with caplog.at_level(logging.INFO):
        client.compute_users(json_users_data)
        assert "Compute users from OpenProject" in caplog.text


def test_compute_users_two_elements_return_two():
    """Test the compute_users method."""
    client = openproject.Client()
    result = client.compute_users(json_users_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert len(result) == len(json_users_data["_embedded"]["elements"])


def test_get_all_tasks_by_project(httpx_mock):
    """Test the get_all_tasks_by_project method.

    Args:
        httpx_mock: pytest fixture to mock httpx
    """
    httpx_mock.add_response(200, json=json_tasks_data)
    client = openproject.Client()
    response = client.get_all_tasks_by_project("project_id")
    assert isinstance(response, list)
    assert len(response) == 2

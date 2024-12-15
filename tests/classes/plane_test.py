"""Tests for the plane module."""

import os
import logging
import json
from sources.classes import plane
from sources.utilities import files

# Get JSON results
json_projects_data = json.loads(
    files.get_content("plane_projects.json", "tests/samples")
)
json_users_data = json.loads(files.get_content("plane_members.json", "tests/samples"))
json_tasks_data = json.loads(files.get_content("plane_issues.json", "tests/samples"))


def test__init__():
    """Test the __init__ method."""
    client = plane.Client()
    assert client.base_url == os.getenv("PLANE_URL")
    assert client.path == ""
    assert client.headers == {"X-API-Key": os.getenv("PLANE_API_KEY")}
    assert client.get_endpoint() == os.getenv("PLANE_URL")


def test_get_endpoint():
    """Test the get_endpoint method."""
    client = plane.Client()
    assert client.get_endpoint() == os.getenv("PLANE_URL")


def test_compute_projects_return_list():
    """Test the compute_projects method."""
    client = plane.Client()
    result = client.compute_projects(json_projects_data)
    assert "results" not in result
    assert result == json_projects_data["results"]
    assert isinstance(result, list)


def test_compute_projects_write_logging(caplog):
    """Test the compute_projects method.

    Args:
        caplog: pytest fixture to capture logs
    """
    client = plane.Client()
    with caplog.at_level(logging.INFO):
        client.compute_projects(json_projects_data)
        assert "Compute projects from Plane" in caplog.text


def test_compute_projects_two_elements_return_two():
    """Test the compute_projects method."""
    client = plane.Client()
    result = client.compute_projects(json_projects_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert len(result) == len(json_projects_data["results"])


def test_compute_users_return_list():
    """Test the compute_users method."""
    client = plane.Client()
    result = client.compute_users(json_users_data)
    assert "_embedded" not in result
    assert "elements" not in result
    assert result == json_users_data
    assert isinstance(result, list)


def test_compute_users_write_logging(caplog):
    """Test the compute_users method.

    Args:
        caplog: pytest fixture to capture logs
    """
    client = plane.Client()
    with caplog.at_level(logging.INFO):
        client.compute_users(json_users_data)
        assert "Compute users from Plane" in caplog.text


def test_compute_users_two_elements_return_two():
    """Test the compute_users method."""
    client = plane.Client()
    result = client.compute_users(json_users_data)
    assert isinstance(result, list)
    assert len(result) == 2
    assert len(result) == len(json_users_data)

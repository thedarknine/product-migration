"""Test project model."""

from datetime import datetime, timedelta
from sources.models.project import Project


past_datetime = datetime.now() - timedelta(days=1)
project_test = Project(
    uuid="62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
    external_id=9,
    name="Project 1",
    identifier="test-1",
    created_at=past_datetime,
    updated_at=past_datetime,
)


def test_repr():
    """Test the project model."""
    assert (
        repr(project_test)
        == "<Project(uuid=62492acb-203d-4bdb-82e3-85fbd5cf2cc9, "
        + "external_id=9, name=Project 1, description=None, identifier=test-1, created_at="
        + str(past_datetime)
        + ", updated_at="
        + str(past_datetime)
        + ")>"
    )


def test_from_raw():
    """Test the project model."""
    raw_data = {
        "id": 9,
        "name": "Project 1",
        "identifier": "test-1",
        "createdAt": "2024-12-27T12:00:00.000Z",
        "updatedAt": "2024-12-27T12:00:00.000Z",
    }
    raw_obj = type("Obj", (object,), dict(raw_data))()
    assert isinstance(Project().from_raw(raw_obj), Project)


def test_to_dict():
    """Test the project model."""
    assert isinstance(project_test.to_dict(), dict)
    assert project_test.to_dict()["uuid"] == "62492acb-203d-4bdb-82e3-85fbd5cf2cc9"
    assert project_test.to_dict()["external_id"] == 9
    assert project_test.to_dict()["name"] == "Project 1"
    assert project_test.to_dict()["identifier"] == "test-1"
    assert project_test.to_dict()["created_at"] == past_datetime
    assert project_test.to_dict()["updated_at"] == past_datetime

    assert project_test.to_dict() == {
        "uuid": "62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
        "external_id": 9,
        "name": "Project 1",
        "description": None,
        "identifier": "test-1",
        "created_at": past_datetime,
        "updated_at": past_datetime,
    }

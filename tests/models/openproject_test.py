"""Test the openproject model."""

from datetime import datetime, timedelta
import pytest
from pydantic_core import ValidationError
from sources.models.openproject import Project, User, Task


past_datetime = datetime.now() - timedelta(days=1)
future_datetime = datetime.now() + timedelta(days=1)


def test_project_valid_data():
    """Test the project model."""
    project = Project(
        id=1,
        name="test",
        identifier="test",
        createdAt=past_datetime,
        updatedAt=past_datetime,
    )
    assert isinstance(project, Project)
    assert project.id == 1
    assert project.name == "test"
    assert project.identifier == "test"
    assert project.createdAt == past_datetime
    assert project.updatedAt == past_datetime


def test_project_invalid_dates():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(
            id=1,
            name="test",
            identifier="test",
            createdAt=future_datetime,
            updatedAt=future_datetime,
        )
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"


def test_project_empty_value():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(
            id=1,
            identifier="test",
            createdAt=past_datetime,
            updatedAt=past_datetime,
        )
    assert exc_info.value.errors()[0]["msg"] == "Field required"


def test_user_valid_data():
    """Test the user model."""
    user = User(
        id=1,
        name="test",
        email="test@mail.com",
        createdAt=past_datetime,
        updatedAt=past_datetime,
    )
    assert isinstance(user, User)
    assert user.id == 1
    assert user.name == "test"
    assert user.email == "test@mail.com"
    assert user.createdAt == past_datetime
    assert user.updatedAt == past_datetime


def test_user_invalid_dates():
    """Test the user model."""
    with pytest.raises(ValidationError) as exc_info:
        User(
            id=1,
            name="test",
            email="test@mail.com",
            createdAt=future_datetime,
            updatedAt=future_datetime,
        )
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"


def test_user_invalid_email():
    """Test the user model."""
    with pytest.raises(ValidationError) as exc_info:
        User(
            id=1,
            name="test",
            email="test",
            createdAt=past_datetime,
            updatedAt=past_datetime,
        )
    assert (
        exc_info.value.errors()[0]["msg"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


def test_task_valid_data():
    """Test the task model."""
    task = Task(id=1, name="test", createdAt=past_datetime, updatedAt=past_datetime)
    assert isinstance(task, Task)
    assert task.id == 1
    assert task.name == "test"
    assert task.createdAt == past_datetime
    assert task.updatedAt == past_datetime


def test_task_invalid_dates():
    """Test the task model."""
    with pytest.raises(ValidationError) as exc_info:
        Task(id=1, name="test", createdAt=future_datetime, updatedAt=future_datetime)
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"

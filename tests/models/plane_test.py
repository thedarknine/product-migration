"""Test the plane model."""

from datetime import datetime, timedelta
import pytest
from pydantic_core import ValidationError
from sources.models.plane import Project, User, Task


past_datetime = datetime.now() - timedelta(days=1)
future_datetime = datetime.now() + timedelta(days=1)


def test_project_valid_data():
    """Test the project model."""
    project = Project(
        id="62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
        name="test",
        created_at=past_datetime,
        updated_at=past_datetime,
    )
    assert isinstance(project, Project)
    assert project.id == "62492acb-203d-4bdb-82e3-85fbd5cf2cc9"
    assert project.name == "test"
    assert project.created_at == past_datetime
    assert project.updated_at == past_datetime


def test_project_invalid_id():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(id=18, name="test", created_at=past_datetime, updated_at=past_datetime)
    assert exc_info.value.errors()[0]["msg"] == "Input should be a valid string"


def test_project_invalid_dates():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(
            id="62492acb-203d-4bdb-82e3-85fbd5cf2cc9",
            name="test",
            created_at=future_datetime,
            updated_at=future_datetime,
        )
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"


def test_project_missing_value():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(id="62492acb-203d-4bdb-82e3-85fbd5cf2cc9", name="test")
    assert exc_info.value.errors()[0]["msg"] == "Field required"


def test_project_empty_value():
    """Test the project model."""
    with pytest.raises(ValidationError) as exc_info:
        Project(id="62492acb-203d-4bdb-82e3-85fbd5cf2cc9", name="")
    assert exc_info.value.errors()[0]["msg"] == "Field required"


def test_user_valid_data():
    """Test the user model."""
    user = User(
        id=1,
        name="test",
        email="test@mail.com",
        created_at=past_datetime,
        updated_at=past_datetime,
    )
    assert isinstance(user, User)
    assert user.id == 1
    assert user.name == "test"
    assert user.email == "test@mail.com"
    assert user.created_at == past_datetime
    assert user.updated_at == past_datetime


def test_user_invalid_email():
    """Test the user model."""
    with pytest.raises(ValidationError) as exc_info:
        User(
            id=1,
            name="test",
            email="test",
            created_at=past_datetime,
            updated_at=past_datetime,
        )
    assert (
        exc_info.value.errors()[0]["msg"]
        == "value is not a valid email address: An email address must have an @-sign."
    )


def test_user_invalid_dates():
    """Test the user model."""
    with pytest.raises(ValidationError) as exc_info:
        User(
            id=1,
            name="test",
            email="test@mail.com",
            created_at=future_datetime,
            updated_at=future_datetime,
        )
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"


def test_task_valid_data():
    """Test the task model."""
    task = Task(id=1, name="test", created_at=past_datetime, updated_at=past_datetime)
    assert isinstance(task, Task)
    assert task.id == 1
    assert task.name == "test"
    assert task.created_at == past_datetime
    assert task.updated_at == past_datetime


def test_task_invalid_dates():
    """Test the task model."""
    with pytest.raises(ValidationError) as exc_info:
        Task(id=1, name="test", created_at=future_datetime, updated_at=future_datetime)
    assert exc_info.value.errors()[0]["msg"] == "Input should be in the past"

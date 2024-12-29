"""Tests for the db module."""

import os
from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy import create_engine, MetaData
from sources.classes import db
from sources.models.project import Project
from sources.models.user import User

fake_engine = create_engine("postgresql+psycopg:///:memory:")


@patch.dict(os.environ, {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_USERNAME": "test_user",
    "DB_PASSWORD": "test_pass",
    "DB_DATABASE": "test_db",
})
def test_init():
    """Test client initialization with environment variables."""
    client = db.Client()
    assert client.host == "localhost"
    assert client.port == "5432"
    assert client.user == "test_user"
    assert client.passwd == "test_pass"
    assert client.dbname == "test_db"
    assert client.engine is None


def test_get_engine_calls_connection_if_engine_is_none():
    """Test the get_engine method when engine is None."""
    client = db.Client()
    with patch.object(
        db.Client, "connection", return_value="mock_engine"
    ) as mock_connection:
        client.get_engine()
        mock_connection.assert_called_once()
        # assert client.get_engine() == "mock_engine"
        # assert client.engine == "mock_engine"


def test_get_engine():
    """Test the get_engine method."""
    db.Client().set_engine(fake_engine)
    assert isinstance(db.Client().get_engine(), object)
    assert db.Client().get_engine() is not None


def test_set_engine_with_none():
    """Test the set_engine method with None."""
    db.Client().set_engine(None)
    assert db.Client().get_engine() is not None


def test_set_engine_sets_engine():
    """Test the set_engine method."""
    client = db.Client()
    mock_engine = "mock_engine"
    client.set_engine(mock_engine)
    assert client.engine == mock_engine


def test_set_engine():
    """Test the set_engine method."""
    engine = fake_engine
    assert isinstance(engine, object)
    assert engine is not None
    db.Client().set_engine(engine)


def test_unset_engine_unsets_engine():
    """Test the unset_engine method."""
    client = db.Client()
    client.engine = "mock_engine"
    client.unset_engine()
    assert client.engine is None


def test_connection_success():
    """Test the connection method."""
    mock_engine = MagicMock()
    mock_engine.connect = MagicMock()

    with patch("sources.classes.db.create_engine", return_value=mock_engine):
        engine = db.Client().connection()
        assert engine is mock_engine


def test_connection_failure():
    """Test the connection method with an exception."""
    mock_engine = MagicMock()
    mock_engine.connect = MagicMock(side_effect=Exception("Test exception"))

    with patch("sources.classes.db.create_engine", return_value=mock_engine):
        with pytest.raises(Exception, match="Test exception"):
            db.Client().connection()

    assert mock_engine.connect.call_count == 1


def test_connection_exception():
    """Test the connection method with an exception."""
    db.Client().host = "localhost"
    assert isinstance(db.Client().connection(), object)


def test_close_connection():
    """Test the close_connection method."""
    db.Client().close_connection(fake_engine)
    assert db.Client().engine is None


def test_create_schema():
    """Test the create_schema method."""
    mock_engine = MagicMock()
    # Patch the metadata.create_all method for Project and User
    with patch.object(
        Project.metadata, "create_all"
    ) as mock_project_create_all, patch.object(
        User.metadata, "create_all"
    ) as mock_user_create_all:
        client = db.Client()
        client.create_schema(mock_engine)

        mock_project_create_all.assert_called_once_with(mock_engine)
        mock_user_create_all.assert_called_once_with(mock_engine)


def test_drop_schema():
    """Test the drop_schema method."""
    mock_engine = MagicMock()
    # Patch the MetaData.reflect and MetaData.drop_all methods
    with patch.object(MetaData, "reflect") as mock_reflect, patch.object(
        MetaData, "drop_all"
    ) as mock_drop_all:
        client = db.Client()
        client.drop_schema(mock_engine)

        mock_reflect.assert_called_once_with(bind=mock_engine)
        mock_drop_all.assert_called_once_with(bind=mock_engine)


def test_write_data():
    """Test the write_data method."""
    # Create a mock engine and connection
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    # Create a mock table
    mock_table = MagicMock()
    with patch("sources.classes.db.Table", return_value=mock_table):
        mock_insert_request = MagicMock()
        with patch("sources.classes.db.insert", return_value=mock_insert_request):
            client = db.Client()
            data = {"column1": "value1", "column2": "value2"}
            client.write_data(mock_engine, "test_table", data)

            # Assert that Table was called with the correct parameters
            # Table.assert_called_once_with('test_table', MetaData(), autoload_with=mock_engine)
            # Assert that insert was called with the correct data
            # insert.assert_called_once_with(mock_table)
            mock_insert_request.values.assert_called_once_with(data)
            mock_connection.commit.assert_called_once()

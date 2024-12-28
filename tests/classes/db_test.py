"""Tests for the db module."""

from sources.classes import db


def test_connection():
    """Test the connection method."""
    assert isinstance(db.Client().connection(), object)


def test_connection_exception():
    """Test the connection method with an exception."""
    db.Client().host = "localhost"
    assert isinstance(db.Client().connection(), object)


def test_set_engine():
    """Test the set_engine method."""
    engine = db.Client().connection()
    assert isinstance(engine, object)
    assert engine is not None
    db.Client().set_engine(engine)


def test_set_engine_with_none():
    """Test the set_engine method with None."""
    db.Client().set_engine(None)
    assert db.Client().get_engine() is not None


def test_get_engine():
    """Test the get_engine method."""
    db.Client().set_engine(db.Client().connection())
    assert isinstance(db.Client().get_engine(), object)
    assert db.Client().get_engine() is not None


def test_close_connection():
    """Test the close_connection method."""
    engine = db.Client().connection()
    db.Client().close_connection(engine)
    assert db.Client().engine is None


def test_drop_schema():
    """Test the drop_schema method."""
    engine = db.Client().connection()
    db.Client().drop_schema(engine)

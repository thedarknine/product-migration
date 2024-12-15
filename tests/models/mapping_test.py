"""Test the mapping model."""

from sources.models.mapping import Mapping, OpenProject, Plane


def test_construct_with_empty_lists():
    """Test the construct method."""
    mapping = Mapping(
        openproject=OpenProject(exclude_projects=[]), plane=Plane(exclude_users=[])
    )
    assert isinstance(mapping, Mapping)
    assert isinstance(mapping.openproject, OpenProject)
    assert isinstance(mapping.plane, Plane)
    assert mapping.openproject.exclude_projects == []
    assert mapping.openproject.exclude_users is None
    assert mapping.plane.exclude_projects is None
    assert mapping.plane.exclude_users == []


def test_construct_with_lists():
    """Test the construct method."""
    mapping = Mapping(
        openproject=OpenProject(exclude_projects=["project1", "project2"]),
        plane=Plane(exclude_users=["user1", "user2"]),
    )
    assert isinstance(mapping, Mapping)
    assert isinstance(mapping.openproject, OpenProject)
    assert isinstance(mapping.plane, Plane)
    assert mapping.openproject.exclude_projects == ["project1", "project2"]
    assert mapping.plane.exclude_users == ["user1", "user2"]

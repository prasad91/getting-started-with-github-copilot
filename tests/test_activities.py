"""
Tests for GET /activities endpoint.
Verify response structure, participant counts, and activity list integrity.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Arrange: Client is ready
    Act: Request all activities
    Assert: Response contains all activities with correct structure
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Class", "Drama Club", "Science Club", "Debate Team"
    ]
    assert all(activity in activities for activity in expected_activities)


def test_activity_has_required_fields(client):
    """
    Arrange: Client is ready
    Act: Request all activities
    Assert: Each activity has required fields (description, schedule, max_participants, participants)
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity_name, activity_data in activities.items():
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"


def test_participants_is_list(client):
    """
    Arrange: Client is ready
    Act: Request all activities
    Assert: Participants field is a list for each activity
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants is not a list"


def test_activity_participants_count_matches_max(client):
    """
    Arrange: Client is ready
    Act: Request all activities
    Assert: Number of participants does not exceed max_participants
    """
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        participant_count = len(activity_data["participants"])
        max_participants = activity_data["max_participants"]
        assert participant_count <= max_participants, \
            f"Activity '{activity_name}' has {participant_count} participants but max is {max_participants}"

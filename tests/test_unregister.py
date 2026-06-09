"""
Tests for POST /activities/{activity_name}/unregister endpoint.
Test successful unregistration, validation errors, and edge cases.
"""

import pytest


def test_unregister_existing_participant(client):
    """
    Arrange: Get an existing participant from an activity
    Act: Post unregister request
    Assert: Status 200, participant removed, success message returned
    """
    # Arrange
    activity = "Chess Club"
    initial_response = client.get("/activities")
    email = initial_response.json()[activity]["participants"][0]
    
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert email in response.json()["message"]


def test_unregister_removes_participant_from_activity(client):
    """
    Arrange: Get an existing participant from an activity
    Act: Post unregister request, then fetch activities
    Assert: Participant no longer appears in activity's participant list
    """
    # Arrange
    activity = "Gym Class"
    initial_response = client.get("/activities")
    email = initial_response.json()[activity]["participants"][0]
    initial_count = len(initial_response.json()[activity]["participants"])
    
    # Act
    unregister_response = client.post(f"/activities/{activity}/unregister?email={email}")
    fetch_response = client.get("/activities")
    
    # Assert
    assert unregister_response.status_code == 200
    updated_participants = fetch_response.json()[activity]["participants"]
    assert email not in updated_participants
    assert len(updated_participants) == initial_count - 1


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Arrange: Prepare valid email but invalid activity name
    Act: Post unregister request
    Assert: Status 404, error message indicates activity not found
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent Activity"
    
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_nonexistent_participant_returns_404(client):
    """
    Arrange: Prepare valid activity but email not registered for it
    Act: Post unregister request
    Assert: Status 404, error message indicates participant not found
    """
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Science Club"
    
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    """
    Arrange: Get an existing participant, unregister them
    Act: Sign them up again
    Assert: Participant can be re-registered after unregistering
    """
    # Arrange
    activity = "Drama Club"
    initial_response = client.get("/activities")
    email = initial_response.json()[activity]["participants"][0]
    
    # Act
    unregister_response = client.post(f"/activities/{activity}/unregister?email={email}")
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    fetch_response = client.get("/activities")
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    assert email in fetch_response.json()[activity]["participants"]


def test_unregister_multiple_participants_sequentially(client):
    """
    Arrange: Get an activity with multiple participants
    Act: Unregister each participant
    Assert: Each is removed without affecting others
    """
    # Arrange
    activity = "Science Club"
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"].copy()
    
    # Act & Assert
    for i, email in enumerate(initial_participants):
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify this participant is removed but others remain
        fetch_response = client.get("/activities")
        remaining = fetch_response.json()[activity]["participants"]
        assert email not in remaining
        
        # Verify other participants are still there
        for other_email in initial_participants[i+1:]:
            assert other_email in remaining

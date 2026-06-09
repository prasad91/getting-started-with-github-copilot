"""
Tests for POST /activities/{activity_name}/signup endpoint.
Test successful signups, validation errors, and edge cases.
"""

import pytest


def test_signup_with_valid_email_and_activity(client):
    """
    Arrange: Prepare valid email and activity name
    Act: Post signup request
    Assert: Status 200, participant added to activity, success message returned
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_adds_participant_to_activity(client):
    """
    Arrange: Prepare valid email and activity name
    Act: Post signup request, then fetch activities
    Assert: Participant appears in activity's participant list
    """
    # Arrange
    email = "alice@mergington.edu"
    activity = "Programming Class"
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"]
    
    # Act
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    fetch_response = client.get("/activities")
    
    # Assert
    assert signup_response.status_code == 200
    updated_participants = fetch_response.json()[activity]["participants"]
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_nonexistent_activity_returns_404(client):
    """
    Arrange: Prepare valid email but invalid activity name
    Act: Post signup request
    Assert: Status 404, error message indicates activity not found
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent Activity"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email_returns_400(client):
    """
    Arrange: Prepare email already signed up for activity
    Act: Post signup request with existing participant
    Assert: Status 400, error message indicates student already signed up
    """
    # Arrange
    activity = "Chess Club"
    # Get an existing participant from the activity
    initial_response = client.get("/activities")
    existing_email = initial_response.json()[activity]["participants"][0]
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={existing_email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_different_activities(client):
    """
    Arrange: Prepare same email for two different activities
    Act: Sign up for both activities
    Assert: Email appears in both activities' participant lists
    """
    # Arrange
    email = "multiactivity@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Art Class"
    
    # Act
    response1 = client.post(f"/activities/{activity1}/signup?email={email}")
    response2 = client.post(f"/activities/{activity2}/signup?email={email}")
    fetch_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email in fetch_response.json()[activity1]["participants"]
    assert email in fetch_response.json()[activity2]["participants"]


def test_signup_email_case_sensitivity(client):
    """
    Arrange: Prepare two emails with different cases
    Act: Sign up with both
    Assert: Both emails are added (emails are case-sensitive)
    """
    # Arrange
    email1 = "Student@mergington.edu"
    email2 = "student@mergington.edu"
    activity = "Tennis Club"
    
    # Act
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    fetch_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    participants = fetch_response.json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants

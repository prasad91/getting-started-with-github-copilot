"""
Tests for GET / endpoint.
Verify root path redirects to static HTML file.
"""

import pytest


def test_root_redirects_to_static_index(client):
    """
    Arrange: Client is ready
    Act: Request root path without following redirects
    Assert: Status 307 (temporary redirect), location header points to /static/index.html
    """
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirects(client):
    """
    Arrange: Client is ready
    Act: Request root path with follow_redirects=True
    Assert: Final response is from static file (200 OK)
    """
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200

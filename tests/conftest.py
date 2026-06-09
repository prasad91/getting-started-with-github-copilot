"""
Pytest configuration and fixtures for API tests.
Provides test client and isolated activities data for each test.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Arrange: Provides a TestClient for making HTTP requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def activities_fixture():
    """
    Arrange: Provides isolated activities data for each test.
    Uses deepcopy to prevent mutations from affecting other tests.
    """
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(activities_fixture):
    """
    Arrange: Automatically resets activities data before each test.
    This ensures test isolation - no side effects between tests.
    """
    # Reset the activities dictionary in the app to the isolated copy
    app.state.activities = activities_fixture
    # Also update the module-level activities variable
    import src.app as app_module
    original_activities = app_module.activities.copy()
    app_module.activities.clear()
    app_module.activities.update(activities_fixture)
    
    yield
    
    # Restore original state after test
    app_module.activities.clear()
    app_module.activities.update(original_activities)

import pytest

from fastapi.testclient import TestClient

from app.core.process import NotificationLogProcess
from app.core.constants import OK
from app.core.exceptions import NotFoundException
from config import app

client = TestClient(app)

@pytest.fixture
def setup_mocks():
    NotificationLogProcess.send_notification = MagicMock(return_value={
        'status': OK,
        'message': 'Notification processed successfully',
        'data': {}
    })

def test_notify_success(setup_mocks):
    request_data = {
        "category": "TestCategory",
        "message": "Test notification message"
    }
    
    response = client.post("/notifications", json=request_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "status": OK,
        "message": "Notification processed successfully",
        "data": request_data
    }

def test_notify_category_not_found(setup_mocks):
    NotificationLogProcess.send_notification = MagicMock(return_value={
        'status': NotFoundException.status,
        'message': "Category not found",
        'data': {}
    })
    
    request_data = {
        "category": "InvalidCategory",
        "message": "Test notification message"
    }
    
    response = client.post("/notifications", json=request_data)
    
    assert response.status_code == NotFoundException.status
    assert response.json() == {
        "status": NotFoundException.status,
        "detail": "Category not found"
    }

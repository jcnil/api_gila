import pytest

from app.core.process import NotificationLogProcess
from app.core.exceptions import NotFoundException
from app.core.handlers import NotificationsHandler
from app.core.querysets import Queryset
from app.core.constants import OK

from unittest.mock import MagicMock

@pytest.fixture
def setup_mocks():
    NotificationLogProcess.send_notification = MagicMock()
    Queryset.log_notification = MagicMock()

def test_send_notification_success(setup_mocks):
    request = {
        'category': 'TestCategory',
        'message': 'Test message'
    }
    
    # Mock get_subscribed_users to return a list with a mock user
    from app.core.helpers import get_subscribed_users
    get_subscribed_users = MagicMock(return_value=[MagicMock(id=1, channels=[MagicMock(name='SMS')])])

    # Mock NotificationsHandler
    NotificationsHandler.NOTIFICATION_HANDLERS = {
        "SMS": MagicMock()
    }
    
    result = NotificationLogProcess.send_notification(request)
    
    assert result['status'] == OK
    assert result['message'] == "Notification processed successfully"
    assert Queryset.log_notification.called
    assert NotificationsHandler.NOTIFICATION_HANDLERS['SMS'].called

def test_send_notification_category_not_found(setup_mocks):
    request = {
        'category': 'InvalidCategory',
        'message': 'Test message'
    }
    
    result = NotificationLogProcess.send_notification(request)
    
    assert result['status'] == NotFoundException.status
    assert result['message'] == "Category not found"

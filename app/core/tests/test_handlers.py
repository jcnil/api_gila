import pytest
from app.core.handlers import NotificationsHandler
from app.core.process import NotificationLogProcess

@pytest.fixture
def setup_mocks():
    NotificationLogProcess.send_notification = MagicMock()

def test_handle_sms(setup_mocks):
    user = MagicMock(id=1, phone='1234567890', subscribed='TestCategory')
    message = 'Test SMS message'
    
    NotificationsHandler.handle_sms(user, message)
    
    NotificationLogProcess.send_notification.assert_called_once_with(
        user_id=user.id,
        category=user.subscribed,
        channel="SMS",
        message=message
    )

def test_handle_email(setup_mocks):
    user = MagicMock(id=1, email='test@example.com', subscribed='TestCategory')
    message = 'Test Email message'
    
    NotificationsHandler.handle_email(user, message)
    
    NotificationLogProcess.send_notification.assert_called_once_with(
        user_id=user.id,
        category=user.subscribed,
        channel="Email",
        message=message
    )

def test_handle_push_notification(setup_mocks):
    user = MagicMock(id=1, name='Test User', subscribed='TestCategory')
    message = 'Test Push Notification message'
    
    NotificationsHandler.handle_push_notification(user, message)
    
    NotificationLogProcess.send_notification.assert_called_once_with(
        user_id=user.id,
        category=user.subscribed,
        channel="PushNotification",
        message=message
    )
from app.core.constants import NOTIFICATION_TYPES
from app.core.process import (
    UserProcess,
    NotificationLogProcess
)

class UserHandler:
    @staticmethod
    def register_user(request):
        obj = UserProcess()
        return obj.register(request)
    
    @staticmethod
    def get_user(user_id):
        obj = UserProcess()
        return obj.get_user(user_id)


    @staticmethod
    def update_user(user_id, request):
        obj = UserProcess()
        return obj.update_user(user_id, request)


class NotificationsHandler:
    @staticmethod
    def get_subscribed_users(category):
        obj = NotificationLogProcess()
        return obj.get_subscribed_users(category)

    @staticmethod
    def get_notifications_by_notify_id(notify_id):
        obj = NotificationLogProcess()
        return obj.get_notifications_by_notify_id(notify_id)

    @staticmethod
    def handle_sms(user, message):
        NotificationLogProcess.send_notification({
            "user_id": user.id,
            "category": user.subscribed,
            "channel": NOTIFICATION_TYPES["SMS"],
            "message": message
        })
        print(f"SMS sent to {user.phone}: {message}")

    @staticmethod
    def handle_email(user, message):
        NotificationLogProcess.send_notification({
            "user_id": user.id,
            "category": user.subscribed,
            "channel": NOTIFICATION_TYPES["Email"],
            "message": message
        })
        print(f"Email sent to {user.email}: {message}")

    @staticmethod
    def handle_push_notification(user, message):
        NotificationLogProcess.send_notification({
            "user_id": user.id,
            "category": user.subscribed,
            "channel": NOTIFICATION_TYPES["PushNotification"],
            "message": message
        })
        print(f"Push notification sent to {user.name}: {message}")

    NOTIFICATION_HANDLERS = {
        "SMS": handle_sms,
        "Email": handle_email,
        "PushNotification": handle_push_notification,
    }


from mongoengine import DoesNotExist

from .models import (
    NotificationLogModel,
    UserModel
)

class Queryset:
    @staticmethod
    def get_user_by_id(user_id: str) -> UserModel:
        """Retrieve a user by their ID."""
        return UserModel.objects(user_id=user_id).first()


    @staticmethod
    def get_users_by_category(category: str) -> list:
        """Retrieve users subscribed to a specific category."""
        return UserModel.objects(subscribed=category).all()

    @staticmethod
    def create_user(request: dict) -> UserModel:
        """Create a new user based on provided data in request."""
        user = UserModel(**request)
        user.save()
        return user

    @staticmethod
    def update_user(user_id: str, request: dict) -> UserModel:

        user = UserModel.objects.get(user_id=user_id)

        user.name = request.get('name')
        user.email = request.get('email')
        user.phone = request.get('phone')
        user.subscribed = request.get('subscribed')
        user.channels = request.get('channels')
        user.save()

        return user

    @staticmethod
    def log_notification(request: dict) -> NotificationLogModel:
        """Log a notification into the database."""

        user_id = request.get('user_id')
        if not user_id:
            raise ValueError("User ID must be provided in the request")

        user = UserModel.objects.get(user_id=user_id)

        request['user'] = user

        log_entry = NotificationLogModel(**request)
        log_entry.save()
        return log_entry

    @staticmethod
    def get_notifications_by_user(user_id: str) -> list:
        """Retrieve all notifications sent to a specific user."""
        return NotificationLogModel.objects(user_id=user_id).all()
    
    @staticmethod
    def get_notifications_by_notify_id(notify_id: str) -> list:
        return NotificationLogModel.objects(notify_id=notify_id).all()
    
    @staticmethod
    def update_notifications(notify_id: str, request: dict) -> NotificationLogModel:

        notify = NotificationLogModel.objects.get(notify_id=notify_id)

        notify.user_id = request.get('user_id')
        notify.category = request.get('category')
        notify.channel = request.get('channel')
        notify.message = request.get('message')
        notify.save()

        return notify

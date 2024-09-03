from app.core.exceptions import NotFoundException
from app.core.querysets import Queryset
from app.core.helpers import get_subscribed_users
from app.core.constants import OK, CATEGORIES


class UserProcess:
    @staticmethod
    def register(request: dict) -> dict:
        
        user_id = request.get('user_id')
        user = Queryset.get_user_by_id(
            user_id=user_id
        )

        if not user:

            Queryset.create_user(request)

            return {
                "status": 201,
                "message": "Registered",
                "data": request
            }

        return {
            "status": OK,
            "message": "Exist User in Database",
            "data": request
        }

    @staticmethod
    def get_user(
        user_id: str
    ) -> dict:

        user = Queryset.get_user_by_id(
            user_id=user_id
        )

        if user is not None:
            return {
                "status": OK,
                "message": "Exist User in Database",
                "data": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "subscribed": user.subscribed,
                    "channels": user.channels
                }
            }
        raise NotFoundException
    @staticmethod
    def update_user(
        user_id: str, 
        request: dict
    ) -> dict:
        user = Queryset.update_user(
            user_id=user_id,
            request=request
        )

        if user is not None:
            return {
                "status": OK,
                "message": "Update user in Database",
                "data": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "subscribed": user.subscribed,
                    "channels": user.channels
                }
            }
        raise NotFoundException


class NotificationLogProcess:
    @staticmethod
    def get_notifications_by_notify_id(
        notify_id: str
    ) -> dict:

        notify = Queryset.get_notifications_by_notify_id(
            notify_id=notify_id
        )

        if notify is not None:
            return {
                "status": OK,
                "message": "Exist Notifications in Database",
                "data": {
                    "notify_id": notify.notify_id,
                    "user_id": notify.user_id,
                    "category": notify.category.name,
                    "channel": notify.channel.name,
                    "message": notify.message
                }
            }
        raise NotFoundException

    @staticmethod
    def get_subscribed_users(category: str):
        users = Queryset.get_users_by_category(
            category=category
        )

        if users is not None:
            return {
                "status": OK,
                "message": "Exist Users in Database",
                "data": [user for user in users]
            }
        raise NotFoundException

    @staticmethod
    def send_notification(request: dict) -> dict:
        """Sends notifications to users based on category and channels they are subscribed to."""
        
        category = request['category']
        if category not in CATEGORIES:
            return {
                "status": NotFoundException.status,
                "message": "Category not found",
                "data": request
            }

        users = get_subscribed_users(category)
        for user in users:
            for channel in user.channels:
                handler = NotificationsHandler.NOTIFICATION_HANDLERS.get(channel.name)
                if handler:
                    handler(user, request['message'])
                    
                    Queryset.log_notification({
                        "user_id": user.id,
                        "category": category,
                        "channel": channel.name,
                        "message": request['message']
                    })

        return {
            "status": OK,
            "message": "Notification processed successfully",
            "data": request
        }

import uuid

from mongoengine.fields import (
    EmailField,
    StringField,
    DictField,
    DateTimeField,
    ListField, 
    EnumField
)
from mongoengine import (
    Document,
    ReferenceField
)

from app.core.helpers import local_now
from app.core.constants import CategoryEnum, NotificationChannelEnum


class BaseDocument(Document):
    """Document base to inherit all models.

    Attributes:
        updated_at (datetime.datetime): The time when the document was last updated.
        created_at (datetime.datetime): The time when the document was created.
        deleted_at (datetime.datetime): The time when the document was deleted (soft delete).
        deleted_by (dict): Information about who deleted the document.
    """
    updated_at = DateTimeField(default=local_now, required=False)
    created_at = DateTimeField(default=local_now)
    deleted_at = DateTimeField(required=False)
    deleted_by = DictField(required=False)

    meta = {
        "abstract": True,
    }

    def update(self):
        self.updated_at = local_now()
        self.save()


class UserModel(BaseDocument):
    """User model representing a user in the system."""

    meta = {
        "collection": "users",
        "indexes": ["user_id","email"]
    }

    user_id = StringField(default=lambda: str(uuid.uuid4()), unique=True)
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField(required=True)
    subscribed = ListField(EnumField(CategoryEnum), required=True)
    channels = ListField(EnumField(NotificationChannelEnum), required=True)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subscribed": [category.to_json() for category in self.subscribed],
            "channels": [channel.to_json() for channel in self.channels]
        }


class NotificationLogModel(BaseDocument):
    """Model to log notification details."""

    meta = {
        "collection": "notification_logs",
        "indexes": ["user", "category", "channel"]
    }

    notify_id = StringField(default=lambda: str(uuid.uuid4()), unique=True)
    category = EnumField(CategoryEnum, required=True)
    channel = EnumField(NotificationChannelEnum, required=True)
    message = StringField()
    user = ReferenceField(UserModel, required=True)

    def to_json(self):
        return {
            "notify_id": self.notify_id,
            "user_id": str(self.user.user_id),
            "category": self.category.name,
            "channel": self.channel.name,
            "message": self.message
        }

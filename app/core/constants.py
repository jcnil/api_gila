from decouple import config

from enum import Enum

TIMEZONE = config("TIMEZONE")
MONGO_URI = config("MONGO_URI")

SERVER_ERROR = "Internal Server Error"

OK = 200
INTERNAL_SERVER_ERROR = "A server error occurred"
BAD_REQUEST = "Invalid input data"
ACCEPTED = "Request accepted"
NOT_ACCEPTABLE = "Request not accepted"

CATEGORIES = ["Sports", "Finance", "Films"]
NOTIFICATION_TYPES = ["SMS", "Email", "PushNotification"]

class CategoryEnum(Enum):
    """Enum for message categories."""
    SPORTS = "Sports"
    FINANCE = "Finance"
    FILMS = "Films"

    def to_json(self):
        return self.value


class NotificationChannelEnum(Enum):
    """Enum for notification channels."""
    SMS = "SMS"
    EMAIL = "Email"
    PUSH_NOTIFICATION = "PushNotification"

    def to_json(self):
        return self.value


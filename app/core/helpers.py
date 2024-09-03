from datetime import datetime

import pytz

from app.core.constants import TIMEZONE


def local_now():
    """datetime.datetime.now of local timezone

    Returns:
        datetime.datetime:
    """
    timezone = TIMEZONE
    now = datetime.now(pytz.timezone(
        timezone
    ))
    return datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second,
        microsecond=now.microsecond
    )

def get_subscribed_users(category):
    users = [
        {
            "id": 1,
            "name": "John", 
            "email": "john@example.com", 
            "phone": "1234567890", 
            "subscribed": ["Sports", "Finance"], 
            "channels": ["Email", "SMS"]},
        {
            "id": 2, 
            "name": "Jane", 
            "email": "jane@example.com", 
            "phone": "0987654321", 
            "subscribed": ["Films"], 
            "channels": ["PushNotification"]}
    ]
    
    return [user for user in users if category in user["subscribed"]]

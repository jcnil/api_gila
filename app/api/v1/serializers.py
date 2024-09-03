import uuid

from pydantic import(
    BaseModel,
    Field,
    constr
)
from typing import Optional, Union, List

from app.core.constants import (
    CategoryEnum,
    NotificationChannelEnum
)


class ResponseSerializer(BaseModel):
    status: Optional[str] = Field(
        title="Status Code",
    )
    data: Optional[dict] = Field(
        title="Response data",
    )
    message: Optional[str] = Field(
        title="Complementary message",
    )
    errors: Optional[Union[dict, list]] = Field(
        title="Retrieves a list of errors if an action fails",
    )


class MetaDataSerializer(BaseModel):
    text: str = Field(
        title="Text"
    )
    url: str = Field(
        title="Public url of the file"
    )


class NotificationRequest(BaseModel):
    category: CategoryEnum = Field(
        title="Category of notification"
    )
    message: constr(min_length=1) = Field(
        title="Message of notification"
    )


class NotificationLogBase(BaseModel):
    notify_id: str = Field(
        title="notify_id",
        default=str(uuid.uuid4())
    )
    category: CategoryEnum = Field(
        title="Category of notification"
    )
    channel: NotificationChannelEnum = Field(
        title="Channel of notification"
    )
    message: Optional[str] = None

    class Config:
        orm_mode = True


class UserInput(BaseModel):
    user_id: str = Field(
        title="user_id",
        default=str(uuid.uuid4())
    )
    name: str = Field(
        title="Name of user",
        default="Jose"

    )
    email: str = Field(
        title="Email of user",
        default="example@example.com"
    )
    phone: str = Field(
        title="Phone of user",
        default="123456"
    )
    subscribed: List[CategoryEnum] = Field(
        title="Category of notification"
    )
    channels: List[NotificationChannelEnum] = Field(
        title="Channel of notification"
    )

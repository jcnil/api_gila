import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.core.exceptions import ExistException, NotFoundException
from app.core.handlers import (
    NotificationsHandler,
    UserHandler
)
from app.api.v1.serializers import(
    UserInput,
    NotificationRequest,
    ResponseSerializer  
)


router = APIRouter()


@router.get(
    "/users/{user_id}",
    tags=["Users"],
    response_model=ResponseSerializer
)
async def get_notifications(
    user_id: str
):
    """Get user by specific user_id"""
    try:
        result = UserHandler.get_user(
            user_id=user_id
        )
        return JSONResponse(
            content={
                "status": result["status"],
                "data": result["data"],
                "message": str(result["message"])
            }
        )
    except NotFoundException as e:
        return JSONResponse(
            content={
                "status": e.status,
                "data": user_id,
                "message": str(e.message("User")),
                "errors": str(e)
            },
            status_code=e.status
        )
    except HTTPException as e:
        return JSONResponse(
            content={
                "status": e.status_code,
                "detail": e.detail
            },
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": 500,
                "detail": str(e)
            },
            status_code=500
        )


@router.post(
    "/users",
    tags=["Users"],
    response_model=ResponseSerializer
)
async def post_create_user(
    user: UserInput
):
    """Post create user"""
    try:
        result = UserHandler.register_user(user.dict())
        return JSONResponse(
            content={
                "status": result["status"],
                "data": result["data"],
                "message": str(result["message"])
            }
        )
    except ExistException as e:
        return JSONResponse(
            content={
                "status": e.status,
                "data": result["data"],
                "message": str(e.message("User")),
                "errors": str(e)
            },
            status_code=e.status
        )
    except HTTPException as e:
        return JSONResponse(
            content={
                "status": e.status_code,
                "detail": e.detail
            },
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": 500,
                "detail": str(e)
            },
            status_code=500
        )


@router.get(
    "/notifications/{notify_id}",
    tags=["Notifications"],
    response_model=ResponseSerializer
)
async def get_notification(
    notify_id: str
):
    """Get notification by specific notify_id"""
    try:
        result = NotificationsHandler.get_notifications_by_notify_id(
            notify_id=notify_id
        )
        return JSONResponse(
            content={
                "status": result["status"],
                "data": result["data"],
                "message": str(result["message"])
            }
        )
    except NotFoundException as e:
        return JSONResponse(
            content={
                "status": e.status,
                "data": notify_id,
                "message": str(e.message("Notification")),
                "errors": str(e)
            },
            status_code=e.status
        )
    except HTTPException as e:
        return JSONResponse(
            content={
                "status": e.status_code,
                "detail": e.detail
            },
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": 500,
                "detail": str(e)
            },
            status_code=500
        )


@router.post(
    "/notifications",
    tags=["Notifications"],
    response_model=ResponseSerializer
)
async def notify(request: NotificationRequest):
    try:
        category = request.category
        message = request.message

        users = NotificationsHandler.get_subscribed_users(category)

        if not users:
            raise NotFoundException("No users found for the given category")

        for user in users:
            for channel in user.channels:
                handler = NotificationsHandler.NOTIFICATION_HANDLERS.get(channel.name)
                if handler:
                    handler(user, message)
                else:
                    raise HTTPException(status_code=400, detail=f"Handler for channel {channel.name} not found")

        return JSONResponse(
            content={
                "status": 200,
                "data": request.dict(),
                "message": "Notification processed successfully"
            }
        )
    except NotFoundException as e:
        return JSONResponse(
            content={
                "status": e.status,
                "detail": str(e)
            },
            status_code=e.status
        )
    except HTTPException as e:
        return JSONResponse(
            content={
                "status": e.status_code,
                "detail": e.detail
            },
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": 500,
                "detail": str(e)
            },
            status_code=500
        )
